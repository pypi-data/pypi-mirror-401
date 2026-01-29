"""
Request tracking middleware for ASGI frameworks (Starlette, FastAPI).

This module provides middleware that automatically generates and tracks
request IDs and session IDs, making them available throughout the request
lifecycle via context variables.

Usage with Starlette/FastAPI:
    from a2a_llm_tracker import TrackerMiddleware

    app = FastAPI()
    app.add_middleware(TrackerMiddleware)

    # Or with options:
    app.add_middleware(
        TrackerMiddleware,
        generate_request_id=True,
        generate_session_id=True,
        request_id_header="X-Request-ID",
        session_id_header="X-Session-ID",
    )

Access the IDs anywhere in your code:
    from a2a_llm_tracker import get_request_id, get_session_id

    request_id = get_request_id()
    session_id = get_session_id()
"""
from __future__ import annotations

import uuid
from contextvars import ContextVar
from typing import Callable, Optional
from ccs import LocalTransaction
# Context variables for request tracking - isolated per request
_request_id_var: ContextVar[str] = ContextVar("llm_tracker_request_id", default="")
_session_id_var: ContextVar[str] = ContextVar("llm_tracker_session_id", default="")


def get_request_id() -> str:
    """Get current request ID from context."""
    return _request_id_var.get()


def get_session_id() -> str:
    """Get current session ID from context."""
    return _session_id_var.get()


def set_request_id(request_id: str) -> None:
    """Set request ID in context."""
    _request_id_var.set(request_id)


def set_session_id(session_id: str) -> None:
    """Set session ID in context."""
    _session_id_var.set(session_id)


def generate_id() -> str:
    """Generate a new unique ID."""
    return str(uuid.uuid4())




    


# Try to import Starlette - it's optional
try:
    from starlette.middleware.base import BaseHTTPMiddleware
    from starlette.requests import Request
    from starlette.responses import Response

    class TrackerMiddleware(BaseHTTPMiddleware):
        """
        Middleware that tracks request and session IDs for LLM cost tracking.

        This middleware:
        1. Extracts or generates request/session IDs from headers
        2. Sets them in context variables (accessible via get_request_id/get_session_id)
        3. Also sets them in the tracker context (for automatic inclusion in analyze_response)
        4. Adds the IDs to response headers

        Args:
            app: The ASGI application
            generate_request_id: If True, generate request ID when not in header (default: True)
            generate_session_id: If True, generate session ID when not in header (default: True)
            request_id_header: Header name for request ID (default: "X-Request-ID")
            session_id_header: Header name for session ID (default: "X-Session-ID")
            id_generator: Custom ID generator function (default: uuid4)
        """

        def __init__(
            self,
            app,
            generate_request_id: bool = True,
            generate_session_id: bool = True,
            request_id_header: str = "X-Request-ID",
            session_id_header: str = "X-Session-ID",
            id_generator: Optional[Callable[[], str]] = None,
        ):
            super().__init__(app)
            self.generate_request_id = generate_request_id
            self.generate_session_id = generate_session_id
            self.request_id_header = request_id_header
            self.session_id_header = session_id_header
            self.id_generator = id_generator or generate_id

        async def dispatch(self, request: Request, call_next) -> Response:
            # Get or generate request ID
            request_id = request.headers.get(self.request_id_header, "")
            if not request_id and self.generate_request_id:
                request_id = self.id_generator()

            # Get or generate session ID
            session_id = request.headers.get(self.session_id_header, "")
            if not session_id and self.generate_session_id:
                session_id = self.id_generator()

            # Set in context variables
            if request_id:
                set_request_id(request_id)
            if session_id:
                set_session_id(session_id)

            # Also set in tracker context for automatic inclusion in analyze_response
            from .context import set_context
            set_context(trace_id=request_id, session_id=session_id)

            # Add to request state for easy access in route handlers
            request.state.request_id = request_id
            request.state.session_id = session_id

            # Process request
            response = await call_next(request)

            # Add IDs to response headers
            if request_id:
                response.headers[self.request_id_header] = request_id
            if session_id:
                response.headers[self.session_id_header] = session_id

            return response

    STARLETTE_AVAILABLE = True

except ImportError:
    STARLETTE_AVAILABLE = False
    TrackerMiddleware = None  # type: ignore


def require_starlette():
    """Raise ImportError if Starlette is not available."""
    if not STARLETTE_AVAILABLE:
        raise ImportError(
            "Starlette is required for TrackerMiddleware. "
            "Install it with: pip install starlette"
        )
