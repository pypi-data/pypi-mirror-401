"""
LLM tracking decorator for LLMOps Observability
Direct Langfuse integration for tracking LLM calls
Enhanced with robust input/output handling and SQS event streaming
"""
from __future__ import annotations
import functools
import inspect
import sys
import time
import traceback
from typing import Optional, Dict, Any, List, Union
from .trace_manager import TraceManager
from .sqs import send_to_sqs, is_sqs_enabled


def extract_text(resp: Any) -> str:
    """
    Extract text from various LLM response formats.
    Supports: Bedrock Converse, Bedrock InvokeModel, OpenAI, LangChain, etc.
    """
    if isinstance(resp, str):
        return resp

    if not isinstance(resp, dict):
        return str(resp)

    # Bedrock Converse API
    try:
        return resp["output"]["message"]["content"][0]["text"]
    except (KeyError, IndexError, TypeError):
        pass

    # Anthropic Messages API
    try:
        return resp["content"][0]["text"]
    except (KeyError, IndexError, TypeError):
        pass

    # Amazon Titan
    try:
        return resp["results"][0]["outputText"]
    except (KeyError, IndexError, TypeError):
        pass

    # Cohere
    try:
        return resp["generation"]
    except (KeyError, TypeError):
        pass

    # AI21
    try:
        return resp["outputs"][0]["text"]
    except (KeyError, IndexError, TypeError):
        pass

    # Generic text field
    try:
        return resp["text"]
    except (KeyError, TypeError):
        pass

    # OpenAI format
    try:
        return resp["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        pass

    return str(resp)


def extract_usage(result: Any, kwargs: Dict[str, Any]) -> Optional[Dict[str, int]]:
    """
    Extract token usage from LLM response or callback.
    
    Returns:
        Dict with input_tokens, output_tokens, total_tokens or None
    """
    usage = {}
    
    # Check if result has usage attribute (OpenAI, Anthropic direct)
    if hasattr(result, 'usage'):
        usage_obj = result.usage
        if hasattr(usage_obj, 'prompt_tokens'):
            usage['input_tokens'] = usage_obj.prompt_tokens
        if hasattr(usage_obj, 'completion_tokens'):
            usage['output_tokens'] = usage_obj.completion_tokens
        if hasattr(usage_obj, 'total_tokens'):
            usage['total_tokens'] = usage_obj.total_tokens
        return usage if usage else None
    
    # Check Bedrock response format
    if isinstance(result, dict):
        # Bedrock Converse API
        if 'usage' in result:
            usage_data = result['usage']
            if 'inputTokens' in usage_data:
                usage['input_tokens'] = usage_data['inputTokens']
            if 'outputTokens' in usage_data:
                usage['output_tokens'] = usage_data['outputTokens']
            if 'totalTokens' in usage_data:
                usage['total_tokens'] = usage_data['totalTokens']
            return usage if usage else None
    
    # Check for LangChain callbacks in kwargs
    config = kwargs.get('config', {})
    callbacks = config.get('callbacks', [])
    for callback in callbacks:
        # Bedrock Anthropic callback
        if hasattr(callback, 'prompt_tokens'):
            usage['input_tokens'] = callback.prompt_tokens
        if hasattr(callback, 'completion_tokens'):
            usage['output_tokens'] = callback.completion_tokens
        if hasattr(callback, 'total_tokens'):
            usage['total_tokens'] = callback.total_tokens
        if usage:
            return usage
    
    return None


def extract_model_info(args: tuple, kwargs: Dict[str, Any]) -> Optional[str]:
    """
    Extract model name from function arguments.
    
    Returns:
        Model name string or None
    """
    # Check kwargs for common model parameter names
    for key in ['model', 'model_id', 'model_name', 'modelId']:
        if key in kwargs:
            return str(kwargs[key])
    
    # Check if first arg has model attribute (LangChain model objects)
    if args:
        first_arg = args[0]
        if hasattr(first_arg, 'model'):
            return str(first_arg.model)
        if hasattr(first_arg, 'model_id'):
            return str(first_arg.model_id)
        if hasattr(first_arg, 'model_name'):
            return str(first_arg.model_name)
    
    return None


def track_llm_call(
    name: Optional[str] = None,
    *,
    metadata: Optional[Dict[str, Any]] = None,
    extract_output: bool = True,
    model: Optional[str] = None,  # Allow specifying model explicitly
    capture_locals: Union[bool, List[str]] = False,
    capture_self: bool = False,
):
    """
    Decorator to track LLM calls with Langfuse as generations.
    
    Enhanced version inspired by veriskGO with proper input/output handling.
    
    Args:
        name: Custom name for the generation (defaults to function name)
        metadata: Metadata tags to attach to the generation
        extract_output: Whether to extract text from LLM response (default True)
        model: Model ID for cost calculation (e.g., "anthropic.claude-3-sonnet-20240229-v1:0")
        capture_locals: Capture local variables (True/False or list of var names)
        capture_self: Whether to capture 'self' variable (default False)
    
    Usage:
        @track_llm_call()
        def call_bedrock(prompt):
            response = bedrock.converse(...)
            return response
            
        @track_llm_call(name="summarize", metadata={"model": "claude-3"})
        async def summarize(text):
            return await chain.ainvoke(...)
    
    Args:
        name: Optional custom name for the generation
        metadata: Optional metadata tags
        extract_output: Whether to extract text from LLM response
    """
    def decorator(func):
        span_name = name or func.__name__
        is_async = inspect.iscoroutinefunction(func)
        
        if is_async:
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                if not TraceManager.has_active_trace():
                    return await func(*args, **kwargs)

                # Setup local variable capture
                from .trace_manager import capture_function_locals, serialize_value as tm_serialize
                tracer, locals_before, locals_after = capture_function_locals(
                    func, capture_locals=capture_locals, capture_self=capture_self
                )

                # Extract callback BEFORE execution for post-execution token reading
                bedrock_callback = None
                config = kwargs.get('config', {})
                callbacks = config.get('callbacks', [])
                for cb in callbacks:
                    # Check if it's a Bedrock token usage callback
                    if hasattr(cb, 'prompt_tokens') and hasattr(cb, 'completion_tokens'):
                        bedrock_callback = cb
                        break

                # Build input - extract prompt if first arg is string
                if args and isinstance(args[0], str):
                    input_data = {
                        "prompt": args[0],
                        "args": args[1:],
                        "kwargs": kwargs,
                    }
                else:
                    input_data = {
                        "args": args,
                        "kwargs": kwargs,
                    }

                # Start observation context (this will be parent for nested calls)
                obs_ctx = TraceManager.start_observation_context(span_name, "generation", input_data)
                
                if not obs_ctx:
                    return await func(*args, **kwargs)

                error = None
                result = None
                start_time = time.time()
                
                # Use the observation context properly with 'with' statement
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
                        
                        # Pop observation from stack
                        TraceManager.pop_observation()
                        duration_ms = int((time.time() - start_time) * 1000)
                        
                        # Extract model info - use decorator param if provided
                        model_name = model or extract_model_info(args, kwargs)
                        
                        # Extract token usage - Try BOTH callback AND response
                        usage_info = None
                        total_cost = None
                        
                        # First, try callback (for LangChain with BedrockAnthropicTokenUsageCallbackHandler)
                        if bedrock_callback:
                            if hasattr(bedrock_callback, 'total_tokens') and bedrock_callback.total_tokens > 0:
                                usage_info = {
                                    "input_tokens": getattr(bedrock_callback, 'prompt_tokens', 0),
                                    "output_tokens": getattr(bedrock_callback, 'completion_tokens', 0),
                                    "total_tokens": getattr(bedrock_callback, 'total_tokens', 0)
                                }
                                
                                # Get cost from callback if available
                                if hasattr(bedrock_callback, 'total_cost'):
                                    total_cost = getattr(bedrock_callback, 'total_cost', 0)
                        
                        # Also try extracting from response (works for direct Bedrock calls)
                        if result and not error:
                            response_usage = extract_usage(result, kwargs)
                            if response_usage:
                                # Use response usage if no callback usage
                                if not usage_info:
                                    usage_info = response_usage
                        
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
                            # Extract text from response if enabled
                            if extract_output:
                                try:
                                    text_output = extract_text(result)
                                    output_data = {
                                        "status": "success",
                                        "text": text_output,
                                        "raw": result,
                                        "locals_before": locals_before,
                                        "locals_after": locals_after,
                                    }
                                except Exception:
                                    output_data = {
                                        "status": "success",
                                        "raw": result,
                                        "locals_before": locals_before,
                                        "locals_after": locals_after,
                                    }
                            else:
                                output_data = {
                                    "status": "success",
                                    "raw": result,
                                    "locals_before": locals_before,
                                    "locals_after": locals_after,
                                }
                        
                        # Update observation with output, usage, and model
                        from .trace_manager import serialize_value
                        from .config import get_langfuse_client
                        
                        # Build base update params
                        update_params = {
                            "output": serialize_value(output_data),
                            "metadata": metadata or {},
                            "level": "ERROR" if error else "DEFAULT",
                            "status_message": str(error) if error else None,
                        }
                        
                        # Inject trace context metadata (PROJECT_ID and ENV)
                        trace_context = TraceManager.get_trace_context_metadata()
                        update_params["metadata"].update(trace_context)
                        
                        # Add model info if available
                        if model_name:
                            update_params["model"] = model_name
                        
                        # Add usage info using Langfuse's usage_details parameter
                        if usage_info:
                            # Langfuse expects usage_details with input/output/total keys
                            update_params["usage_details"] = {
                                "input": usage_info.get("input_tokens", 0),
                                "output": usage_info.get("output_tokens", 0),
                                "total": usage_info.get("total_tokens", 0),
                            }
                            
                            # Calculate cost based on model and tokens
                            from .pricing import calculate_cost
                            
                            # Always calculate cost breakdown from tokens and model
                            cost_dict = calculate_cost(
                                input_tokens=usage_info.get("input_tokens", 0),
                                output_tokens=usage_info.get("output_tokens", 0),
                                model_id=model_name
                            )
                            
                            # Use callback cost if available, otherwise use calculated
                            if total_cost is None or total_cost == 0:
                                total_cost = cost_dict["total"]
                            
                            # Add cost_details if available
                            if total_cost is not None and total_cost > 0:
                                cost_details_value = {
                                    "input": cost_dict["input"],
                                    "output": cost_dict["output"],
                                    "total": total_cost,
                                }
                                update_params["cost_details"] = cost_details_value
                        
                        # Use Langfuse's update_current_generation() instead of obs.update()
                        langfuse = get_langfuse_client()
                        langfuse.update_current_generation(**update_params)
                
                # Flush after exiting context
                from .config import get_langfuse_client
                langfuse = get_langfuse_client()
                langfuse.flush()
                
                status_str = " (error)" if error else ""
                usage_str = f" [{usage_info.get('total_tokens', 0)} tokens]" if usage_info else ""
                print(f"[LLMOps-Observability] Generation sent{status_str}: {span_name} ({duration_ms}ms){usage_str}")
                
                return result
            
            return async_wrapper
        else:
            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                if not TraceManager.has_active_trace():
                    return func(*args, **kwargs)

                # Setup local variable capture
                from .trace_manager import capture_function_locals, serialize_value as tm_serialize
                tracer, locals_before, locals_after = capture_function_locals(
                    func, capture_locals=capture_locals, capture_self=capture_self
                )

                # Extract callback BEFORE execution for post-execution token reading
                bedrock_callback = None
                config = kwargs.get('config', {})
                callbacks = config.get('callbacks', [])
                for cb in callbacks:
                    # Check if it's a Bedrock token usage callback
                    if hasattr(cb, 'prompt_tokens') and hasattr(cb, 'completion_tokens'):
                        bedrock_callback = cb
                        break

                # Build input - extract prompt if first arg is string
                if args and isinstance(args[0], str):
                    input_data = {
                        "prompt": args[0],
                        "args": args[1:],
                        "kwargs": kwargs,
                    }
                else:
                    input_data = {
                        "args": args,
                        "kwargs": kwargs,
                    }

                # Start observation context (this will be parent for nested calls)
                obs_ctx = TraceManager.start_observation_context(span_name, "generation", input_data)
                
                if not obs_ctx:
                    return func(*args, **kwargs)

                error = None
                result = None
                start_time = time.time()
                
                # Use the observation context properly with 'with' statement
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
                        if tracer:
                            sys.settrace(None)
                        
                        # Pop observation from stack
                        TraceManager.pop_observation()
                        
                        duration_ms = int((time.time() - start_time) * 1000)
                        
                        # Extract model info - use decorator param if provided
                        model_name = model or extract_model_info(args, kwargs)
                        
                        # Extract token usage - Try BOTH callback AND response
                        usage_info = None
                        total_cost = None
                        
                        # First, try callback (for LangChain with BedrockAnthropicTokenUsageCallbackHandler)
                        if bedrock_callback:
                            if hasattr(bedrock_callback, 'total_tokens') and bedrock_callback.total_tokens > 0:
                                usage_info = {
                                    "input_tokens": getattr(bedrock_callback, 'prompt_tokens', 0),
                                    "output_tokens": getattr(bedrock_callback, 'completion_tokens', 0),
                                    "total_tokens": getattr(bedrock_callback, 'total_tokens', 0)
                                }
                                
                                # Get cost from callback if available
                                if hasattr(bedrock_callback, 'total_cost'):
                                    total_cost = getattr(bedrock_callback, 'total_cost', 0)
                        
                        # Also try extracting from response (works for direct Bedrock calls)
                        if result and not error:
                            response_usage = extract_usage(result, kwargs)
                            if response_usage:
                                # Use response usage if no callback usage
                                if not usage_info:
                                    usage_info = response_usage
                        
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
                            # Extract text from response if enabled
                            if extract_output:
                                try:
                                    text_output = extract_text(result)
                                    output_data = {
                                        "status": "success",
                                        "text": text_output,
                                        "raw": result,
                                        "locals_before": locals_before,
                                        "locals_after": locals_after,
                                    }
                                except Exception:
                                    output_data = {
                                        "status": "success",
                                        "raw": result,
                                        "locals_before": locals_before,
                                        "locals_after": locals_after,
                                    }
                            else:
                                output_data = {
                                    "status": "success",
                                    "raw": result,
                                    "locals_before": locals_before,
                                    "locals_after": locals_after,
                                }
                        
                        # Update observation with output, usage, and model
                        from .trace_manager import serialize_value
                        from .config import get_langfuse_client
                        
                        # Build base update params
                        update_params = {
                            "output": serialize_value(output_data),
                            "metadata": metadata or {},
                            "level": "ERROR" if error else "DEFAULT",
                            "status_message": str(error) if error else None,
                        }
                        
                        # Inject trace context metadata (PROJECT_ID and ENV)
                        trace_context = TraceManager.get_trace_context_metadata()
                        update_params["metadata"].update(trace_context)
                        
                        # Add model info if available
                        if model_name:
                            update_params["model"] = model_name
                        
                        # Add usage info using Langfuse's usage_details parameter
                        if usage_info:
                            # Langfuse expects usage_details with input/output/total keys
                            update_params["usage_details"] = {
                                "input": usage_info.get("input_tokens", 0),
                                "output": usage_info.get("output_tokens", 0),
                                "total": usage_info.get("total_tokens", 0),
                            }
                            
                            # Calculate cost based on model and tokens
                            from .pricing import calculate_cost
                            
                            # Always calculate cost breakdown from tokens and model
                            cost_dict = calculate_cost(
                                input_tokens=usage_info.get("input_tokens", 0),
                                output_tokens=usage_info.get("output_tokens", 0),
                                model_id=model_name
                            )
                            
                            # Use callback cost if available, otherwise use calculated
                            if total_cost is None or total_cost == 0:
                                total_cost = cost_dict["total"]
                            
                            # Add cost_details if available
                            if total_cost is not None and total_cost > 0:
                                cost_details_value = {
                                    "input": cost_dict["input"],
                                    "output": cost_dict["output"],
                                    "total": total_cost,
                                }
                                update_params["cost_details"] = cost_details_value
                        
                        # Use Langfuse's update_current_generation() instead of obs.update()
                        langfuse = get_langfuse_client()
                        langfuse.update_current_generation(**update_params)
                        
                        # Send span event to SQS (non-blocking, independent of Langfuse)
                        if is_sqs_enabled() and TraceManager.has_active_trace():
                            trace_id = TraceManager._active.get("trace_id")
                            if trace_id:
                                span_event = {
                                    "event_type": "span",
                                    "trace_id": trace_id,
                                    "span_id": obs.id if hasattr(obs, 'id') else "unknown",
                                    "parent_span_id": None,
                                    "name": span_name,
                                    "timestamp": TraceManager._now(),
                                    "duration_ms": duration_ms,
                                    "input": input_data,
                                    "output": output_data,
                                    "metadata": update_params.get("metadata", {})
                                }
                                if usage_info:
                                    span_event["usage"] = usage_info
                                if "cost_details" in update_params:
                                    span_event["cost"] = update_params["cost_details"]
                                send_to_sqs(span_event)
                
                # Flush after exiting context
                from .config import get_langfuse_client
                langfuse = get_langfuse_client()
                langfuse.flush()
                
                status_str = " (error)" if error else ""
                usage_str = f" [{usage_info.get('total_tokens', 0)} tokens]" if usage_info else ""
                print(f"[LLMOps-Observability] Generation sent{status_str}: {span_name} ({duration_ms}ms){usage_str}")
                
                return result
            
            return sync_wrapper
    
    return decorator


