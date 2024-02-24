import logging
from timeit import default_timer
from typing import Awaitable, Callable

import grpc
from prometheus_client.registry import REGISTRY
from py_grpc_prometheus import grpc_utils, server_metrics

logger = logging.getLogger()

LEGACY = True
SKIP_EXCEPTION = False
ENABLE_HANDLING_TIME_HISTOGRAM = True

_code_to_status_mapping = {x.value[0]: x for x in grpc.StatusCode}

metrics = server_metrics.init_metrics(REGISTRY)
grpc_server_handled_total_counter = server_metrics.get_grpc_server_handled_counter(
    LEGACY,
    REGISTRY,
)


async def _wrap_async_iterator_inc_counter(iterator, counter, grpc_type, grpc_service_name, grpc_method_name):
    async for item in iterator:
        counter.labels(
            grpc_type=grpc_type,
            grpc_service=grpc_service_name,
            grpc_method=grpc_method_name).inc()
        yield item


def _compute_error_code(grpc_exception):
    if isinstance(grpc_exception, grpc.aio.Call):
        return grpc_exception.code()
    return grpc.StatusCode.UNKNOWN


def _compute_status_code(servicer_context):
    if servicer_context.code() is None:
        return grpc.StatusCode.OK
    return _code_to_status_mapping[servicer_context.code()]


def _increase_grpc_server_started_counter(grpc_type, grpc_service_name, grpc_method_name):
    metrics["grpc_server_started_counter"].labels(
        grpc_type=grpc_type,
        grpc_service=grpc_service_name,
        grpc_method=grpc_method_name
    ).inc()


def _increase_grpc_server_handled_total_counter(grpc_type, grpc_service_name, grpc_method_name, grpc_code):
    if LEGACY:
        grpc_server_handled_total_counter.labels(
            grpc_type=grpc_type,
            grpc_service=grpc_service_name,
            grpc_method=grpc_method_name,
            code=grpc_code
        ).inc()
    else:
        grpc_server_handled_total_counter.labels(
            grpc_type=grpc_type,
            grpc_service=grpc_service_name,
            grpc_method=grpc_method_name,
            grpc_code=grpc_code
        ).inc()


def _increase_grpc_server_handled_latency(grpc_type, grpc_service_name, grpc_method_name, start):
    if LEGACY:
        metrics["legacy_grpc_server_handled_latency_seconds"].labels(
            grpc_type=grpc_type,
            grpc_service=grpc_service_name,
            grpc_method=grpc_method_name
        ).observe(max(default_timer() - start, 0))
    elif ENABLE_HANDLING_TIME_HISTOGRAM:
        metrics["grpc_server_handled_histogram"].labels(
            grpc_type=grpc_type,
            grpc_service=grpc_service_name,
            grpc_method=grpc_method_name
        ).observe(max(default_timer() - start, 0))


def _wrap_rpc_behavior(handler, new_behavior_factory, grpc_service_name, grpc_method_name):
    """Returns a new rpc handler that wraps the given function"""
    if handler is None:
        return None

    if handler.request_streaming and handler.response_streaming:
        orig_behavior = handler.stream_stream
        handler_factory = grpc.stream_stream_rpc_method_handler
    elif handler.request_streaming and not handler.response_streaming:
        orig_behavior = handler.stream_unary
        handler_factory = grpc.stream_unary_rpc_method_handler
    elif not handler.request_streaming and handler.response_streaming:
        orig_behavior = handler.unary_stream
        handler_factory = grpc.unary_stream_rpc_method_handler
    else:
        orig_behavior = handler.unary_unary
        handler_factory = grpc.unary_unary_rpc_method_handler

    return handler_factory(
        behavior=new_behavior_factory(orig_behavior,
                                      handler.request_streaming,
                                      handler.response_streaming,
                                      grpc_service_name,
                                      grpc_method_name),
        request_deserializer=handler.request_deserializer,
        response_serializer=handler.response_serializer,
    )


# ----------------------------------- metrics wrapper

