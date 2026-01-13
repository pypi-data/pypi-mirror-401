import asyncio
import json
import logging
import os
from pathlib import Path

import typer
from assembly_client.api import AssemblyAPIClient
from assembly_client.generated import Service

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Load key from env
API_KEY = os.getenv("ASSEMBLY_API_KEY")
if not API_KEY:
    try:
        with open(".env") as f:
            for line in f:
                if line.startswith("ASSEMBLY_API_KEY="):
                    API_KEY = line.strip().split("=")[1]
                    break
    except FileNotFoundError:
        pass

if not API_KEY:
    raise ValueError("ASSEMBLY_API_KEY not found")

FIXTURE_DIR = Path("tests/fixtures")
FIXTURE_DIR.mkdir(parents=True, exist_ok=True)


async def fetch_fixture(client: AssemblyAPIClient, service: Service):
    filename = f"{service.name}.json"
    filepath = FIXTURE_DIR / filename

    if filepath.exists():
        logger.info(f"Skipping {service.name} (already exists)")
        return

    logger.info(f"Fetching {service.name}...")

    # Default params that might work for many services
    params = {
        "pSize": 1,
        "AGE": "21",  # 21st Assembly
        "UNIT_CD": "100021",  # Sometimes needed
    }

    # Try to be smarter?
    # We could check PARAM_MAP[service.value] to see required fields.
    # But for now, let's just try with defaults and see what sticks.

    try:
        # Use internal client to get raw JSON
        endpoint = await client.get_endpoint(service.value)
        url = f"{client.BASE_URL}/{endpoint}"

        request_params = {
            "KEY": client.api_key,
            "Type": "json",
            "pIndex": 1,
        }
        request_params.update(params)

        response = await client.client.get(url, params=request_params)
        response.raise_for_status()
        data = response.json()

        # Check for API error in response body (INFO-xxx is usually success or no data)
        # But if it's an ERROR code, we might want to know.
        # The API returns errors in <head> usually.

        # Save to file
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"Saved {filename}")

    except Exception as e:
        logger.error(f"Failed to fetch {service.name}: {e}")


app = typer.Typer()


@app.command()
def main(
    force: bool = typer.Option(False, help="Force update existing fixtures"),
    limit: int = typer.Option(None, help="Limit number of fixtures to fetch"),
):
    # Load API Key
    api_key = os.getenv("ASSEMBLY_API_KEY")
    if not api_key:
        # Try .env
        try:
            from dotenv import load_dotenv

            load_dotenv()
            api_key = os.getenv("ASSEMBLY_API_KEY")
        except ImportError:
            pass

    if not api_key:
        logger.error("ASSEMBLY_API_KEY not found. Cannot generate fixtures.")
        return

    async def run():
        async with AssemblyAPIClient(api_key=api_key) as client:
            tasks = []
            sem = asyncio.Semaphore(5)

            async def bound_fetch(s):
                async with sem:
                    # Pass force flag if we modify fetch_fixture to accept it
                    # For now, let's handle force logic here or in fetch_fixture
                    filename = f"{s.name}.json"
                    filepath = FIXTURE_DIR / filename

                    if not force and filepath.exists():
                        # logger.info(f"Skipping {s.name} (already exists)")
                        return

                    await fetch_fixture(client, s)
                    await asyncio.sleep(0.1)

            services = list(Service)
            if limit:
                services = services[:limit]

            for service in services:
                tasks.append(bound_fetch(service))

            await asyncio.gather(*tasks)

    asyncio.run(run())


if __name__ == "__main__":
    app()
