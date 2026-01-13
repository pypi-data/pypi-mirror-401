"""Integration tests for FlowKit."""

import pytest
import asyncio
from unittest.mock import patch, AsyncMock

import flowkit


class TestPackageLevelAPI:
    """Test the package-level API."""
    
    @pytest.mark.asyncio
    async def test_package_level_get(self):
        """Test package-level get method."""
        with patch('flowkit.httpx.AsyncClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_client_class.return_value.__aenter__.return_value = mock_client
            
            # Mock the FlowRequest creation and execution
            with patch.object(flowkit, '_flowkit') as mock_flowkit:
                mock_request = AsyncMock()
                mock_request.get.return_value = {"data": "value"}
                mock_flowkit.get.return_value = mock_request
                
                result = await flowkit.get("https://api.example.com/data").get()
                assert result == {"data": "value"}
    
    def test_package_attributes_exist(self):
        """Test that all package-level attributes are available."""
        assert hasattr(flowkit, 'get')
        assert hasattr(flowkit, 'post')
        assert hasattr(flowkit, 'put')
        assert hasattr(flowkit, 'delete')
        assert hasattr(flowkit, 'patch')
        assert hasattr(flowkit, 'head')
        assert hasattr(flowkit, 'options')
        assert hasattr(flowkit, 'simple')
        assert hasattr(flowkit, 'flow')
        assert hasattr(flowkit, '__version__')


class TestIntegrationExamples:
    """Test real integration examples."""
    
    @pytest.mark.asyncio
    async def test_simple_workflow(self):
        """Test a simple workflow example."""
        @flowkit.simple
        def fetch_user_data(user_id: int):
            return flowkit.get(f"https://api.example.com/users/{user_id}")
        
        with patch('flowkit.httpx.AsyncClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_client_class.return_value.__aenter__.return_value = mock_client
            
            with patch.object(flowkit, '_flowkit') as mock_flowkit:
                mock_request = AsyncMock()
                mock_request.get.return_value = {"id": user_id, "name": "Test User"}
                mock_flowkit.get.return_value = mock_request
                
                result = await fetch_user_data(123)
                assert result == {"id": 123, "name": "Test User"}