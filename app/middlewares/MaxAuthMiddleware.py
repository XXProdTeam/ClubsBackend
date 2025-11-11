import hmac
import hashlib
from typing import List, Tuple
from urllib.parse import unquote, parse_qsl

from fastapi import Request
from fastapi.responses import JSONResponse

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


class MaxAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, bot_token: str):
        super().__init__(app)
        self.bot_token = bot_token

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        if not request.url.path.startswith("/api/v1/") or request.method == "OPTIONS":
            return await call_next(request)

        init_data_header = request.headers.get("X-Max-Init-Data")

        if not init_data_header:
            return JSONResponse(
                status_code=401,
                content={"detail": "X-Max-Init-Data Header is missing"},
            )

        try:
            is_valid = self.validate_init_data(init_data_header)
            if not is_valid:
                return JSONResponse(
                    status_code=403,
                    content={"detail": "Invalid initData"},
                )
        except Exception as e:
            return JSONResponse(
                status_code=403,
                content={"detail": f"Validation Error: {e}"},
            )

        response = await call_next(request)
        return response

    def validate_init_data(self, init_data: str) -> bool:
        """
        Валидирует строку initData в соответствии с документацией MAX - Валидация данных.
        """
        decoded_str = unquote(init_data)

        received_hash = ""
        data_check_pairs: List[Tuple[str, str]] = []

        parsed_data = parse_qsl(decoded_str)

        for key, value in parsed_data:
            if key == "hash":
                received_hash = value
            else:
                data_check_pairs.append((key, value))

        if not received_hash:
            raise ValueError("Parameter hash not found in initData")

        data_check_pairs.sort(key=lambda x: x[0])
        data_check_string = "\n".join(
            [f"{key}={value}" for key, value in data_check_pairs]
        )

        secret_key = hmac.new(
            "WebAppData".encode(), self.bot_token.encode(), hashlib.sha256
        ).digest()

        calculated_hash = hmac.new(
            secret_key, data_check_string.encode(), hashlib.sha256
        ).hexdigest()

        return calculated_hash == received_hash
