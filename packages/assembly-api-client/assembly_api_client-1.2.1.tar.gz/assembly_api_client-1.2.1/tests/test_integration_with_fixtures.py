import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest
from assembly_client.api import AssemblyAPIClient
from assembly_client.generated import MODEL_MAP, Service

FIXTURE_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def bills_fixture():
    with open(FIXTURE_DIR / "bills.json", encoding="utf-8") as f:
        return json.load(f)


@pytest.mark.asyncio
async def test_get_data_with_fixture(bills_fixture):
    # Setup Mock Client
    client = AssemblyAPIClient(api_key="test_key")

    # Mock the internal http client
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = bills_fixture

    client.client.get = AsyncMock(return_value=mock_response)

    # Mock get_endpoint to avoid spec parsing network call if not cached
    # We assume the spec is cached or we can mock it.
    # Actually, get_data calls get_endpoint.
    # If we have the spec cached (which we do from previous steps), it should work.
    # But to be safe and isolated, we can mock get_endpoint.
    client.get_endpoint = AsyncMock(return_value="test_endpoint")

    # Execute
    service = Service.국회의원_발의법률안
    results = await client.get_data(service, params={"AGE": "21"})

    # Verify
    assert isinstance(results, list)
    assert len(results) > 0

    # Check if items are Pydantic models
    model_cls = MODEL_MAP[service.value]
    first_item = results[0]
    print(f"Result type: {type(first_item)}")
    if isinstance(first_item, dict):
        print("Fallback to dict detected. Attempting manual validation to find error...")
        try:
            model_cls(**first_item)
        except Exception as e:
            print(f"Validation Error: {e}")

    assert isinstance(first_item, model_cls)

    # Verify data content
    # We need to check what's in the fixture.
    # The fixture is raw JSON from API.
    # The API returns { "OK7XM...": [ { "head": ... }, { "row": [...] } ] }
    # get_data extracts the "row" part.

    # The fixture might have a different key than service.value (API quirk)
    fixture_key = list(bills_fixture.keys())[0]
    raw_rows = bills_fixture[fixture_key][1]["row"]
    assert len(results) == len(raw_rows)

    # Check a field
    # We need to know a field name. In our generated model, fields are English keys.
    # Let's check one field.
    # We can inspect the model class to see available fields.
    print(f"Model fields: {model_cls.model_fields.keys()}")

    # Let's assume BILL_ID or BILL_NAME exists as we saw in previous steps
    if hasattr(first_item, "BILL_ID"):
        assert first_item.BILL_ID == raw_rows[0].get("BILL_ID")
    if hasattr(first_item, "BILL_NAME"):
        assert first_item.BILL_NAME == raw_rows[0].get("BILL_NAME")

    print("Bills Test passed!")


@pytest.fixture
def members_fixture():
    with open(FIXTURE_DIR / "members.json", encoding="utf-8") as f:
        return json.load(f)


@pytest.mark.asyncio
async def test_get_members_with_fixture(members_fixture):
    client = AssemblyAPIClient(api_key="test_key")

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = members_fixture
    client.client.get = AsyncMock(return_value=mock_response)
    client.get_endpoint = AsyncMock(return_value="test_endpoint")

    # Service.국회의원인적사항 or 국회의원_인적사항
    # We need to find the correct enum member.
    # Let's check services.py content or try both.
    service = getattr(Service, "국회의원인적사항", None) or getattr(Service, "국회의원_인적사항", None)
    assert service is not None

    results = await client.get_data(service, params={"AGE": "21"})

    assert isinstance(results, list)
    assert len(results) > 0

    model_cls = MODEL_MAP[service.value]
    first_item = results[0]
    assert isinstance(first_item, model_cls)

    # Verify content
    fixture_key = list(members_fixture.keys())[0]
    raw_rows = members_fixture[fixture_key][1]["row"]

    # Check a field (HG_NM is Name)
    if hasattr(first_item, "HG_NM"):
        assert first_item.HG_NM == raw_rows[0].get("HG_NM")

    print("Members Test passed!")
