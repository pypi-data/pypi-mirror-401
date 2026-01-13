"""FlowKit decorators for auto-async conversion and workflow management."""

import asyncio
import inspect
from typing import Any, Callable, TypeVar, Union
from functools import wraps

from .core import FlowClient, FlowRequest

F = TypeVar('F', bound=Callable[..., Any])


def simple(func: F) -> F:
    """Decorator that automatically converts sync functions to async.
    
    This decorator allows you to write synchronous-looking code that 
    automatically handles async operations using FlowKit.
    
    Example:
        @flowkit.simple
        def fetch_user_data(user_id: int):
            return flowkit.get(f"/users/{user_id}").json().pipe(process_user)
        
        # Usage (still needs to be awaited)
        result = await fetch_user_data(123)
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Create a FlowKit client for this function
        client = FlowClient()
        
        # Execute the function and handle FlowRequest objects
        result = func(*args, **kwargs)
        
        # If result is a FlowRequest, execute it
        if isinstance(result, FlowRequest):
            return await result.get()
        
        # If result is a coroutine, await it
        if inspect.iscoroutine(result):
            return await result
        
        return result
    
    return wrapper  # type: ignore


def flow(func: F) -> F:
    """Decorator for managing complex async workflows with automatic session handling.
    
    Example:
        @flowkit.flow
        def fetch_multiple_data():
            user_req = flowkit.get("/user")
            posts_req = flowkit.get("/posts")
            comments_req = flowkit.get("/comments")
            
            # Execute all requests concurrently
            return await flowkit.batch([user_req, posts_req, comments_req])
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        client = FlowClient()
        
        # Execute function with client context
        async with client.session():
            result = func(*args, **kwargs)
            
            # Handle different return types
            if isinstance(result, FlowRequest):
                return await client.execute(result)
            
            if inspect.iscoroutine(result):
                return await result
            
            return result
    
    return wrapper  # type: ignore


def auto_await(func: F) -> F:
    """Advanced decorator that makes async functions callable both sync and async.
    
    This allows the same function to be used in both sync and async contexts.
    """
    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        try:
            # Check if we're in an async context
            loop = asyncio.get_running_loop()
            # If we're already in an async context, return a coroutine
            return func(*args, **kwargs)
        except RuntimeError:
            # No running loop, so run it in a new event loop
            return asyncio.run(func(*args, **kwargs))
    
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        return await func(*args, **kwargs)
    
    # Return different wrappers based on how it's called
    if asyncio.iscoroutinefunction(func):
        return async_wrapper  # type: ignore
    else:
        return sync_wrapper  # type: ignore


# Alias for backward compatibility
workflow = flow