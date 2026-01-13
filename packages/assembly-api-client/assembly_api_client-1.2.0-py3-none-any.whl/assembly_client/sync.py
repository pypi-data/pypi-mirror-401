"""
Module to synchronize API specifications.
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

import httpx

from .parser import SpecParser, load_service_map

logger = logging.getLogger(__name__)

MASTER_LIST_SERVICE_ID = "OOBAOA001213RL17443"
BASE_URL = "https://open.assembly.go.kr/portal/openapi"


async def fetch_master_list(api_key: str, parser: SpecParser) -> List[Dict]:
    """Fetch the complete list of APIs from the master service."""

    # 1. Bootstrap: Get the endpoint for the Master List Service
    try:
        logger.info(f"Bootstrapping: Downloading spec for Master List Service ({MASTER_LIST_SERVICE_ID})...")
        # Force download to ensure we have the latest spec for the master list itself
        # Use infSeq=1 for this specific service as per previous observation
        # Note: parser.parse_spec will handle caching, but we might want to force update?
        # For now, let's trust the parser's logic or maybe add a force_refresh flag to parser later.
        # But here we can just clear cache for this ID if we want to force.

        spec = await parser.parse_spec(MASTER_LIST_SERVICE_ID, inf_seq=1)
        master_endpoint = spec.endpoint
        logger.info(f"Resolved Master List Endpoint: {master_endpoint}")
    except Exception as e:
        logger.error(f"Failed to resolve master list endpoint: {e}", exc_info=True)
        raise

    all_rows = []
    p_index = 1
    p_size = 100
    total_count = None

    async with httpx.AsyncClient(timeout=30.0) as client:
        while True:
            url = f"{BASE_URL}/{master_endpoint}"
            params = {
                "KEY": api_key,
                "Type": "json",
                "pIndex": p_index,
                "pSize": p_size,
            }

            try:
                logger.debug(f"Fetching master list page {p_index}...")
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                if master_endpoint in data:
                    service_data = data[master_endpoint]
                    
                    # Get total count on first page
                    if total_count is None and service_data:
                        head = service_data[0].get("head", [])
                        for h in head:
                            if "list_total_count" in h:
                                total_count = h["list_total_count"]
                                break
                    
                    # Structure: [ {head}, {row: []} ]
                    if len(service_data) > 1 and "row" in service_data[1]:
                        rows = service_data[1]["row"]
                        all_rows.extend(rows)

                        # Finish if we've collected everything or no more rows returned
                        if total_count and len(all_rows) >= total_count:
                            break
                        if len(rows) < p_size:
                            break
                        p_index += 1
                    else:
                        break  # No more data
                else:
                    # Check for error in response
                    if "RESULT" in data:
                        logger.error(f"API Error: {data['RESULT']}")
                    break

            except Exception as e:
                logger.error(f"Failed to fetch master list page {p_index}: {e}")
                break

    return all_rows


def save_master_list(rows: List[Dict], cache_dir: Path):
    """Save master list to a single JSON file in the cache directory."""
    output_file = cache_dir / "all_apis.json"

    wrapper = {
        "OPENSRVAPI": [
            {
                "head": [
                    {"list_total_count": len(rows)},
                    {"RESULT": {"CODE": "INFO-000", "MESSAGE": "Normal Processing"}},
                ]
            },
            {"row": rows},
        ]
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(wrapper, f, ensure_ascii=False, indent=2)
    logger.info(f"Saved {len(rows)} APIs to {output_file}")


def cleanup_orphaned_specs(cache_dir: Path, active_service_ids: set[str]):
    """Remove cached spec files that are no longer in the active service list."""
    # Always keep the master list and the bootstrapper spec
    protected_files = {"all_apis.json", f"{MASTER_LIST_SERVICE_ID}.json"}
    
    removed_count = 0
    for json_file in cache_dir.glob("*.json"):
        if json_file.name in protected_files:
            continue
            
        service_id = json_file.stem
        if service_id not in active_service_ids:
            try:
                logger.info(f"Removing orphaned spec cache: {json_file.name}")
                json_file.unlink()
                removed_count += 1
            except OSError as e:
                logger.error(f"Failed to remove orphaned spec {json_file.name}: {e}")
            
    if removed_count > 0:
        logger.info(f"Cleaned up {removed_count} orphaned spec files.")


async def sync_service(parser: SpecParser, service_id: str, service_name: str | None = None) -> str:
    """
    Sync a single service by parsing its spec (downloads if not cached).
    Returns status: 'updated', 'failed'
    """
    try:
        await parser.parse_spec(service_id)
        return "updated"
    except Exception as e:
        logger.error(f"Failed to sync {service_id} ({service_name}): {e}")
        return "failed"


async def sync_all_services(
    api_key: str, parser: SpecParser, limit: Optional[int] = None, force_update_list: bool = False
) -> Dict[str, int]:
    """
    Sync all services found in the master list.

    Args:
        api_key: API Key for fetching master list.
        parser: SpecParser instance.
        limit: Max number of services to sync.
        force_update_list: Whether to force re-downloading the master list.

    Returns:
        Stats dict with 'updated' and 'failed' counts.
    """

    # 1. Update Master List if needed
    master_file = parser.cache_dir / "all_apis.json"
    if force_update_list or not master_file.exists():
        logger.info("Fetching master list...")
        rows = await fetch_master_list(api_key, parser)
        save_master_list(rows, parser.cache_dir)

    # 2. Load Services
    service_map = load_service_map(parser.cache_dir)
    service_ids = sorted(service_map.keys())

    # Cleanup orphaned specs before starting sync
    cleanup_orphaned_specs(parser.cache_dir, set(service_ids))

    if limit:
        service_ids = service_ids[:limit]

    logger.info(f"Starting sync for {len(service_ids)} services...")

    stats = {"updated": 0, "failed": 0}

    # Process in chunks
    chunk_size = 5
    for i in range(0, len(service_ids), chunk_size):
        chunk = service_ids[i : i + chunk_size]
        tasks = [sync_service(parser, sid, service_map.get(sid)) for sid in chunk]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            if isinstance(result, Exception):
                stats["failed"] += 1
            elif result == "updated":
                stats["updated"] += 1
            else:
                stats["failed"] += 1

        logger.info(f"Progress: {min(i + chunk_size, len(service_ids))}/{len(service_ids)}")

    return stats
