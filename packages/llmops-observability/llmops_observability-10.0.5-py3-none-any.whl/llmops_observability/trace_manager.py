"""
Trace Manager for LLMOps Observability
Handles tracing and tracking of LLM operations with direct Langfuse integration
Direct Langfuse integration with SQS event streaming
"""
from __future__ import annotations
import uuid
import threading
import time
import traceback
import functools
import inspect
import sys
import json
import logging
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List, Union
from .models import SpanContext, TraceConfig
from .config import get_langfuse_client
from .sqs import send_to_sqs, send_to_sqs_immediate, is_sqs_enabled

# Configure logger
logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[llmops_observability] %(levelname)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


# ============================================================
# Safe Serialization Helpers (from veriskGO)
# ============================================================

# Maximum size for serialized output (200 KB)
MAX_OUTPUT_SIZE = 200 * 1024  # 200 KB

def serialize_value(value: Any, max_size: int = MAX_OUTPUT_SIZE) -> Any:
    """Serialize value with size limit to prevent large data issues.
    
    Args:
        value: Value to serialize
        max_size: Maximum size in bytes (default 200 KB)
    
    Returns:
        Serialized value, truncated if necessary
    """
    try:
        # First, serialize to JSON
        serialized_str = json.dumps(value, default=str)
        serialized_bytes = serialized_str.encode('utf-8')
        
        # Check size
        if len(serialized_bytes) <= max_size:
            return json.loads(serialized_str)
        
        # Too large - return truncation info instead
        preview_size = min(1000, max_size // 2)  # Show first 1KB as preview
        preview = serialized_str[:preview_size]
        
        logger.warning(f"Output truncated: {len(serialized_bytes)} bytes → {max_size} bytes limit")
        
        return {
            "_truncated": True,
            "_original_size_bytes": len(serialized_bytes),
            "_original_size_mb": round(len(serialized_bytes) / (1024 * 1024), 2),
            "_preview": preview + "...",
            "_message": f"Output truncated (original: {round(len(serialized_bytes) / (1024 * 1024), 2)} MB, limit: {round(max_size / 1024, 0)} KB)"
        }
    except Exception as e:
        return str(value)


def safe_locals(d: Dict[str, Any]) -> Dict[str, Any]:
    """Safely serialize local variables"""
    return {k: serialize_value(v) for k, v in d.items() if not k.startswith("_")}


# ============================================================
# Core Trace Manager
# ============================================================

class TraceManager:
    _lock = threading.Lock()
    _active: Dict[str, Any] = {
        "trace_id": None,
        "trace_obj": None,  # Langfuse trace object reference
        "spans": [],
        "stack": [],  # Stack of active spans for nesting
        "metadata": {},
        "observation_stack": [],  # Stack of Langfuse observation contexts
    }
    # Buffer for spans created before trace is established
    _pending_spans: List[Dict[str, Any]] = []

    @classmethod
    def has_active_trace(cls) -> bool:
        """Check if there's an active trace"""
        return cls._active["trace_id"] is not None

    @classmethod
    def _id(cls) -> str:
        """Generate a unique ID compatible with Langfuse (32 lowercase hex chars)"""
        return uuid.uuid4().hex

    @classmethod
    def _now(cls) -> str:
        """Get current timestamp in ISO format"""
        return datetime.now(timezone.utc).isoformat()

    @classmethod
    def start_trace(
        cls,
        name: str,
        project_id: Optional[str] = None,
        environment: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> str:
        """
        Start a new trace with project and environment tracking.
        
        Args:
            name: Operation/trace name (e.g., "chat_message", "document_analysis")
            project_id: Project identifier (defaults to PROJECT_ID env var)
            environment: Environment name (defaults to ENV env var, e.g., "development", "production")
            metadata: Optional metadata dictionary
            user_id: Optional user ID
            session_id: Optional session ID
            tags: Optional list of tags
            
        Returns:
            str: Trace ID
            
        Example:
            TraceManager.start_trace(
                "chat_message",
                "my_project",
                "production",
                metadata={"user_id": "123", "session_id": "456"}
            )
        """
        # Validate operation name is provided and not empty
        if not name or not name.strip():
            logger.error("Cannot start trace: operation name is required and cannot be empty")
            raise ValueError("Operation name is required and cannot be empty")
        
        # Create trace configuration with auto-population from env vars
        trace_config = TraceConfig(
            name=name,
            project_id=project_id,
            environment=environment,
            user_id=user_id,
            session_id=session_id,
            metadata=metadata,
            tags=tags,
        )
        
        with cls._lock:
            if cls._active["trace_id"]:
                logger.warning("Trace already active. Ending previous trace.")
                cls._end_trace_internal()

            trace_id = cls._id()
            
            # Create Langfuse root span which creates a trace
            # In Langfuse, a trace is created automatically when you create a root observation
            langfuse = get_langfuse_client()
            
            # Create a root span with the operation name
            # This span will be the trace container
            root_span = langfuse.start_span(
                name=f"{trace_config.name}_root",  # Root span name
                input={
                    "operation": trace_config.name,
                    "project_id": trace_config.project_id,
                    "user_id": trace_config.user_id,
                    "session_id": trace_config.session_id,
                },
                metadata=trace_config.metadata,
            )
            
            # Update the trace metadata with project_id as the trace name
            # Set environment as a tag for proper tracking
            trace_tags = (trace_config.tags or []).copy()
            if trace_config.environment:
                trace_tags.append(trace_config.environment)
            
            root_span.update_trace(
                name=trace_config.trace_name,  # Use project_id as trace name
                user_id=trace_config.user_id,
                session_id=trace_config.session_id,
                tags=trace_tags,
                metadata=trace_config.metadata,
            )
            
            cls._active["trace_id"] = root_span.trace_id  # Use Langfuse's generated trace ID
            cls._active["trace_obj"] = root_span  # Store the root span object
            cls._active["trace_config"] = trace_config  # Store trace configuration
            cls._active["trace_info"] = {
                "name": trace_config.trace_name,  # Store project_id as trace name
                "operation": trace_config.name,  # Store operation name
                "project_id": trace_config.project_id,
                "environment": trace_config.environment,
                "user_id": trace_config.user_id,
                "session_id": trace_config.session_id,
                "metadata": trace_config.metadata,
                "tags": trace_config.tags or [],
                "trace_input": None,
                "trace_output": None,
            }
            cls._active["spans"] = []
            cls._active["stack"] = []  # Initialize stack for nested spans
            cls._active["observation_stack"] = []  # Initialize observation stack
            cls._active["metadata"] = metadata or {}
            
            # Attach any pending spans to this trace  
            if cls._pending_spans:
                logger.debug(f"Creating {len(cls._pending_spans)} held spans in trace '{trace_config.project_id}'")
                
                # Sort by start time to maintain order
                cls._pending_spans.sort(key=lambda x: x.get("start_time", datetime.now(timezone.utc)))
                
                for pending_span in cls._pending_spans:
                    try:
                        span_type = pending_span.get("type", "span")
                        span_name = pending_span["name"]
                        
                        # Create child observation using root span's methods
                        if span_type == "generation":
                            obs = root_span.start_generation(
                                name=span_name,
                                input=pending_span.get("input"),
                                output=pending_span.get("output"),
                                metadata=pending_span.get("metadata", {}),
                                level=pending_span.get("level", "DEFAULT"),
                                status_message=pending_span.get("status_message"),
                            )
                        else:
                            obs = root_span.start_span(
                                name=span_name,
                                input=pending_span.get("input"),
                                output=pending_span.get("output"),
                                metadata=pending_span.get("metadata", {}),
                                level=pending_span.get("level", "DEFAULT"),
                                status_message=pending_span.get("status_message"),
                            )
                        
                        # End the span immediately since it's already complete
                        obs.end()
                        
                        logger.debug(f"Created held span: {span_name}")
                    except Exception as e:
                        logger.warning(f"Failed to create held span {pending_span['name']}: {e}")
                
                # Clear the buffer
                cls._pending_spans.clear()
            
            logger.info(f"Trace started: {trace_config.trace_name} | Operation: {trace_config.name} | Env: {trace_config.environment} (ID: {trace_id})")
            
            # Send trace_start event to SQS (non-blocking)
            if is_sqs_enabled():
                trace_start_event = {
                    "event_type": "trace_start",
                    "trace_id": trace_id,
                    "trace_name": trace_config.trace_name,
                    "operation": trace_config.name,
                    "timestamp": cls._now(),
                    "metadata": {
                        "project_id": trace_config.project_id,
                        "environment": trace_config.environment,
                        "user_id": trace_config.user_id,
                        "session_id": trace_config.session_id,
                        **(trace_config.metadata or {})
                    }
                }
                send_to_sqs(trace_start_event)
                logger.debug(f"Trace start event sent to SQS: {trace_id}")
            
            return trace_id

    @classmethod
    def _end_trace_internal(cls):
        """Internal method to end trace without lock (already within lock context)"""
        trace_id = cls._active["trace_id"]
        trace_obj = cls._active.get("trace_obj")
        
        if trace_id:
            # End the root span if it exists
            if trace_obj and hasattr(trace_obj, "end"):
                trace_obj.end()
            
            # Flush to Langfuse immediately
            langfuse = get_langfuse_client()
            langfuse.flush()
            
            # Clear the active trace
            cls._active["trace_id"] = None
            cls._active["trace_obj"] = None
            cls._active["trace_info"] = None
            cls._active["spans"] = []
            cls._active["stack"] = []
            cls._active["metadata"] = {}
            cls._active["observation_stack"] = []

    @classmethod
    def end_trace(cls, final_output: Optional[Any] = None) -> Optional[str]:
        """
        End the current trace and flush to Langfuse.
        
        Args:
            final_output: Optional final output for the trace
            
        Returns:
            Optional[str]: Trace ID if successful
        """
        with cls._lock:
            trace_id = cls._active["trace_id"]
            trace_info = cls._active.get("trace_info", {})
            
            if not trace_id:
                return None
            
            # Validate that trace has a name before ending
            trace_name = trace_info.get("name", "").strip()
            if not trace_name:
                logger.warning("Ending trace without a name - trace may not be properly identified in Langfuse")
            
            if final_output and cls._active["trace_obj"]:
                # Update trace object with final output
                trace_obj = cls._active["trace_obj"]
                if hasattr(trace_obj, "update"):
                    trace_obj.update(output=final_output)
            
            cls._end_trace_internal()
            
            logger.info(f"Trace ended and flushed: {trace_id}")
            return trace_id

    @classmethod
    def finalize_and_send(
        cls,
        *,
        user_id: str,
        session_id: str,
        trace_name: str,
        trace_input: dict,
        trace_output: dict,
        extra_spans: list = [],
    ):
        """
        Finalize and send the trace with input/output (compatible with veriskGO API).
        
        This method provides compatibility with veriskGO's API by accepting
        trace_input and trace_output, then ending the trace.
        
        Args:
            user_id: User ID for the trace
            session_id: Session ID for the trace
            trace_name: Name of the trace
            trace_input: Input data for the trace
            trace_output: Output data for the trace
            extra_spans: Additional spans (not used in this implementation)
        
        Returns:
            bool: True if successful, False otherwise
        """
        # Validate trace name is provided and not empty
        if not trace_name or not trace_name.strip():
            logger.error("Cannot finalize trace: trace name is required and cannot be empty")
            return False
        
        with cls._lock:
            trace_id = cls._active.get("trace_id")
            trace_obj = cls._active.get("trace_obj")
            
            if not trace_id or not trace_obj:
                logger.error("No active trace to finalize.")
                return False
            
            # Update the root span with input/output using update_trace()
            trace_obj.update_trace(
                name=trace_name,
                user_id=user_id,
                session_id=session_id,
                input=serialize_value(trace_input),
                output=serialize_value(trace_output),
            )
        
        # Just flush - don't create new observations
        try:
            langfuse = get_langfuse_client()
            
            # Flush all observations to Langfuse
            langfuse.flush()
            
        except Exception as e:
            logger.error(f"Error sending trace to Langfuse: {e}")
            traceback.print_exc()
        
        # End the trace
        with cls._lock:
            cls._end_trace_internal()
        
        # Send trace_end event to SQS (immediate, critical message)
        if is_sqs_enabled():
            trace_end_event = {
                "event_type": "trace_end",
                "trace_id": trace_id,
                "user_id": user_id,
                "session_id": session_id,
                "trace_name": trace_name,
                "trace_input": serialize_value(trace_input),
                "trace_output": serialize_value(trace_output),
                "timestamp": cls._now(),
                "metadata": {
                    "project_id": cls._active.get("trace_config", {}).project_id if cls._active.get("trace_config") else "unknown"
                }
            }
            send_to_sqs_immediate(trace_end_event)
            logger.debug(f"Trace end event sent to SQS: {trace_id}")
        
        logger.info(f"Trace finalized and sent: {trace_name} (ID: {trace_id})")
        return True


    @classmethod
    def start_observation_context(cls, span_name: str, span_type: str, input_data: Any):
        """
        Start a Langfuse observation context that will be the parent for nested calls.
        
        Args:
            span_name: Name of the span
            span_type: Type ("span" or "generation")
            input_data: Input data for the span
            
        Returns:
            observation context manager
        """
        with cls._lock:
            trace_id = cls._active.get("trace_id")
            trace_obj = cls._active.get("trace_obj")
            current_obs_stack = cls._active.get("observation_stack", [])
            
            if not trace_id or not trace_obj:
                return None
        
        langfuse = get_langfuse_client()
        
        # Serialize input
        serialized_input = serialize_value(input_data)
        
        # Check if we have a parent observation
        parent_obs = current_obs_stack[-1] if current_obs_stack else None
        
        # Start observation context from parent or from root span
        if parent_obs:
            # Create child observation from parent
            if span_type == "generation":
                obs_ctx = parent_obs.start_as_current_observation(
                    as_type="generation",
                    name=span_name,
                    input=serialized_input,
                )
            else:
                obs_ctx = parent_obs.start_as_current_observation(
                    as_type="span",
                    name=span_name,
                    input=serialized_input,
                )
        else:
            # Create root observation - attach to root span (trace container)
            if span_type == "generation":
                obs_ctx = trace_obj.start_as_current_generation(
                    name=span_name,
                    input=serialized_input,
                )
            else:
                obs_ctx = trace_obj.start_as_current_span(
                    name=span_name,
                    input=serialized_input,
                )
        
        return obs_ctx
    
    @classmethod
    def push_observation(cls, obs):
        """Push an observation onto the stack when entering its context"""
        with cls._lock:
            cls._active["observation_stack"].append(obs)
    
    @classmethod
    def pop_observation(cls):
        """Pop an observation from the stack when exiting its context"""
        with cls._lock:
            if cls._active["observation_stack"]:
                cls._active["observation_stack"].pop()
    
    @classmethod
    def get_trace_context_metadata(cls) -> Dict[str, Any]:
        """Get metadata with PROJECT_ID and ENV from active trace config.
        
        Returns:
            Dict with project_id and environment if trace is active, empty dict otherwise
        """
        with cls._lock:
            trace_config = cls._active.get("trace_config")
            if trace_config:
                return {
                    "project_id": trace_config.project_id,
                    "environment": trace_config.environment,
                }
            return {}


# ============================================================
# Local Capture Utilities (from veriskGO)
# ============================================================

def capture_function_locals(func, capture_locals: Union[bool, List[str]] = True, capture_self: bool = True):
    """
    Capture local variables before and after function execution.
    Uses sys.settrace for frame inspection (similar to veriskGO).
    
    Args:
        func: Function to capture locals from
        capture_locals: Whether to capture locals (True, False, or list of var names)
        capture_self: Whether to capture 'self' variable
    
    Returns:
        Tuple of (tracer, locals_before, locals_after)
    """
    locals_before = {}
    locals_after = {}

    if not capture_locals:
        return None, locals_before, locals_after

    target_code = func.__code__
    target_name = func.__name__
    target_module = func.__module__

    entered = False

    def tracer(frame, event, arg):
        nonlocal entered

        if frame.f_code is target_code and frame.f_globals.get("__name__") == target_module:
            try:
                if not entered:
                    entered = True
                    f_locals = frame.f_locals
                    
                    # Filter specific variables if capture_locals is a list
                    if isinstance(capture_locals, list):
                        f_locals = {k: v for k, v in f_locals.items() if k in capture_locals}

                    if not capture_self and "self" in f_locals:
                        f_locals = {k: v for k, v in f_locals.items() if k != "self"}
                    locals_before.update(safe_locals(f_locals))

                if event == "return":
                    f_locals = frame.f_locals
                    
                    # Filter specific variables if capture_locals is a list
                    if isinstance(capture_locals, list):
                        f_locals = {k: v for k, v in f_locals.items() if k in capture_locals}
                    
                    if not capture_self and "self" in f_locals:
                        f_locals = {k: v for k, v in f_locals.items() if k != "self"}
                    locals_after.update(safe_locals(f_locals))
                    locals_after["_return"] = serialize_value(arg)
            except Exception as e:
                logger.error(f"Tracer error: {e}")
                traceback.print_exc()

        return tracer

    return tracer, locals_before, locals_after


# ============================================================
# Decorator: track_function (Enhanced with veriskGO features)
# ============================================================

def track_function(
    name: Optional[str] = None,
    *,
    metadata: Optional[Dict[str, Any]] = None,
    capture_locals: Union[bool, List[str]] = False,
    capture_self: bool = False,
):
    """
    Decorator to track function execution with Langfuse (enhanced version from veriskGO).
    
    Features:
    - Captures input arguments and output
    - Optionally captures local variables before/after execution
    - Manages span stack for proper nesting
    - Sends directly to Langfuse (no batching)
    
    Usage:
        @track_function()
        def process_data(input_data):
            # Your code here
            return result
            
        @track_function(name="custom_name", metadata={"version": "1.0"}, capture_locals=True)
        def detailed_function(x, y):
            result = x + y
            return result
            
        @track_function(capture_locals=["important_var"])
        async def async_function():
            important_var = "tracked"
            return result
    
    Args:
        name: Optional custom name for the span
        metadata: Optional metadata tags
        capture_locals: Capture local variables (True/False or list of var names)
        capture_self: Whether to capture 'self' variable (default False)
    """
    def decorator(func):
        span_name = name or func.__name__
        is_async = inspect.iscoroutinefunction(func)
        
        if is_async:
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                # If no active trace, buffer this span for later attachment
                if not TraceManager.has_active_trace():
                    # Execute function and collect data
                    start_time = datetime.now(timezone.utc)
                    error = None
                    result = None
                    
                    try:
                        result = await func(*args, **kwargs)
                    except Exception as e:
                        error = e
                        raise
                    finally:
                        end_time = datetime.now(timezone.utc)
                        
                        # Buffer the span data
                        span_data = {
                            "name": span_name,
                            "type": "span",
                            "start_time": start_time,
                            "end_time": end_time,
                            "input": {
                                "args": serialize_value(args),
                                "kwargs": serialize_value(kwargs),
                            },
                            "output": {
                                "status": "error" if error else "success",
                                "output": serialize_value(result) if not error else None,
                            },
                            "metadata": metadata or {},
                            "level": "ERROR" if error else "DEFAULT",
                            "status_message": str(error) if error else None,
                        }
                        
                        TraceManager._pending_spans.append(span_data)
                        duration_ms = int((end_time - start_time).total_seconds() * 1000)
                        logger.debug(f"Span buffered (no trace): {span_name} ({duration_ms}ms)")
                    
                    return result

                # Build input data
                input_data = {
                    "args": serialize_value(args),
                    "kwargs": serialize_value(kwargs),
                }

                # Start observation context (this will be parent for nested calls)
                obs_ctx = TraceManager.start_observation_context(span_name, "span", input_data)
                
                if not obs_ctx:
                    return await func(*args, **kwargs)

                # Setup local variable capture
                tracer, locals_before, locals_after = capture_function_locals(
                    func, capture_locals=capture_locals, capture_self=capture_self
                )
                
                error = None
                result = None
                start_time = time.time()
                
                # Use the observation context properly with 'with' statement
                # This keeps the context active during function execution
                with obs_ctx as obs:
                    # Push observation onto stack so nested calls become children
                    TraceManager.push_observation(obs)
                    
                    if tracer:
                        sys.settrace(tracer)
                    
                    try:
                        result = await func(*args, **kwargs)
                    except Exception as e:
                        error = e
                        raise
                    finally:
                        if tracer:
                            sys.settrace(None)
                        
                        duration_ms = int((time.time() - start_time) * 1000)
                        
                        # Build output
                        if error:
                            output_data = {
                                "status": "error",
                                "error": str(error),
                                "stacktrace": traceback.format_exc(),
                                "locals_before": locals_before,
                                "locals_after": locals_after,
                            }
                        else:
                            output_data = {
                                "status": "success",
                                "latency_ms": duration_ms,
                                "locals_before": locals_before,
                                "locals_after": locals_after,
                                "output": serialize_value(result),
                            }
                        
                        # Inject trace context metadata (PROJECT_ID and ENV)
                        span_metadata = metadata or {}
                        trace_context = TraceManager.get_trace_context_metadata()
                        span_metadata.update(trace_context)
                        
                        # Update observation with output
                        obs.update(
                            output=serialize_value(output_data),
                            metadata=span_metadata,
                            level="ERROR" if error else "DEFAULT",
                            status_message=str(error) if error else None,
                        )
                        
                        # Send span event to SQS (non-blocking, independent of Langfuse)
                        if is_sqs_enabled() and TraceManager.has_active_trace():
                            trace_id = TraceManager._active.get("trace_id")
                            if trace_id:
                                span_event = {
                                    "event_type": "span",
                                    "trace_id": trace_id,
                                    "span_id": obs.id if hasattr(obs, 'id') else "unknown",
                                    "parent_span_id": None,  # Will be updated by decorator context
                                    "name": span_name,
                                    "timestamp": TraceManager._now(),
                                    "duration_ms": duration_ms,
                                    "input": input_data,
                                    "output": output_data,
                                    "metadata": span_metadata
                                }
                                send_to_sqs(span_event)
                                logger.debug(f"Span event sent to SQS: {span_name}")
                        
                        # Note: flush happens after context exit
                
                # Flush after exiting context
                langfuse = get_langfuse_client()
                langfuse.flush()
                
                status_str = " (error)" if error else ""
                logger.debug(f"Span sent{status_str}: {span_name} ({duration_ms}ms)")
                
                return result
            
            return async_wrapper
        else:
            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                # If no active trace, buffer this span for later attachment
                if not TraceManager.has_active_trace():
                    # Execute function and collect data
                    start_time = datetime.now(timezone.utc)
                    error = None
                    result = None
                    
                    try:
                        result = func(*args, **kwargs)
                    except Exception as e:
                        error = e
                        raise
                    finally:
                        end_time = datetime.now(timezone.utc)
                        
                        # Buffer the span data
                        span_data = {
                            "name": span_name,
                            "type": "span",
                            "start_time": start_time,
                            "end_time": end_time,
                            "input": {
                                "args": serialize_value(args),
                                "kwargs": serialize_value(kwargs),
                            },
                            "output": {
                                "status": "error" if error else "success",
                                "output": serialize_value(result) if not error else None,
                            },
                            "metadata": metadata or {},
                            "level": "ERROR" if error else "DEFAULT",
                            "status_message": str(error) if error else None,
                        }
                        
                        TraceManager._pending_spans.append(span_data)
                        duration_ms = int((end_time - start_time).total_seconds() * 1000)
                        logger.debug(f"Span buffered (no trace): {span_name} ({duration_ms}ms)")
                    
                    return result

                # Build input data
                input_data = {
                    "args": serialize_value(args),
                    "kwargs": serialize_value(kwargs),
                }

                # Start observation context (this will be parent for nested calls)
                obs_ctx = TraceManager.start_observation_context(span_name, "span", input_data)
                
                if not obs_ctx:
                    return func(*args, **kwargs)

                # Setup local variable capture
                tracer, locals_before, locals_after = capture_function_locals(
                    func, capture_locals=capture_locals, capture_self=capture_self
                )
                
                error = None
                result = None
                start_time = time.time()
                
                # Use the observation context properly with 'with' statement
                # This keeps the context active during function execution
                with obs_ctx as obs:
                    # Push observation onto stack so nested calls become children
                    TraceManager.push_observation(obs)
                    
                    if tracer:
                        sys.settrace(tracer)
                    
                    try:
                        result = func(*args, **kwargs)
                    except Exception as e:
                        error = e
                        raise
                    finally:
                        # Pop observation from stack
                        TraceManager.pop_observation()
                        
                        if tracer:
                            sys.settrace(None)
                        
                        duration_ms = int((time.time() - start_time) * 1000)
                        
                        # Build output
                        if error:
                            output_data = {
                                "status": "error",
                                "error": str(error),
                                "stacktrace": traceback.format_exc(),
                                "locals_before": locals_before,
                                "locals_after": locals_after,
                            }
                        else:
                            output_data = {
                                "status": "success",
                                "latency_ms": duration_ms,
                                "locals_before": locals_before,
                                "locals_after": locals_after,
                                "output": serialize_value(result),
                            }
                        
                        # Inject trace context metadata (PROJECT_ID and ENV)
                        span_metadata = metadata or {}
                        trace_context = TraceManager.get_trace_context_metadata()
                        span_metadata.update(trace_context)
                        
                        # Update observation with output
                        obs.update(
                            output=serialize_value(output_data),
                            metadata=span_metadata,
                            level="ERROR" if error else "DEFAULT",
                            status_message=str(error) if error else None,
                        )
                
                # Flush after exiting context
                langfuse = get_langfuse_client()
                langfuse.flush()
                
                status_str = " (error)" if error else ""
                logger.debug(f"Span sent{status_str}: {span_name} ({duration_ms}ms)")
                
                return result
            
            return sync_wrapper
    
    return decorator

