"""
Notion MCP Integration for CSN Server
- Secure API key handling via Google Secret Manager
- Intelligent rate limiting with exponential backoff
- Comprehensive mapping between AMA smv_entries and Notion database properties
- Batch operations for efficient API usage
- Error handling and retry mechanisms
"""

import aiohttp
import asyncio
import time
import logging
from typing import List, Dict, Any, Optional
from google.cloud import secretmanager
from pydantic import BaseModel
import structlog

# --- Logging ---
logger = structlog.get_logger()

# --- Secure API Key Handling ---
async def get_notion_api_key(secret_id: str, project_id: str) -> str:
    """Retrieve Notion API key from Google Secret Manager asynchronously."""
    client = secretmanager.SecretManagerServiceAsyncClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = await client.access_secret_version(request={"name": name})
    secret = response.payload.data.decode("UTF-8")
    return secret

# --- Rate Limiting with Exponential Backoff ---
async def notion_api_request(
    session: aiohttp.ClientSession,
    method: str,
    url: str,
    headers: Dict[str, str],
    json: Optional[Dict[str, Any]] = None,
    max_retries: int = 5,
    base_delay: float = 1.0,
) -> Any:
    """Make a Notion API request with exponential backoff on rate limits."""
    for attempt in range(max_retries):
        try:
            async with session.request(method, url, headers=headers, json=json) as resp:
                if resp.status == 429:
                    # Rate limited
                    delay = base_delay * (2 ** attempt)
                    logger.warning("Rate limited by Notion API", attempt=attempt, delay=delay)
                    await asyncio.sleep(delay)
                    continue
                elif resp.status >= 500:
                    # Server error
                    delay = base_delay * (2 ** attempt)
                    logger.warning("Server error from Notion API", status=resp.status, attempt=attempt, delay=delay)
                    await asyncio.sleep(delay)
                    continue
                elif resp.status >= 400:
                    # Client error
                    error = await resp.text()
                    logger.error("Client error from Notion API", status=resp.status, error=error)
                    raise Exception(f"Notion API error: {resp.status} {error}")
                return await resp.json()
        except Exception as e:
            logger.error("Exception during Notion API request", error=str(e), attempt=attempt)
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(base_delay * (2 ** attempt))

# --- AMA to Notion Mapping ---
class AMAEntry(BaseModel):
    id: str
    patient_id: str
    timestamp: str
    data_type: str
    data: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None


def map_ama_to_notion(entry: AMAEntry, property_map: Dict[str, str]) -> Dict[str, Any]:
    """Map AMA entry to Notion database properties."""
    notion_props = {}
    for ama_key, notion_key in property_map.items():
        value = getattr(entry, ama_key, None)
        if value is not None:
            notion_props[notion_key] = {"rich_text": [{"text": {"content": str(value)}}]}
    # Example: add more complex mapping if needed
    return notion_props

# --- Batch Operations ---
async def batch_upsert_to_notion(
    entries: List[AMAEntry],
    notion_database_id: str,
    property_map: Dict[str, str],
    notion_api_key: str,
    batch_size: int = 10,
    notion_api_url: str = "https://api.notion.com/v1/pages",
    notion_version: str = "2022-06-28",
) -> List[Dict[str, Any]]:
    """Batch upsert AMA entries to Notion database."""
    headers = {
        "Authorization": f"Bearer {notion_api_key}",
        "Notion-Version": notion_version,
        "Content-Type": "application/json",
    }
    results = []
    async with aiohttp.ClientSession() as session:
        for i in range(0, len(entries), batch_size):
            batch = entries[i:i+batch_size]
            tasks = []
            for entry in batch:
                props = map_ama_to_notion(entry, property_map)
                payload = {
                    "parent": {"database_id": notion_database_id},
                    "properties": props
                }
                tasks.append(
                    notion_api_request(session, "POST", notion_api_url, headers, json=payload)
                )
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            for res in batch_results:
                if isinstance(res, Exception):
                    logger.error("Failed to upsert entry to Notion", error=str(res))
                else:
                    results.append(res)
    return results

# --- Example Usage Function ---
async def sync_ama_entries_to_notion(
    ama_entries: List[Dict[str, Any]],
    property_map: Dict[str, str],
    notion_database_id: str,
    secret_id: str,
    project_id: str,
    batch_size: int = 10,
) -> List[Dict[str, Any]]:
    """Sync a list of AMA entries to Notion with secure key handling and retries."""
    notion_api_key = await get_notion_api_key(secret_id, project_id)
    entries = [AMAEntry(**entry) for entry in ama_entries]
    results = await batch_upsert_to_notion(
        entries,
        notion_database_id,
        property_map,
        notion_api_key,
        batch_size=batch_size
    )
    return results 