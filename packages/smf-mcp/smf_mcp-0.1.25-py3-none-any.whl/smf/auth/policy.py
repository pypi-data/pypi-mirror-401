"""
Authorization helpers for SMF tools.
"""

from __future__ import annotations

import inspect
from functools import wraps
from typing import Any, Callable, Iterable

from fastmcp.exceptions import ToolError
from mcp.server.auth.middleware.auth_context import get_access_token


def _normalize_scopes(scopes: Iterable[str]) -> set[str]:
    return {s.strip() for s in scopes if s and s.strip()}


def _get_token_scopes() -> set[str]:
    token = get_access_token()
    if token is None:
        return set()
    return _normalize_scopes(token.scopes or [])


def require_scopes(*required_scopes: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Require that the current request token contains all required scopes.

    Raises ToolError if the request is unauthenticated or missing scopes.
    """
    required = _normalize_scopes(required_scopes)

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        if inspect.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                token_scopes = _get_token_scopes()
                if not token_scopes:
                    raise ToolError("Unauthorized: missing access token")
                if not required.issubset(token_scopes):
                    missing = ", ".join(sorted(required - token_scopes))
                    raise ToolError(f"Forbidden: missing required scopes ({missing})")
                return await func(*args, **kwargs)

            return async_wrapper

        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            token_scopes = _get_token_scopes()
            if not token_scopes:
                raise ToolError("Unauthorized: missing access token")
            if not required.issubset(token_scopes):
                missing = ", ".join(sorted(required - token_scopes))
                raise ToolError(f"Forbidden: missing required scopes ({missing})")
            return func(*args, **kwargs)

        return sync_wrapper

    return decorator


def require_any_scope(*required_scopes: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Require that the current request token contains at least one of the scopes.

    Raises ToolError if the request is unauthenticated or missing scopes.
    """
    required = _normalize_scopes(required_scopes)

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        if inspect.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                token_scopes = _get_token_scopes()
                if not token_scopes:
                    raise ToolError("Unauthorized: missing access token")
                if required and token_scopes.isdisjoint(required):
                    raise ToolError(
                        "Forbidden: missing any required scope "
                        f"({', '.join(sorted(required))})"
                    )
                return await func(*args, **kwargs)

            return async_wrapper

        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            token_scopes = _get_token_scopes()
            if not token_scopes:
                raise ToolError("Unauthorized: missing access token")
            if required and token_scopes.isdisjoint(required):
                raise ToolError(
                    "Forbidden: missing any required scope "
                    f"({', '.join(sorted(required))})"
                )
            return func(*args, **kwargs)

        return sync_wrapper

    return decorator
