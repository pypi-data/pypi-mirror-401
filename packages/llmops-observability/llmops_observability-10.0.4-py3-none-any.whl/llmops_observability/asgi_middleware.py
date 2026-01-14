"""
ASGI Middleware for LLMOps Observability
Automatic tracing for FastAPI and other ASGI applications
Based on veriskGO's asgi_middleware with direct Langfuse integration
"""
import uuid
import time
import os
import socket
from .trace_manager import TraceManager


class LLMOpsASGIMiddleware:
    """
    ASGI middleware for automatic tracing of HTTP requests.
    
    Usage with FastAPI:
        from fastapi import FastAPI
        from llmops_observability.asgi_middleware import LLMOpsASGIMiddleware
        
        app = FastAPI()
        app.add_middleware(LLMOpsASGIMiddleware, service_name="my_api")
        
        @app.get("/")
        async def root():
            return {"message": "Hello World"}
    """

    def __init__(self, app, service_name="llmops_service"):
        """
        Initialize the ASGI middleware.
        
        Args:
            app: ASGI application instance
            service_name: Name of the service (used in trace naming)
        """
        self.app = app
        self.service_name = service_name

    def get_trace_name(self):
        """
        Generate a trace name based on project and hostname.
        
        Returns:
            str: Trace name in format "project_hostname"
        """
        project = os.path.basename(os.getcwd())
        hostname = socket.gethostname()
        return f"{project}_{hostname}"

    async def __call__(self, scope, receive, send):
        """
        ASGI middleware entry point.
        
        Args:
            scope: ASGI scope dictionary
            receive: ASGI receive callable
            send: ASGI send callable
        """
        # We only trace HTTP traffic
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        method = scope.get("method", "UNKNOWN")
        path = scope.get("path", "UNKNOWN")

        # Extract headers (optional user/session identification)
        headers = {k.decode(): v.decode() for k, v in scope.get("headers", [])}
        user_id = headers.get("x-user-id", "anonymous")
        session_id = headers.get("x-session-id", str(uuid.uuid4()))
        
        # Generate trace name
        trace_name = self.get_trace_name()

        # Start trace with metadata
        TraceManager.start_trace(
            trace_name,
            metadata={
                "path": path,
                "method": method,
                "user_id": user_id,
                "session_id": session_id,
                "service": self.service_name,
            },
            user_id=user_id,
            session_id=session_id,
        )

        start_time = time.time()
        response_body = None
        status_code = None

        async def send_wrapper(message):
            """Wrapper to capture response data"""
            nonlocal response_body, status_code

            # Capture response status
            if message["type"] == "http.response.start":
                status_code = message.get("status")

            # Capture response body
            if message["type"] == "http.response.body":
                body = message.get("body")
                try:
                    response_body = body.decode() if body else None
                except Exception:
                    response_body = str(body) if body else None

            await send(message)

        try:
            # Execute the application
            await self.app(scope, receive, send_wrapper)
        except Exception as exc:
            # Trace the exception
            TraceManager.finalize_and_send(
                user_id=user_id,
                session_id=session_id,
                trace_name=f"{trace_name}_error",
                trace_input={"path": path, "method": method},
                trace_output={
                    "error": str(exc),
                    "error_type": type(exc).__name__,
                },
            )
            raise

        # Normal completion - finalize trace with input/output
        latency_ms = int((time.time() - start_time) * 1000)
        
        TraceManager.finalize_and_send(
            user_id=user_id,
            session_id=session_id,
            trace_name=trace_name,
            trace_input={
                "path": path,
                "method": method,
                "headers": dict(headers),  # Include all headers
            },
            trace_output={
                "status_code": status_code,
                "response": response_body,
                "latency_ms": latency_ms,
            },
        )
