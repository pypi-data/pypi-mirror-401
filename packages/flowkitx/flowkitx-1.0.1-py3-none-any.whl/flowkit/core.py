"""Core FlowKit functionality - async workflow simplification engine."""

import asyncio
from contextlib import asynccontextmanager
from typing import Any, Callable, Dict, Generic, List, Optional, TypeVar, Union
from functools import wraps
import httpx

T = TypeVar('T')


class FlowRequest(Generic[T]):
    """Represents a chainable async request with fluent API."""
    
    def __init__(
        self, 
        client: httpx.AsyncClient,
        method: str,
        url: str,
        **kwargs
    ):
        self._client = client
        self._method = method
        self._url = url
        self._kwargs = kwargs
        self._response: Optional[httpx.Response] = None
        self._data: Any = None
        self._pipe_function: Optional[Callable] = None
        self._original_request: Optional['FlowRequest'] = None
    
    async def _execute(self) -> httpx.Response:
        """Execute the HTTP request."""
        if self._response is None:
            self._response = await getattr(self._client, self._method)(
                self._url, **self._kwargs
            )
        return self._response  # type: ignore
    
    async def response(self) -> httpx.Response:
        """Get the HTTP response object."""
        return await self._execute()
    
    async def json(self) -> Dict[str, Any]:
        """Parse response as JSON."""
        if self._data is None:
            resp = await self._execute()
            self._data = resp.json()
        return self._data
    
    async def text(self) -> str:
        """Get response as text."""
        resp = await self._execute()
        return resp.text
    
    async def content(self) -> bytes:
        """Get response as bytes."""
        resp = await self._execute()
        return resp.content
    
    def pipe(self, func: Callable[[T], Any]) -> 'FlowRequest[Any]':
        """Chain a function to process result."""
        new_request = FlowRequest(self._client, '_pipe', '_internal')
        new_request._pipe_function = func
        new_request._original_request = self
        return new_request
    
    async def get(self) -> Any:
        """Execute the full pipeline and return final result."""
        if self._method == '_pipe' and self._original_request:
            # Execute original request first
            original_data = await self._original_request.get()
            # Apply pipe function
            if self._pipe_function:
                return self._pipe_function(original_data)
            return original_data
        else:
            # Regular request - return JSON by default
            return await self.json()


class FlowClient:
    """Main FlowKit client that simplifies async HTTP operations."""
    
    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: httpx.Timeout = httpx.Timeout(30.0),
        headers: Optional[Dict[str, str]] = None,
        follow_redirects: bool = True,
    ):
        self.base_url = base_url
        self.timeout = timeout
        self.headers = headers or {}
        self.follow_redirects = follow_redirects
        self._client: Optional[httpx.AsyncClient] = None
    
    @asynccontextmanager
    async def session(self):
        """Context manager for async HTTP session."""
        client_kwargs = {
            'timeout': self.timeout,
            'headers': self.headers,
            'follow_redirects': self.follow_redirects,
        }
        if self.base_url:
            client_kwargs['base_url'] = self.base_url
            
        async with httpx.AsyncClient(**client_kwargs) as client:
            yield client
    
    def _create_request(
        self, 
        method: str, 
        url: str, 
        **kwargs
    ) -> FlowRequest:
        """Create a new FlowRequest instance."""
        # Handle URL joining with base_url
        base_url = self.base_url
        if base_url and not url.startswith(('http://', 'https://')):
            url = f"{base_url.rstrip('/')}/{url.lstrip('/')}"
        
        # Create temporary client for each request
        client_kwargs = {
            'timeout': self.timeout,
            'headers': self.headers,
            'follow_redirects': self.follow_redirects,
        }
        if base_url:
            client_kwargs['base_url'] = base_url
            
        client = httpx.AsyncClient(**client_kwargs)
        
        return FlowRequest(client, method, url, **kwargs)
    
    def get(self, url: str, **kwargs) -> FlowRequest:
        """Create a GET request."""
        return self._create_request('get', url, **kwargs)
    
    def post(self, url: str, **kwargs) -> FlowRequest:
        """Create a POST request."""
        return self._create_request('post', url, **kwargs)
    
    def put(self, url: str, **kwargs) -> FlowRequest:
        """Create a PUT request."""
        return self._create_request('put', url, **kwargs)
    
    def delete(self, url: str, **kwargs) -> FlowRequest:
        """Create a DELETE request."""
        return self._create_request('delete', url, **kwargs)
    
    def patch(self, url: str, **kwargs) -> FlowRequest:
        """Create a PATCH request."""
        return self._create_request('patch', url, **kwargs)
    
    def head(self, url: str, **kwargs) -> FlowRequest:
        """Create a HEAD request."""
        return self._create_request('head', url, **kwargs)
    
    def options(self, url: str, **kwargs) -> FlowRequest:
        """Create an OPTIONS request."""
        return self._create_request('options', url, **kwargs)
    
    async def execute(self, request: FlowRequest[T]) -> T:
        """Execute a FlowRequest and return result."""
        return await request.get()
    
    async def batch(self, requests: List[FlowRequest]) -> List[Any]:
        """Execute multiple requests concurrently."""
        async with self.session() as client:
            tasks = []
            for req in requests:
                # Replace client for each request
                req._client = client
                tasks.append(req.get())
            return await asyncio.gather(*tasks)