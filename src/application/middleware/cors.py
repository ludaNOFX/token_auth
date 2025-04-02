import re
from collections.abc import Callable, Sequence

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from starlette.requests import Request
from starlette.responses import Response, PlainTextResponse


ALL_METHODS = ("DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT")
SAFELISTED_HEADERS = {"Accept", "Accept-Language", "Content-Language", "Content-Type"}


class CustomCORSMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        allow_origins: Sequence[str] = (),
        allow_methods: Sequence[str] = ("GET",),
        allow_headers: Sequence[str] = (),
        allow_credentials: bool = False,
        allow_origin_regex: str | None = None,
        expose_headers: Sequence[str] = (),
        max_age: int = 600,
    ) -> None:
        super().__init__(app)
        self.allow_all_origins = "*" in allow_origins
        self.allow_all_headers = "*" in allow_headers
        self.allow_origin_regex = (
            re.compile(allow_origin_regex) if allow_origin_regex else None
        )  # noqa: E501
        self.allow_methods = set(ALL_METHODS if "*" in allow_methods else allow_methods)
        self.allow_headers = SAFELISTED_HEADERS | set(allow_headers)
        self.allow_credentials = allow_credentials
        self.expose_headers = expose_headers
        self.max_age = max_age
        self.preflight_explicit_allow_origin = (
            not self.allow_all_origins or allow_credentials
        )  # noqa: E501

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        origin = request.headers.get("origin")
        if not origin:
            return await call_next(request)

        if (
            request.method == "OPTIONS"
            and "access-control-request-method" in request.headers
        ):
            return self.preflight_response(request)

        response = await call_next(request)
        return self.simple_response(response, origin)

    def preflight_response(self, request: Request) -> Response:
        headers = {
            "Access-Control-Allow-Methods": ", ".join(self.allow_methods),
            "Access-Control-Max-Age": str(self.max_age),
            "Vary": "Origin" if self.preflight_explicit_allow_origin else "",
        }

        if self.allow_all_origins:
            headers["Access-Control-Allow-Origin"] = "*"
        else:
            headers["Access-Control-Allow-Origin"] = request.headers["origin"]

        requested_headers = request.headers.get("access-control-request-headers")
        if self.allow_all_headers and requested_headers:
            headers["Access-Control-Allow-Headers"] = requested_headers
        elif requested_headers:
            headers["Access-Control-Allow-Headers"] = ", ".join(
                h
                for h in requested_headers.split(",")
                if h.strip().lower() in self.allow_headers
            )

        if self.allow_credentials:
            headers["Access-Control-Allow-Credentials"] = "true"

        return PlainTextResponse("OK", status_code=200, headers=headers)

    def simple_response(self, response: Response, origin: str) -> Response:
        if self.allow_all_origins:
            response.headers["Access-Control-Allow-Origin"] = "*"
        else:
            response.headers["Access-Control-Allow-Origin"] = origin

        if self.allow_credentials:
            response.headers["Access-Control-Allow-Credentials"] = "true"

        if self.expose_headers:
            response.headers["Access-Control-Expose-Headers"] = ", ".join(
                self.expose_headers
            )  # noqa: E501

        return response
