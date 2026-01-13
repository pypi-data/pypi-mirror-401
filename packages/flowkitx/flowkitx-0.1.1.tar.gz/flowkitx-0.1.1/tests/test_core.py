"""FlowKit tests for core functionality."""

import pytest
import asyncio
from unittest.mock import AsyncMock, patch
import httpx

from flowkit.core import FlowClient, FlowRequest


class TestFlowRequest:
    """Test FlowRequest functionality."""
    
    @pytest.fixture
    def mock_client(self):
        """Create a mock HTTP client."""
        client = AsyncMock(spec=httpx.AsyncClient)
        return client
    
    @pytest.fixture
    def flow_request(self, mock_client):
        """Create a FlowRequest for testing."""
        return FlowRequest(mock_client, 'get', 'https://api.example.com/data')
    
    @pytest.mark.asyncio
    async def test_request_execution(self, flow_request, mock_client):
        """Test that requests are executed properly."""
        # Mock response
        mock_response = AsyncMock(spec=httpx.Response)
        mock_response.json.return_value = {"key": "value"}
        mock_client.get.return_value = mock_response
        
        # Execute request
        result = await flow_request._execute()
        
        assert result == mock_response
        mock_client.get.assert_called_once_with(
            'https://api.example.com/data'
        )
    
    @pytest.mark.asyncio
    async def test_json_parsing(self, flow_request, mock_client):
        """Test JSON response parsing."""
        mock_response = AsyncMock(spec=httpx.Response)
        mock_response.json.return_value = {"key": "value"}
        mock_client.get.return_value = mock_response
        
        result = await flow_request.json()
        
        assert result == {"key": "value"}
    
    @pytest.mark.asyncio
    async def test_pipe_chaining(self, mock_client):
        """Test method chaining with pipe."""
        flow_request = FlowRequest(mock_client, 'get', 'https://api.example.com/data')
        
        def process_data(data):
            return {"processed": data}
        
        chained_request = flow_request.pipe(process_data)
        
        # Mock the original data
        mock_response = AsyncMock(spec=httpx.Response)
        mock_response.json.return_value = {"key": "value"}
        mock_client.get.return_value = mock_response
        
        result = await chained_request.get()
        
        assert result == {"processed": {"key": "value"}}


class TestFlowClient:
    """Test FlowClient functionality."""
    
    @pytest.fixture
    def client(self):
        """Create a FlowClient instance."""
        return FlowClient()
    
    def test_client_initialization(self):
        """Test client initialization with parameters."""
        client = FlowClient(
            base_url="https://api.example.com",
            timeout=httpx.Timeout(10.0),
            headers={"Authorization": "Bearer token"}
        )
        
        assert client.base_url == "https://api.example.com"
        assert client.timeout.timeout == 10.0
        assert client.headers["Authorization"] == "Bearer token"
    
    def test_request_creation(self, client):
        """Test that requests are created properly."""
        request = client.get("/endpoint")
        
        assert isinstance(request, FlowRequest)
        assert request._method == "get"
        assert request._url == "/endpoint"
    
    def test_url_joining_with_base_url(self):
        """Test URL joining with base URL."""
        client = FlowClient(base_url="https://api.example.com/v1")
        
        # Test URL joining
        request = client.get("/users")
        assert request._url == "https://api.example.com/v1/users"
        
        # Test with full URL (should not be modified)
        request = client.get("https://other.api.com/data")
        assert request._url == "https://other.api.com/data"
    
    @pytest.mark.asyncio
    async def test_batch_execution(self):
        """Test concurrent batch execution."""
        client = FlowClient()
        
        # Create mock requests
        with patch('flowkit.core.httpx.AsyncClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_client_class.return_value.__aenter__.return_value = mock_client
            
            # Create mock responses
            mock_response1 = AsyncMock(spec=httpx.Response)
            mock_response2 = AsyncMock(spec=httpx.Response)
            mock_response1.json.return_value = {"id": 1}
            mock_response2.json.return_value = {"id": 2}
            
            # Mock the FlowRequest.get method
            mock_get1 = AsyncMock(return_value={"id": 1})
            mock_get2 = AsyncMock(return_value={"id": 2})
            
            req1 = FlowRequest(mock_client, 'get', 'url1')
            req2 = FlowRequest(mock_client, 'get', 'url2')
            req1.get = mock_get1
            req2.get = mock_get2
            
            results = await client.batch([req1, req2])
            
            assert results == [{"id": 1}, {"id": 2}]