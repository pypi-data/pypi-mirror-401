"""Tests for FlowKit decorators."""

import pytest
import asyncio
from unittest.mock import patch, AsyncMock

from flowkit.decorators import simple, flow, auto_await
from flowkit.core import FlowRequest, FlowClient


class TestSimpleDecorator:
    """Test the @simple decorator."""
    
    @pytest.mark.asyncio
    async def test_simple_decorator_with_flow_request(self):
        """Test @simple decorator with FlowRequest."""
        @simple
        def fetch_data():
            # Mock FlowRequest creation
            with patch('flowkit.decorators.FlowClient') as mock_client_class:
                mock_client = mock_client_class.return_value
                mock_request = AsyncMock(spec=FlowRequest)
                mock_request.get.return_value = {"data": "value"}
                mock_client.get.return_value = mock_request
                
                return mock_client.get("https://api.example.com/data")
        
        # We need to test the decorator behavior differently
        # since it's complex with the mocking
        with patch('flowkit.decorators.FlowClient') as mock_client_class:
            mock_client = mock_client_class.return_value
            mock_request = AsyncMock(spec=FlowRequest)
            mock_request.get.return_value = {"data": "value"}
            mock_client.get.return_value = mock_request
            
            @simple
            def fetch_data():
                return mock_client.get("https://api.example.com/data")
            
            result = await fetch_data()
            assert result == {"data": "value"}
    
    @pytest.mark.asyncio
    async def test_simple_decorator_with_regular_data(self):
        """Test @simple decorator with regular data."""
        @simple
        def process_data():
            return {"processed": True}
        
        result = await process_data()
        assert result == {"processed": True}


class TestFlowDecorator:
    """Test the @flow decorator."""
    
    @pytest.mark.asyncio
    async def test_flow_decorator_with_session(self):
        """Test @flow decorator with session management."""
        @flow
        def fetch_data():
            return {"data": "value"}
        
        result = await fetch_data()
        assert result == {"data": "value"}


class TestAutoAwaitDecorator:
    """Test the @auto_await decorator."""
    
    @pytest.mark.asyncio
    async def test_auto_await_with_async_function(self):
        """Test @auto_await with async function."""
        @auto_await
        async def async_func():
            return {"async": True}
        
        result = await async_func()
        assert result == {"async": True}
    
    def test_auto_await_with_sync_function(self):
        """Test @auto_await with sync function."""
        @auto_await
        def sync_func():
            return {"sync": True}
        
        result = sync_func()
        assert result == {"sync": True}