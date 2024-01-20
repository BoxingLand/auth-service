from typing import Any


class TokenExpiredSignatureException(Exception):
    def __init__(
            self,
            headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__("Your token has expired. Please log in again.")
        self.status_code = 403
        self.headers = headers


class TokenDecodeException(Exception):
    def __init__(
            self,
            headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__("Error when decoding the token. Please check your request.")
        self.status_code = 403
        self.headers = headers


class TokenMissingRequiredClaimException(Exception):
    def __init__(
            self,
            headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__("There is no required field in your token. Please contact the administrator.")
        self.status_code = 403
        self.headers = headers


class TokenIncorrectException(Exception):
    def __init__(
            self,
            headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__("Incorrect token.")
        self.status_code = 403
        self.headers = headers
