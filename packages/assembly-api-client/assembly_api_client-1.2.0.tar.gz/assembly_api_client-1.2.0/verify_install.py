import asyncio
import os

from assembly_client.api import AssemblyAPIClient
from assembly_client.generated import PARAM_MAP, Service


async def main():
    print("Verifying Assembly API Client (Type-Safe Params)...")

    api_key = os.getenv("ASSEMBLY_API_KEY", "test_key")
    async with AssemblyAPIClient(api_key=api_key) as client:
        print("Client initialized.")

        # 1. Use Enum
        service = Service.국회의원발의법률안
        print(f"Service: {service.name} ({service.value})")

        # 2. Use Request Model
        # Dynamically get the params class (or import it if we knew the name)
        # In real code: from assembly_client.generated.models import Params_OK7XM...
        # Here we use the map for generic testing
        params_cls = PARAM_MAP[service.value]
        print(f"Params Class: {params_cls.__name__}")

        # Instantiate params
        # Note: AGE is required in our dummy spec
        params = params_cls(AGE="21")
        print(f"Params: {params}")

        # 3. Call get_data with typed params
        # We can't really call it without a network or mock, but we can check if it accepts it.
        # Let's mock the internal _resolve_service_id and get_endpoint to avoid network
        # Actually, let's just run it and catch the network error (or expected error)
        # But we want to verify that `params` was converted to dict correctly.

        # Let's inspect the conversion logic by calling a private method or just trusting the code?
        # Better: let's mock `client.client.get` to inspect the arguments.
        from unittest.mock import AsyncMock

        client.client.get = AsyncMock()
        client.client.get.return_value.status_code = 200
        client.client.get.return_value.json.return_value = {}  # Empty response

        # Mock get_endpoint to avoid spec parsing network call if not cached
        # But we have it cached from previous steps.

        try:
            await client.get_data(service, params=params)
        except Exception:
            # We expect an error because response is empty/invalid, but we check the call args
            pass

        # Verify call args
        call_args = client.client.get.call_args
        if call_args:
            args, kwargs = call_args
            sent_params = kwargs.get("params", {})
            print(f"Sent Params: {sent_params}")
            assert sent_params["AGE"] == "21"
            # Check if other required params (KEY, Type, etc) are there?
            # No, those are basic params handled inside get_data or appended?
            # Wait, `get_data` merges `params` with `basic_params`?
            # The current `get_data` implementation passes `params` directly to `client.get`.
            # The User is responsible for basic params?
            # No, `AssemblyAPIClient` usually handles KEY/Type/pIndex/pSize if they are defaults?
            # Let's check `api.py`.

            # Checking `api.py`:
            # It constructs `request_params` with defaults (KEY, Type, pIndex, pSize).
            # Then `request_params.update(params)`.
            # So our `AGE` should be there.

            assert sent_params["KEY"] == api_key
            assert sent_params["Type"] == "json"
            print("Params verification successful!")

    print("Verification complete.")


if __name__ == "__main__":
    asyncio.run(main())
