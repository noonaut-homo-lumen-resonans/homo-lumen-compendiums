"""
Notion MCP Integration for CSN Server

This module provides comprehensive integration between CSN Server's AMA system and Notion,
including secure API key management, intelligent rate limiting, complex data mapping,
batch operations, and real-time synchronization via webhooks.

Features:
- Secure API key handling via Google Secret Manager
- Intelligent rate limiting with exponential backoff
- Comprehensive mapping between AMA smv_entries and Notion database properties
- Support for complex relations and metadata preservation
- Batch operations for efficient API usage
- Error handling with detailed logging and retry mechanisms
- Webhook support for real-time synchronization
- Pydantic models for request/response validation
"""

import aiohttp
import asyncio
import time
import logging
import json
import hashlib
import hmac
from typing import List, Dict, Any, Optional, Union, Tuple
from datetime import datetime, timezone
from enum import Enum
from pydantic import BaseModel, Field, validator
import structlog

# Configure structured logging
logger = structlog.get_logger()

# --- Pydantic Models for Request/Response Validation ---

class NotionPropertyType(str, Enum):
    """Supported Notion property types"""
    RICH_TEXT = "rich_text"
    NUMBER = "number"
    SELECT = "select"
    MULTI_SELECT = "multi_select"
    DATE = "date"
    CHECKBOX = "checkbox"
    URL = "url"
    EMAIL = "email"
    PHONE_NUMBER = "phone_number"
    RELATION = "relation"
    FILES = "files"
    FORMULA = "formula"
    ROLLUP = "rollup"
    CREATED_TIME = "created_time"
    CREATED_BY = "created_by"
    LAST_EDIT_TIME = "last_edit_time"
    LAST_EDIT_BY = "last_edit_by"

class AMAEntry(BaseModel):
    """AMA entry model for data validation"""
    id: str = Field(..., description="Unique identifier for the AMA entry")
    patient_id: str = Field(..., description="Patient identifier")
    timestamp: datetime = Field(..., description="Entry timestamp")
    data_type: str = Field(..., description="Type of data entry")
    data: Dict[str, Any] = Field(..., description="Main data payload")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    relations: Optional[List[str]] = Field(None, description="Related entry IDs")
    tags: Optional[List[str]] = Field(None, description="Entry tags")
    
    @validator('timestamp', pre=True)
    def parse_timestamp(cls, v):
        if isinstance(v, str):
            return datetime.fromisoformat(v.replace('Z', '+00:00'))
        return v

class NotionPropertyMapping(BaseModel):
    """Mapping configuration for AMA to Notion properties"""
    ama_field: str = Field(..., description="AMA field name")
    notion_property: str = Field(..., description="Notion property name")
    property_type: NotionPropertyType = Field(..., description="Notion property type")
    required: bool = Field(False, description="Whether this field is required")
    transform: Optional[str] = Field(None, description="Transformation function name")
    
class NotionDatabaseConfig(BaseModel):
    """Configuration for Notion database integration"""
    database_id: str = Field(..., description="Notion database ID")
    property_mappings: List[NotionPropertyMapping] = Field(..., description="Property mappings")
    batch_size: int = Field(10, description="Batch size for operations")
    enable_webhooks: bool = Field(False, description="Enable webhook support")
    webhook_secret: Optional[str] = Field(None, description="Webhook secret for verification")

class NotionAPIResponse(BaseModel):
    """Standard Notion API response model"""
    object: str
    id: str
    created_time: Optional[str] = None
    last_edited_time: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None
    url: Optional[str] = None

class WebhookEvent(BaseModel):
    """Notion webhook event model"""
    type: str
    workspace_id: str
    page_id: Optional[str] = None
    database_id: Optional[str] = None
    timestamp: datetime

# --- Secure API Key Handling via Google Secret Manager ---

class NotionSecretManager:
    """Handles secure retrieval of Notion API keys from Google Secret Manager"""
    
    def __init__(self, project_id: str):
        self.project_id = project_id
        self._client = None
    
    async def _get_client(self):
        """Get or create Secret Manager client"""
        if self._client is None:
            try:
                from google.cloud import secretmanager
                self._client = secretmanager.SecretManagerServiceAsyncClient()
            except ImportError:
                raise ImportError("google-cloud-secret-manager is required for secret management")
        return self._client
    
    async def get_notion_api_key(self, secret_id: str) -> str:
        """
        Retrieve Notion API key from Google Secret Manager
        
        Args:
            secret_id: Secret ID in Google Secret Manager
            
        Returns:
            API key as string
            
        Raises:
            Exception: If secret retrieval fails
        """
        try:
            client = await self._get_client()
            name = f"projects/{self.project_id}/secrets/{secret_id}/versions/latest"
            response = await client.access_secret_version(request={"name": name})
            secret = response.payload.data.decode("UTF-8")
            logger.info("Successfully retrieved Notion API key", secret_id=secret_id)
            return secret
        except Exception as e:
            logger.error("Failed to retrieve Notion API key", secret_id=secret_id, error=str(e))
            raise

