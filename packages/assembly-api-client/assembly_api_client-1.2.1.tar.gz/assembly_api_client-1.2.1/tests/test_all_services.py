import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest
from assembly_client.api import AssemblyAPIClient
from assembly_client.generated import MODEL_MAP, Service

FIXTURE_DIR = Path(__file__).parent / "fixtures"

# Get all fixture files
fixture_files = list(FIXTURE_DIR.glob("*.json"))


# Map filenames to Service enum members
# Filename is "Service Name.json" (e.g. "국회의원_발의법률안.json")
# Service enum member name is "국회의원_발의법률안"
def get_service_from_filename(filename):
    name = filename.stem
    # Try exact match
    if hasattr(Service, name):
        return getattr(Service, name)
    return None


test_cases = []
for f in fixture_files:
    service = get_service_from_filename(f)
    if service:
        test_cases.append((service, f))


@pytest.mark.asyncio
@pytest.mark.parametrize("service, fixture_path", test_cases)
async def test_all_services_with_fixtures(service, fixture_path):
    """
    Test that every service can correctly parse its corresponding real-world fixture data.
    """
    with open(fixture_path, encoding="utf-8") as f:
        fixture_data = json.load(f)

    client = AssemblyAPIClient(api_key="test_key")

    # Mock response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = fixture_data
    client.client.get = AsyncMock(return_value=mock_response)

    # Mock endpoint resolution
    client.get_endpoint = AsyncMock(return_value="test_endpoint")

    # Execute
    try:
        results = await client.get_data(service)
    except Exception as e:
        pytest.fail(f"API call failed: {e}")

    # Check if we got data or empty list (some fixtures might be empty if no data found)
    # API returns { "CODE": "INFO-200", "MESSAGE": "해당하는 데이터가 없습니다." } for empty

    # Check if fixture actually has data
    has_data = False
    for _, val in fixture_data.items():
        if isinstance(val, list) and len(val) >= 2 and "row" in val[1]:
            has_data = True
            break

    if has_data:
        assert isinstance(results, list)
        # It's possible results is empty if parsing failed silently, but we want to catch that.
        # However, if the fixture has data, results should have data.
        assert len(results) > 0, f"Failed to parse data for {service.name}"

        # Verify model type
        model_cls = MODEL_MAP[service.value]
        assert isinstance(results[0], model_cls), f"Expected {model_cls.__name__}, got {type(results[0])}"
    else:
        # If fixture is empty (INFO-200), result should be empty list or dict (depending on implementation)
        # Current implementation returns raw dict if no "row" found or empty list?
        # Let's check api.py: if "row" not found, returns data (dict).
        pass