def metrics_wrapper(behavior, request_streaming, response_streaming, grpc_service_name, grpc_method_name):
    async def new_unary_behavior(request_or_iterator, servicer_context):
        response = None
        try:
            start = default_timer()
            grpc_type = grpc_utils.get_method_type(request_streaming, response_streaming)
            try:
                _increase_grpc_server_started_counter(grpc_type, grpc_service_name, grpc_method_name)

                # Invoke the original rpc behavior.
                response = await behavior(request_or_iterator, servicer_context)

                _increase_grpc_server_handled_total_counter(
                    grpc_type,
                    grpc_service_name,
                    grpc_method_name,
                    _compute_status_code(servicer_context).name
                )

                return response

            except grpc.RpcError as exc:
                _increase_grpc_server_handled_total_counter(
                    grpc_type,
                    grpc_service_name,
                    grpc_method_name,
                    _compute_error_code(exc).name
                )
                raise exc

            finally:
                _increase_grpc_server_handled_latency(grpc_type, grpc_service_name, grpc_method_name, start)

        except Exception as exc:  # pylint: disable=broad-except
            # Allow user to skip the exceptions in order to maintain
            # the basic functionality in the server
            # in order to suppress the noise in logging
            logger.error(exc)
            if SKIP_EXCEPTION:
                response = await behavior(request_or_iterator, servicer_context)
                return response
            raise exc

    async def new_stream_behavior(request_or_iterator, servicer_context):
        iterator = None
        try:
            start = default_timer()
            grpc_type = grpc_utils.get_method_type(request_streaming, response_streaming)
            try:
                _increase_grpc_server_started_counter(grpc_type, grpc_service_name, grpc_method_name)

                iterator = _wrap_async_iterator_inc_counter(
                    behavior(request_or_iterator, servicer_context),
                    metrics["grpc_server_stream_msg_sent"],
                    grpc_type,
                    grpc_service_name,
                    grpc_method_name
                )

                async for obj in iterator:
                    yield obj

                _increase_grpc_server_handled_total_counter(
                    grpc_type,
                    grpc_service_name,
                    grpc_method_name,
                    _compute_status_code(servicer_context).name
                )

            except grpc.RpcError as exc:
                _increase_grpc_server_handled_total_counter(
                    grpc_type,
                    grpc_service_name,
                    grpc_method_name,
                    _compute_error_code(exc).name
                )
                raise exc

            finally:
                _increase_grpc_server_handled_latency(grpc_type, grpc_service_name, grpc_method_name, start)

        except Exception as exc:
            logger.error(exc)
            if SKIP_EXCEPTION:
                async for obj in behavior(request_or_iterator, servicer_context):
                    yield obj
            raise exc

    if response_streaming:
        return new_stream_behavior
    return new_unary_behavior


class PromAioServerInterceptor(grpc.aio.ServerInterceptor):
    def __init__(self):
        logger.info("Initializing metric interceptor")

    async def intercept_service(
            self,
            continuation: Callable[[grpc.HandlerCallDetails], Awaitable[grpc.RpcMethodHandler]],
            handler_call_details: grpc.HandlerCallDetails
    ) -> grpc.RpcMethodHandler:
        """
        Intercepts the server function calls.
        Only intercepts unary requests.
        """
        grpc_service_name, grpc_method_name, _ = grpc_utils.split_method_call(handler_call_details)
        handler = await continuation(handler_call_details)
        handler = _wrap_rpc_behavior(handler, metrics_wrapper, grpc_service_name, grpc_method_name)
        return handler

