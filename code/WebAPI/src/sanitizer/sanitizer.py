import json
from typing import Any
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import bleach


def sanitize_value(value: Any) -> Any:
    """Recursively sanitize strings and nested structures."""
    if isinstance(value, str):
        # Remove dangerous tags, attributes, and JS code
        return bleach.clean(value, strip=True)
    elif isinstance(value, dict):
        return {k: sanitize_value(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [sanitize_value(v) for v in value]
    else:
        return value


class SanitizerMiddleware(BaseHTTPMiddleware):
    """Middleware that sanitizes incoming request data (body, query, and path)."""

    async def dispatch(self, request: Request, call_next):
        # --- Sanitize query parameters ---
        query_params = {k: sanitize_value(v) for k, v in request.query_params.items()}
        request._query_params = query_params  # type: ignore

        # --- Sanitize path parameters (e.g. token in URL) ---
        if "path_params" in request.scope:
            request.scope["path_params"] = {
                k: sanitize_value(v) for k, v in request.scope["path_params"].items()
            }

        # --- Sanitize JSON body (POST, PUT, PATCH) ---
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                body_bytes = await request.body()
                if body_bytes:
                    body_data = json.loads(body_bytes)
                    sanitized_data = sanitize_value(body_data)
                    request._body = json.dumps(sanitized_data).encode("utf-8")  # type: ignore
            except (json.JSONDecodeError, UnicodeDecodeError):
                # skip non-JSON bodies (e.g. form-data or files)
                pass

        response = await call_next(request)
        return response
