from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from assembly_client.api import AssemblyAPIClient
from assembly_client.errors import AssemblyAPIError

SAMPLE_SPEC = {"OPENSRVAPI": [{"row": [{"INF_ID": "TEST_ID", "INF_NM": "Test Service"}]}]}


@pytest.fixture
def mock_env():
    with patch.dict("os.environ", {"ASSEMBLY_API_KEY": "test_key"}):
        yield


@pytest.mark.asyncio
async def test_client_init(mock_env):
    client = AssemblyAPIClient()
    assert client.api_key == "test_key"
    # New client does not pre-load specs, so we don't check for TEST_ID in specs
    assert client.spec_parser is not None


@pytest.mark.asyncio
async def test_get_data_success(mock_env):
    client = AssemblyAPIClient()

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "test_endpoint": [
            {"head": [{"RESULT": {"CODE": "INFO-000", "MESSAGE": "Success"}}]},
            {"row": [{"data": "value"}]},
        ]
    }
    mock_response.raise_for_status = MagicMock()

    # Mock get_endpoint to return a test endpoint
    client.get_endpoint = AsyncMock(return_value="test_endpoint")

    # Mock the async client.get method
    client.client.get = AsyncMock(return_value=mock_response)

    data = await client.get_data("TEST_ID")
    # The new client returns the whole JSON response, so we access it directly
    assert data["test_endpoint"][1]["row"][0]["data"] == "value"
    client.client.get.assert_called_once()


@pytest.mark.asyncio
async def test_get_data_error(mock_env):
    client = AssemblyAPIClient()

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "test_endpoint": [{"head": [{"RESULT": {"CODE": "INFO-300", "MESSAGE": "Error"}}]}]
    }
    mock_response.raise_for_status = MagicMock()

    # Mock get_endpoint and _resolve_service_id
    client.get_endpoint = AsyncMock(return_value="test_endpoint")
    client._resolve_service_id = MagicMock(side_effect=lambda x: x)
    client.client.get = AsyncMock(return_value=mock_response)

    with pytest.raises(AssemblyAPIError) as exc:
        await client.get_data("TEST_ID")
    assert "INFO-300" in str(exc.value)
