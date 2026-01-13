"""Tests for get_all_data async generator method."""

import pytest
from unittest.mock import AsyncMock, patch

from assembly_client.api import AssemblyAPIClient


@pytest.fixture
def client():
    """Create a test client with mocked dependencies."""
    with patch.object(AssemblyAPIClient, "__init__", lambda self, *args, **kwargs: None):
        c = AssemblyAPIClient.__new__(AssemblyAPIClient)
        c.api_key = "test_key"
        c.service_map = {}
        c.name_to_id = {}
        c.parsed_specs = {}
        return c


@pytest.mark.asyncio
async def test_get_all_data_result_only_response(client):
    """Test that RESULT-only responses (INFO-200) return empty result."""
    # Mock get_data to return RESULT-only response
    client.get_data = AsyncMock(return_value={
        "RESULT": {
            "CODE": "INFO-200",
            "MESSAGE": "해당하는 데이터가 없습니다."
        }
    })
    
    rows_collected = []
    async for rows in client.get_all_data("test_service"):
        rows_collected.extend(rows)
    
    assert rows_collected == []
    client.get_data.assert_called_once()


@pytest.mark.asyncio
async def test_get_all_data_normal_response_single_page(client):
    """Test normal response with single page of data."""
    client.get_data = AsyncMock(return_value={
        "test_endpoint": [
            {"head": [{"list_total_count": 2}]},
            {"row": [{"id": 1}, {"id": 2}]}
        ]
    })
    
    rows_collected = []
    async for rows in client.get_all_data("test_service"):
        rows_collected.extend(rows)
    
    assert len(rows_collected) == 2
    assert rows_collected[0]["id"] == 1
    assert rows_collected[1]["id"] == 2


@pytest.mark.asyncio
async def test_get_all_data_multiple_pages(client):
    """Test pagination across multiple pages."""
    call_count = 0
    
    async def mock_get_data(service_id, params):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return {
                "test_endpoint": [
                    {"head": [{"list_total_count": 150}]},
                    {"row": [{"id": i} for i in range(100)]}
                ]
            }
        else:
            return {
                "test_endpoint": [
                    {"head": [{"list_total_count": 150}]},
                    {"row": [{"id": i} for i in range(100, 150)]}
                ]
            }
    
    client.get_data = mock_get_data
    
    rows_collected = []
    async for rows in client.get_all_data("test_service", p_size=100):
        rows_collected.extend(rows)
    
    assert len(rows_collected) == 150
    assert call_count == 2


@pytest.mark.asyncio
async def test_get_all_data_empty_rows(client):
    """Test that empty rows stops iteration."""
    client.get_data = AsyncMock(return_value={
        "test_endpoint": [
            {"head": [{"list_total_count": 0}]},
            {"row": []}
        ]
    })
    
    rows_collected = []
    async for rows in client.get_all_data("test_service"):
        rows_collected.extend(rows)
    
    assert rows_collected == []


@pytest.mark.asyncio
async def test_get_all_data_non_list_content(client):
    """Test that non-list content stops iteration gracefully."""
    client.get_data = AsyncMock(return_value={
        "strange_endpoint": "not a list"
    })
    
    rows_collected = []
    async for rows in client.get_all_data("test_service"):
        rows_collected.extend(rows)
    
    assert rows_collected == []


@pytest.mark.asyncio
async def test_get_all_data_missing_head(client):
    """Test graceful handling when head is missing list_total_count."""
    client.get_data = AsyncMock(return_value={
        "test_endpoint": [
            {"head": []},  # No list_total_count
            {"row": [{"id": 1}]}
        ]
    })
    
    rows_collected = []
    async for rows in client.get_all_data("test_service"):
        rows_collected.extend(rows)
    
    # Should still return the row, just can't paginate intelligently
    assert len(rows_collected) == 1
