import asyncio
import logging
from pathlib import Path

from assembly_client.codegen.generator import generate_model_code, generate_params_model_code, generate_services_enum
from assembly_client.parser import SpecParser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("codegen")


async def main():
    parser = SpecParser()
    generated_dir = Path("src/assembly_client/generated")
    generated_dir.mkdir(parents=True, exist_ok=True)

    # 1. Generate Services Enum
    logger.info("Generating services.py...")
    services_code = generate_services_enum(parser.cache_dir)
    with open(generated_dir / "services.py", "w", encoding="utf-8") as f:
        f.write(services_code)

    # 2. Generate Models
    logger.info("Generating models.py...")
    # We need to iterate over all cached specs.
    # If cache is empty, we might need to sync first?
    # For now, let's assume cache is populated or we iterate over what we have.
    # Or better, iterate over the service map and parse each spec (which will download if needed).
    # But downloading 180 specs might take time.
    # Let's just do it for the ones currently in cache + maybe a few key ones for testing.
    # User said "openapi 스펙으로 저장하든...". Ideally we generate for ALL.
    # But for this session, let's generate for what we have in cache to prove concept.

    # Actually, let's try to generate for ALL if possible, but maybe limit to avoid timeout?
    # Let's just iterate over existing JSON files in cache for now.

    models_code = [
        "from pydantic import BaseModel, Field",
        "from typing import Optional, Union",
        "",
    ]

    json_files = list(parser.cache_dir.glob("*.json"))
    logger.info(f"Found {len(json_files)} cached specs.")

    for json_file in json_files:
        if json_file.name == "all_apis.json":
            continue

        try:
            # Load spec manually to avoid re-parsing logic if possible, or just use parser
            # parser.parse_spec checks cache first.
            service_id = json_file.stem
            spec = await parser.parse_spec(service_id)

            # Response Model
            code = generate_model_code(spec)
            models_code.append(code)
            models_code.append("")

            # Request Params Model
            p_code = generate_params_model_code(spec)
            models_code.append(p_code)
            models_code.append("")

        except Exception as e:
            logger.error(f"Failed to generate model for {json_file}: {e}")

    with open(generated_dir / "models.py", "w", encoding="utf-8") as f:
        f.write("\n".join(models_code))

    # Create __init__.py with MODEL_MAP
    with open(generated_dir / "__init__.py", "w") as f:
        f.write("from .services import Service\n")
        f.write("from .models import *\n\n")

        f.write("MODEL_MAP = {\n")
        for json_file in json_files:
            if json_file.name == "all_apis.json":
                continue
            service_id = json_file.stem
            class_name = f"Model_{service_id}"
            f.write(f"    '{service_id}': {class_name},\n")
        f.write("}\n\n")

        f.write("PARAM_MAP = {\n")
        for json_file in json_files:
            if json_file.name == "all_apis.json":
                continue
            service_id = json_file.stem
            class_name = f"Params_{service_id}"
            f.write(f"    '{service_id}': {class_name},\n")
        f.write("}\n")

    logger.info("Code generation complete.")


if __name__ == "__main__":
    asyncio.run(main())
