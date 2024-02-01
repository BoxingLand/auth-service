from uuid import UUID

import grpc

from app.auth import auth_pb2, auth_pb2_grpc
from app.core.security import security
from app.core.security.security import TokenType, create_jwt_tokens



class Auth(auth_pb2_grpc.AuthServicer):
    async def VerifyEmail(
            self,
            request: auth_pb2.VerifyEmailRequest,
            context: grpc.aio.ServicerContext,
    ) -> auth_pb2.VerifyEmailResponse:
        ...

    async def VerifyEmailNew(
            self,
            request: auth_pb2.VerifyEmailNewRequest,
            context: grpc.aio.ServicerContext,
    ) -> auth_pb2.VerifyEmailNewResponse:
        ...

    async def Refresh(
            self,
            request: auth_pb2.RefreshRequest,
            context: grpc.aio.ServicerContext,
    ) -> auth_pb2.RefreshResponse:
        refresh_token_decoded = security.decode_token(token=request.refresh_token, context=context)
        if refresh_token_decoded["type"] != TokenType.refresh_token:
            await context.abort(grpc.StatusCode.PERMISSION_DENIED, details="TokenIncorrect")

        token_data = await create_jwt_tokens(
            user_id=refresh_token_decoded["sub"]
        )

        return auth_pb2.RefreshResponse(
            token_type=token_data.token_type,
            access_token=token_data.access_token,
            refresh_token=token_data.refresh_token,
        )

    async def Access(
            self,
            request: auth_pb2.AccessRequest,
            context: grpc.aio.ServicerContext,
    ) -> auth_pb2.AccessResponse:
        access_token_decoded = security.decode_token(
            token=request.access_token,
            context=context
        )

        if access_token_decoded["type"] != TokenType.access_token:
            await context.abort(grpc.StatusCode.PERMISSION_DENIED, details="TokenIncorrect")
        return auth_pb2.AccessResponse(
            exp=access_token_decoded["exp"],
            sub=access_token_decoded["sub"],
            type=access_token_decoded["type"]
        )

    async def CreateTokens(
            self,
            request: auth_pb2.CreateTokensRequest,
            context: grpc.aio.ServicerContext,
    ) -> auth_pb2.CreateTokensResponse:
        token_data = await create_jwt_tokens(
            user_id=UUID(request.user_id)
        )
        access_token_decoded = security.decode_token(
            token=token_data.access_token,
            context=context
        )

        return auth_pb2.CreateTokensResponse(
            token_type=token_data.token_type,
            access_token=token_data.access_token,
            refresh_token=token_data.refresh_token,
        )