# from timeit import default_timer
# from typing import Awaitable, Callable
#
# import grpc
# from loguru import logger
# from prometheus_client.registry import REGISTRY
# from py_grpc_prometheus import grpc_utils, server_metrics
#
#
# class PromAioServerInterceptor(grpc.aio.ServerInterceptor):
#     def __init__(
#             self,
#             enable_handling_time_histogram=False,
#             legacy=False,
#             skip_exceptions=False,
#             log_exceptions=True,
#             registry=REGISTRY
#     ) -> None:
#         self._enable_handling_time_histogram = enable_handling_time_histogram
#         self._legacy = legacy
#         self._grpc_server_handled_total_counter = server_metrics.get_grpc_server_handled_counter(
#             self._legacy,
#             registry
#         )
#         self._metrics = server_metrics.init_metrics(registry)
#         self._skip_exceptions = skip_exceptions
#         self._log_exceptions = log_exceptions
#
#         self._code_to_status_mapping = {x.value[0]: x for x in grpc.StatusCode}
#
#     async def intercept_service(
#             self,
#             continuation: Callable[[grpc.HandlerCallDetails], Awaitable[grpc.RpcMethodHandler]],
#             handler_call_details: grpc.HandlerCallDetails
#     ) -> grpc.RpcMethodHandler:
#
#         grpc_service_name, grpc_method_name, _ = grpc_utils.split_method_call(handler_call_details)
#
#         def metrics_wrapper(behavior, request_streaming, response_streaming):
#             async def new_behavior(request_or_iterator, servicer_context):
#                 response_or_iterator = None
#                 try:
#                     start = default_timer()
#                     grpc_type = grpc_utils.get_method_type(request_streaming, response_streaming)
#                     try:
#                         if request_streaming:
#                             request_or_iterator = grpc_utils.wrap_iterator_inc_counter(
#                                 request_or_iterator,
#                                 self._metrics["grpc_server_stream_msg_received"],
#                                 grpc_type,
#                                 grpc_service_name,
#                                 grpc_method_name
#                             )
#                         else:
#                             self._metrics["grpc_server_started_counter"].labels(
#                                 grpc_type=grpc_type,
#                                 grpc_service=grpc_service_name,
#                                 grpc_method=grpc_method_name
#                             ).inc()
#
#                         # Invoke the original rpc behavior.
#                         response_or_iterator = await behavior(request_or_iterator, servicer_context)
#
#                         if response_streaming:
#                             sent_metric = self._metrics["grpc_server_stream_msg_sent"]
#                             response_or_iterator = grpc_utils.wrap_iterator_inc_counter(
#                                 response_or_iterator,
#                                 sent_metric,
#                                 grpc_type,
#                                 grpc_service_name,
#                                 grpc_method_name
#                             )
#
#                         else:
#                             self.increase_grpc_server_handled_total_counter(
#                                 grpc_type,
#                                 grpc_service_name,
#                                 grpc_method_name,
#                                 self._compute_status_code(servicer_context).name
#                             )
#                         return response_or_iterator
#                     except grpc.RpcError as e:
#                         self.increase_grpc_server_handled_total_counter(
#                             grpc_type,
#                             grpc_service_name,
#                             grpc_method_name,
#                             self._compute_error_code(e).name
#                         )
#                         raise e
#
#                     finally:
#
#                         if not response_streaming:
#                             if self._legacy:
#                                 self._metrics["legacy_grpc_server_handled_latency_seconds"].labels(
#                                     grpc_type=grpc_type,
#                                     grpc_service=grpc_service_name,
#                                     grpc_method=grpc_method_name
#                                 ).observe(max(default_timer() - start, 0))
#                             elif self._enable_handling_time_histogram:
#                                 self._metrics["grpc_server_handled_histogram"].labels(
#                                     grpc_type=grpc_type,
#                                     grpc_service=grpc_service_name,
#                                     grpc_method=grpc_method_name
#                                 ).observe(max(default_timer() - start, 0))
#                 except Exception as e:
#                     if self._skip_exceptions:
#                         if self._log_exceptions:
#                             logger.error(e)
#                         if response_or_iterator is None:
#                             return response_or_iterator
#                         return behavior(request_or_iterator, servicer_context)
#                     raise e
#
#             return new_behavior
#
#         handler = await continuation(handler_call_details)
#         optional_any = self._wrap_rpc_behavior(handler, metrics_wrapper)
#
#         return optional_any
#
#     def _compute_status_code(self, servicer_context):
#         if servicer_context.cancelled():
#             return grpc.StatusCode.CANCELLED
#
#         if servicer_context.code() is None:
#             return grpc.StatusCode.OK
#
#         return self._code_to_status_mapping[servicer_context.code()]
#
#     def _compute_error_code(self, grpc_exception):
#         if isinstance(grpc_exception, grpc.aio.Call):
#             return grpc_exception.code()
#
#         return grpc.StatusCode.UNKNOWN
#
#     def increase_grpc_server_handled_total_counter(
#             self, grpc_type, grpc_service_name, grpc_method_name, grpc_code):
#         if self._legacy:
#             self._grpc_server_handled_total_counter.labels(
#                 grpc_type=grpc_type,
#                 grpc_service=grpc_service_name,
#                 grpc_method=grpc_method_name,
#                 code=grpc_code
#             ).inc()
#         else:
#             self._grpc_server_handled_total_counter.labels(
#                 grpc_type=grpc_type,
#                 grpc_service=grpc_service_name,
#                 grpc_method=grpc_method_name,
#                 grpc_code=grpc_code
#             ).inc()
#
#     def _wrap_rpc_behavior(self, handler, fn):
#         if handler is None:
#             return None
#
#         if handler.request_streaming and handler.response_streaming:
#             behavior_fn = handler.stream_stream
#             handler_factory = grpc.stream_stream_rpc_method_handler
#         elif handler.request_streaming and not handler.response_streaming:
#             behavior_fn = handler.stream_unary
#             handler_factory = grpc.stream_unary_rpc_method_handler
#         elif not handler.request_streaming and handler.response_streaming:
#             behavior_fn = handler.unary_stream
#             handler_factory = grpc.unary_stream_rpc_method_handler
#         else:
#             behavior_fn = handler.unary_unary
#             handler_factory = grpc.unary_unary_rpc_method_handler
#
#         return handler_factory(
#             fn(behavior_fn, handler.request_streaming, handler.response_streaming),
#             request_deserializer=handler.request_deserializer,
#             response_serializer=handler.response_serializer
#         )