# --- Rate Limiting with Exponential Backoff ---

class NotionRateLimiter:
    """Handles rate limiting for Notion API with exponential backoff"""
    
    def __init__(self, max_retries: int = 5, base_delay: float = 1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.last_request_time = 0
        self.min_request_interval = 0.1  # 100ms between requests
    
    async def wait_if_needed(self):
        """Wait if needed to respect rate limits"""
        now = time.time()
        time_since_last = now - self.last_request_time
        if time_since_last < self.min_request_interval:
            await asyncio.sleep(self.min_request_interval - time_since_last)
        self.last_request_time = time.time()
    
    async def handle_rate_limit(self, attempt: int, retry_after: Optional[int] = None):
        """Handle rate limiting with exponential backoff"""
        if retry_after:
            delay = retry_after
        else:
            delay = self.base_delay * (2 ** attempt)
        
        logger.warning("Rate limited by Notion API", attempt=attempt, delay=delay, retry_after=retry_after)
        await asyncio.sleep(delay)

class NotionAPIClient:
    """Handles all Notion API interactions with rate limiting and error handling"""
    
    def __init__(self, api_key: str, rate_limiter: NotionRateLimiter):
        self.api_key = api_key
        self.rate_limiter = rate_limiter
        self.base_url = "https://api.notion.com/v1"
        self.version = "2022-06-28"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Notion-Version": self.version,
            "Content-Type": "application/json",
        }
    
    async def request(
        self,
        method: str,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make a Notion API request with rate limiting and retry logic
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            json_data: JSON payload
            params: Query parameters
            
        Returns:
            API response as dictionary
            
        Raises:
            Exception: If request fails after all retries
        """
        url = f"{self.base_url}{endpoint}"
        
        for attempt in range(self.rate_limiter.max_retries):
            try:
                await self.rate_limiter.wait_if_needed()
                
                async with aiohttp.ClientSession() as session:
                    async with session.request(
                        method, url, headers=self.headers, json=json_data, params=params
                    ) as resp:
                        if resp.status == 429:
                            retry_after = resp.headers.get('Retry-After')
                            retry_after_int = int(retry_after) if retry_after else None
                            await self.rate_limiter.handle_rate_limit(attempt, retry_after_int)
                            continue
                        elif resp.status >= 500:
                            delay = self.rate_limiter.base_delay * (2 ** attempt)
                            logger.warning("Server error from Notion API", status=resp.status, attempt=attempt, delay=delay)
                            await asyncio.sleep(delay)
                            continue
                        elif resp.status >= 400:
                            error_text = await resp.text()
                            logger.error("Client error from Notion API", status=resp.status, error=error_text)
                            raise Exception(f"Notion API error: {resp.status} {error_text}")
                        
                        response_data = await resp.json()
                        logger.info("Notion API request successful", method=method, endpoint=endpoint, status=resp.status)
                        return response_data
                        
            except Exception as e:
                logger.error("Exception during Notion API request", error=str(e), attempt=attempt, method=method, endpoint=endpoint)
                if attempt == self.rate_limiter.max_retries - 1:
                    raise
                await asyncio.sleep(self.rate_limiter.base_delay * (2 ** attempt))
        
        raise Exception("Max retries exceeded")

# --- AMA to Notion Mapping with Complex Relations ---

class NotionPropertyMapper:
    """Handles mapping between AMA entries and Notion database properties"""
    
    def __init__(self, config: NotionDatabaseConfig):
        self.config = config
        self.mappings = {m.ama_field: m for m in config.property_mappings}
    
    def map_ama_to_notion(self, entry: AMAEntry) -> Dict[str, Any]:
        """
        Map AMA entry to Notion database properties
        
        Args:
            entry: AMA entry to map
            
        Returns:
            Notion properties dictionary
        """
        notion_props = {}
        
        for mapping in self.config.property_mappings:
            value = self._get_ama_value(entry, mapping.ama_field)
            if value is not None or mapping.required:
                notion_props[mapping.notion_property] = self._create_notion_property(
                    value, mapping.property_type, mapping.transform
                )
        
        # Handle relations if present
        if entry.relations:
            notion_props["Relations"] = {
                "relation": [{"id": rel_id} for rel_id in entry.relations]
            }
        
        # Handle tags if present
        if entry.tags:
            notion_props["Tags"] = {
                "multi_select": [{"name": tag} for tag in entry.tags]
            }
        
        return notion_props
    
    def _get_ama_value(self, entry: AMAEntry, field: str) -> Any:
        """Extract value from AMA entry"""
        if field == "id":
            return entry.id
        elif field == "patient_id":
            return entry.patient_id
        elif field == "timestamp":
            return entry.timestamp.isoformat()
        elif field == "data_type":
            return entry.data_type
        elif field == "data":
            return json.dumps(entry.data)
        elif field == "metadata":
            return json.dumps(entry.metadata) if entry.metadata else None
        elif field.startswith("data."):
            # Access nested data fields
            keys = field.split(".")[1:]
            value = entry.data
            for key in keys:
                value = value.get(key) if isinstance(value, dict) else None
                if value is None:
                    break
            return value
        return None
    
    def _create_notion_property(self, value: Any, property_type: NotionPropertyType, transform: Optional[str]) -> Dict[str, Any]:
        """Create Notion property with appropriate type"""
        if transform:
            value = self._apply_transform(value, transform)
        
        if value is None:
            return {property_type: []}
        
        if property_type == NotionPropertyType.RICH_TEXT:
            return {"rich_text": [{"text": {"content": str(value)}}]}
        elif property_type == NotionPropertyType.NUMBER:
            return {"number": float(value) if value else None}
        elif property_type == NotionPropertyType.SELECT:
            return {"select": {"name": str(value)}}
        elif property_type == NotionPropertyType.MULTI_SELECT:
            if isinstance(value, list):
                return {"multi_select": [{"name": str(v)} for v in value]}
            else:
                return {"multi_select": [{"name": str(value)}]}
        elif property_type == NotionPropertyType.DATE:
            if isinstance(value, datetime):
                return {"date": {"start": value.isoformat()}}
            elif isinstance(value, str):
                return {"date": {"start": value}}
        elif property_type == NotionPropertyType.CHECKBOX:
            return {"checkbox": bool(value)}
        elif property_type == NotionPropertyType.URL:
            return {"url": str(value) if value else None}
        elif property_type == NotionPropertyType.EMAIL:
            return {"email": str(value) if value else None}
        elif property_type == NotionPropertyType.PHONE_NUMBER:
            return {"phone_number": str(value) if value else None}
        
        # Default to rich text
        return {"rich_text": [{"text": {"content": str(value)}}]}
    
    def _apply_transform(self, value: Any, transform: str) -> Any:
        """Apply transformation to value"""
        if transform == "uppercase":
            return str(value).upper()
        elif transform == "lowercase":
            return str(value).lower()
        elif transform == "title":
            return str(value).title()
        elif transform == "truncate_100":
            return str(value)[:100]
        return value

# --- Batch Operations ---

class NotionBatchProcessor:
    """Handles batch operations for efficient Notion API usage"""
    
    def __init__(self, client: NotionAPIClient, mapper: NotionPropertyMapper):
        self.client = client
        self.mapper = mapper
    
    async def batch_create_pages(self, entries: List[AMAEntry], batch_size: int = None) -> List[Dict[str, Any]]:
        """
        Create multiple pages in Notion database
        
        Args:
            entries: List of AMA entries to create
            batch_size: Size of each batch (uses config default if None)
            
        Returns:
            List of created page responses
        """
        if batch_size is None:
            batch_size = self.mapper.config.batch_size
        
        results = []
        for i in range(0, len(entries), batch_size):
            batch = entries[i:i + batch_size]
            batch_results = await self._process_batch(batch)
            results.extend(batch_results)
            logger.info("Processed batch", batch_number=i//batch_size + 1, batch_size=len(batch), success_count=len([r for r in batch_results if not isinstance(r, Exception)]))
        
        return results
    
    async def _process_batch(self, entries: List[AMAEntry]) -> List[Dict[str, Any]]:
        """Process a single batch of entries"""
        tasks = []
        for entry in entries:
            props = self.mapper.map_ama_to_notion(entry)
            payload = {
                "parent": {"database_id": self.mapper.config.database_id},
                "properties": props
            }
            tasks.append(self.client.request("POST", "/pages", json_data=payload))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results

# --- Webhook Support for Real-time Synchronization ---

class NotionWebhookHandler:
    """Handles Notion webhooks for real-time synchronization"""
    
    def __init__(self, secret: str):
        self.secret = secret
    
    def verify_signature(self, body: bytes, signature: str, timestamp: str) -> bool:
        """
        Verify webhook signature
        
        Args:
            body: Request body
            signature: X-Notion-Signature header
            timestamp: X-Notion-Timestamp header
            
        Returns:
            True if signature is valid
        """
        try:
            expected_signature = hmac.new(
                self.secret.encode('utf-8'),
                f"{timestamp}.{body.decode('utf-8')}".encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            return hmac.compare_digest(f"v0={expected_signature}", signature)
        except Exception as e:
            logger.error("Failed to verify webhook signature", error=str(e))
            return False
    
    def parse_webhook_event(self, body: Dict[str, Any]) -> WebhookEvent:
        """
        Parse webhook event from Notion
        
        Args:
            body: Webhook request body
            
        Returns:
            Parsed webhook event
        """
        return WebhookEvent(
            type=body.get("type", ""),
            workspace_id=body.get("workspace_id", ""),
            page_id=body.get("page", {}).get("id") if body.get("page") else None,
            database_id=body.get("database", {}).get("id") if body.get("database") else None,
            timestamp=datetime.fromisoformat(body.get("timestamp", "").replace('Z', '+00:00'))
        )

# --- Main Integration Class ---

class NotionMCPIntegration:
    """Main integration class for Notion MCP functionality"""
    
    def __init__(
        self,
        project_id: str,
        secret_id: str,
        config: NotionDatabaseConfig,
        rate_limiter: Optional[NotionRateLimiter] = None
    ):
        self.project_id = project_id
        self.secret_id = secret_id
        self.config = config
        self.rate_limiter = rate_limiter or NotionRateLimiter()
        self.secret_manager = NotionSecretManager(project_id)
        self.api_key = None
        self.client = None
        self.mapper = NotionPropertyMapper(config)
        self.batch_processor = None
        self.webhook_handler = None
        
        if config.enable_webhooks and config.webhook_secret:
            self.webhook_handler = NotionWebhookHandler(config.webhook_secret)
    
    async def initialize(self):
        """Initialize the integration by retrieving API key and setting up clients"""
        self.api_key = await self.secret_manager.get_notion_api_key(self.secret_id)
        self.client = NotionAPIClient(self.api_key, self.rate_limiter)
        self.batch_processor = NotionBatchProcessor(self.client, self.mapper)
        logger.info("Notion MCP integration initialized", database_id=self.config.database_id)
    
    async def sync_ama_entries(self, entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Sync AMA entries to Notion database
        
        Args:
            entries: List of AMA entry dictionaries
            
        Returns:
            List of created page responses
        """
        if not self.client:
            await self.initialize()
        
        ama_entries = [AMAEntry(**entry) for entry in entries]
        results = await self.batch_processor.batch_create_pages(ama_entries)
        
        success_count = len([r for r in results if not isinstance(r, Exception)])
        logger.info("AMA entries synced to Notion", total=len(entries), success=success_count, failed=len(entries) - success_count)
        
        return results
    
    async def handle_webhook(self, body: bytes, signature: str, timestamp: str) -> Optional[WebhookEvent]:
        """
        Handle incoming webhook from Notion
        
        Args:
            body: Request body
            signature: X-Notion-Signature header
            timestamp: X-Notion-Timestamp header
            
        Returns:
            Parsed webhook event if valid, None otherwise
        """
        if not self.webhook_handler:
            logger.warning("Webhook handler not configured")
            return None
        
        if not self.webhook_handler.verify_signature(body, signature, timestamp):
            logger.warning("Invalid webhook signature")
            return None
        
        try:
            body_dict = json.loads(body.decode('utf-8'))
            event = self.webhook_handler.parse_webhook_event(body_dict)
            logger.info("Webhook event received", event_type=event.type, workspace_id=event.workspace_id)
            return event
        except Exception as e:
            logger.error("Failed to parse webhook event", error=str(e))
            return None

# --- Example Usage and Utility Functions ---

async def create_notion_integration(
    project_id: str,
    secret_id: str,
    database_id: str,
    property_mappings: List[Dict[str, Any]],
    enable_webhooks: bool = False,
    webhook_secret: Optional[str] = None
) -> NotionMCPIntegration:
    """
    Create a Notion MCP integration instance
    
    Args:
        project_id: Google Cloud project ID
        secret_id: Secret Manager secret ID for Notion API key
        database_id: Notion database ID
        property_mappings: List of property mapping configurations
        enable_webhooks: Whether to enable webhook support
        webhook_secret: Webhook secret for verification
        
    Returns:
        Configured NotionMCPIntegration instance
    """
    mappings = [NotionPropertyMapping(**m) for m in property_mappings]
    config = NotionDatabaseConfig(
        database_id=database_id,
        property_mappings=mappings,
        enable_webhooks=enable_webhooks,
        webhook_secret=webhook_secret
    )
    
    integration = NotionMCPIntegration(project_id, secret_id, config)
    await integration.initialize()
    return integration 