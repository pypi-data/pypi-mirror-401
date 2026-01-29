"""Django middleware for Monora trace context propagation.

This middleware automatically extracts W3C Trace Context headers from
incoming requests and injects them into outgoing responses.

Usage:
    # settings.py
    MIDDLEWARE = [
        'monora.middleware.django.MonoraDjangoMiddleware',
        # ... other middleware
    ]

    # Optional configuration in settings.py
    MONORA_MIDDLEWARE = {
        'skip_paths': ['/health', '/ready'],
        'span_name_func': lambda request: f"{request.method} {request.path}",
    }
"""
from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Set

from ..propagation import extract_context, inject_headers
from ..tracing import trace

try:
    from django.http import HttpRequest, HttpResponse
    from django.conf import settings
    DJANGO_AVAILABLE = True
except ImportError:
    DJANGO_AVAILABLE = False
    HttpRequest = Any  # type: ignore
    HttpResponse = Any  # type: ignore
    settings = None  # type: ignore


class MonoraDjangoMiddleware:
    """Django middleware that propagates W3C Trace Context.

    This middleware wraps Django applications and:
    1. Extracts trace context from incoming request headers
    2. Creates a trace span for the request
    3. Injects trace context into response headers

    Configuration via settings.MONORA_MIDDLEWARE:
        skip_paths: List of paths to skip (e.g., ['/health', '/ready'])
        span_name_func: Function (request) -> str for custom span names

    Example:
        # settings.py
        MIDDLEWARE = [
            'monora.middleware.django.MonoraDjangoMiddleware',
            # ... other middleware
        ]

        MONORA_MIDDLEWARE = {
            'skip_paths': ['/health', '/ready', '/metrics'],
        }
    """

    def __init__(self, get_response: Callable[[Any], Any]):
        """Initialize the middleware.

        Args:
            get_response: The next middleware or view in the chain.
        """
        if not DJANGO_AVAILABLE:
            raise ImportError(
                "Django is not installed. "
                "Install with: pip install django"
            )
        self.get_response = get_response

        # Load configuration from settings
        config = getattr(settings, 'MONORA_MIDDLEWARE', {})
        self.skip_paths: Set[str] = set(config.get('skip_paths', []))
        self.span_name_func: Callable[[Any], str] = (
            config.get('span_name_func') or self._default_span_name
        )

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Process the request with trace context.

        Args:
            request: The Django HTTP request.

        Returns:
            The HTTP response.
        """
        path = request.path

        # Skip specified paths
        if path in self.skip_paths:
            return self.get_response(request)

        # Extract headers from request
        headers = self._extract_headers(request)

        # Get span name
        span_name = self.span_name_func(request)

        # Extract trace context
        ctx = extract_context(headers)

        # Build trace options
        trace_kwargs: Dict[str, Any] = {}
        if ctx:
            trace_kwargs["trace_id"] = ctx.monora_trace_id or ctx.trace_id
            trace_kwargs["metadata"] = {"parent_span_id": ctx.parent_span_id}
            if ctx.monora_span_id:
                trace_kwargs["metadata"]["caller_span_id"] = ctx.monora_span_id

        # Execute request within trace context
        with trace(span_name, **trace_kwargs) as span:
            # Store span on request for access in views
            request.monora_span = span  # type: ignore
            request.monora_trace_id = span.trace_id  # type: ignore
            request.monora_span_id = span.span_id  # type: ignore

            response = self.get_response(request)

            # Inject trace context into response headers
            injected = inject_headers()
            for key, value in injected.items():
                response[key] = value

            return response

    def _extract_headers(self, request: HttpRequest) -> Dict[str, str]:
        """Extract HTTP headers from Django request.

        Args:
            request: The Django HTTP request.

        Returns:
            Dictionary of headers.
        """
        headers: Dict[str, str] = {}

        # Django stores headers in META with HTTP_ prefix
        for key, value in request.META.items():
            if key.startswith('HTTP_'):
                # Convert HTTP_HEADER_NAME to header-name
                header_name = key[5:].replace('_', '-').lower()
                headers[header_name] = value
            elif key in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
                # These don't have HTTP_ prefix
                header_name = key.replace('_', '-').lower()
                headers[header_name] = value

        return headers

    def _default_span_name(self, request: HttpRequest) -> str:
        """Generate default span name from request.

        Args:
            request: The Django HTTP request.

        Returns:
            Span name string.
        """
        method = request.method or 'GET'
        path = request.path
        return f"{method} {path}"


class MonoraDjangoAsyncMiddleware:
    """Async Django middleware that propagates W3C Trace Context.

    This is the async version of MonoraDjangoMiddleware for use with
    ASGI deployments and async views.

    Example:
        # settings.py (for async deployment)
        MIDDLEWARE = [
            'monora.middleware.django.MonoraDjangoAsyncMiddleware',
            # ... other middleware
        ]
    """

    sync_capable = False
    async_capable = True

    def __init__(self, get_response: Callable[[Any], Any]):
        """Initialize the async middleware.

        Args:
            get_response: The next middleware or view in the chain.
        """
        if not DJANGO_AVAILABLE:
            raise ImportError(
                "Django is not installed. "
                "Install with: pip install django"
            )
        self.get_response = get_response

        # Load configuration from settings
        config = getattr(settings, 'MONORA_MIDDLEWARE', {})
        self.skip_paths: Set[str] = set(config.get('skip_paths', []))
        self.span_name_func: Callable[[Any], str] = (
            config.get('span_name_func') or self._default_span_name
        )

    async def __call__(self, request: HttpRequest) -> HttpResponse:
        """Process the request with trace context.

        Args:
            request: The Django HTTP request.

        Returns:
            The HTTP response.
        """
        path = request.path

        # Skip specified paths
        if path in self.skip_paths:
            return await self.get_response(request)

        # Extract headers from request
        headers = self._extract_headers(request)

        # Get span name
        span_name = self.span_name_func(request)

        # Extract trace context
        ctx = extract_context(headers)

        # Build trace options
        trace_kwargs: Dict[str, Any] = {}
        if ctx:
            trace_kwargs["trace_id"] = ctx.monora_trace_id or ctx.trace_id
            trace_kwargs["metadata"] = {"parent_span_id": ctx.parent_span_id}
            if ctx.monora_span_id:
                trace_kwargs["metadata"]["caller_span_id"] = ctx.monora_span_id

        # Execute request within trace context
        with trace(span_name, **trace_kwargs) as span:
            # Store span on request for access in views
            request.monora_span = span  # type: ignore
            request.monora_trace_id = span.trace_id  # type: ignore
            request.monora_span_id = span.span_id  # type: ignore

            response = await self.get_response(request)

            # Inject trace context into response headers
            injected = inject_headers()
            for key, value in injected.items():
                response[key] = value

            return response

    def _extract_headers(self, request: HttpRequest) -> Dict[str, str]:
        """Extract HTTP headers from Django request."""
        headers: Dict[str, str] = {}
        for key, value in request.META.items():
            if key.startswith('HTTP_'):
                header_name = key[5:].replace('_', '-').lower()
                headers[header_name] = value
            elif key in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
                header_name = key.replace('_', '-').lower()
                headers[header_name] = value
        return headers

    def _default_span_name(self, request: HttpRequest) -> str:
        """Generate default span name from request."""
        method = request.method or 'GET'
        path = request.path
        return f"{method} {path}"


def monora_exception_handler(get_response: Callable[[Any], Any]):
    """Django middleware that logs exceptions to Monora.

    This middleware should be placed after MonoraDjangoMiddleware to
    capture and log any unhandled exceptions.

    Example:
        MIDDLEWARE = [
            'monora.middleware.django.MonoraDjangoMiddleware',
            'monora.middleware.django.monora_exception_handler',
            # ... other middleware
        ]
    """
    def middleware(request: HttpRequest) -> HttpResponse:
        try:
            return get_response(request)
        except Exception as exc:
            # Log error event if we have a span
            if hasattr(request, 'monora_span'):
                from ..api import log_event
                log_event('error', {
                    'error': {
                        'name': type(exc).__name__,
                        'message': str(exc),
                    },
                    'request': {
                        'method': request.method,
                        'path': request.path,
                    },
                })
            raise

    return middleware


def create_django_middleware(
    skip_paths: Optional[List[str]] = None,
    span_name_func: Optional[Callable[[Any], str]] = None,
) -> type:
    """Create a configured Django middleware class.

    This is useful when you want to configure the middleware without
    using Django settings.

    Args:
        skip_paths: Optional list of paths to skip.
        span_name_func: Optional custom span name function.

    Returns:
        Configured middleware class.

    Example:
        >>> from monora.middleware.django import create_django_middleware
        >>>
        >>> MonoraMiddleware = create_django_middleware(
        ...     skip_paths=['/health', '/ready']
        ... )
        >>>
        >>> # In settings.py, use the class directly or import from where defined
        >>> MIDDLEWARE = [MonoraMiddleware, ...]
    """
    class ConfiguredMiddleware(MonoraDjangoMiddleware):
        def __init__(self, get_response: Callable[[Any], Any]):
            if not DJANGO_AVAILABLE:
                raise ImportError(
                    "Django is not installed. "
                    "Install with: pip install django"
                )
            self.get_response = get_response
            self.skip_paths = set(skip_paths or [])
            self.span_name_func = span_name_func or self._default_span_name

    return ConfiguredMiddleware
