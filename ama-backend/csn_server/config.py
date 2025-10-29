"""
Configuration settings for CSN Server
"""

from typing import List, Dict, Any
from pydantic_settings import BaseSettings
from pydantic import Field

import json


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application Configuration
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=True, env="DEBUG")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    secret_key: str = Field(env="SECRET_KEY")
    allowed_hosts: List[str] = Field(default=["localhost", "127.0.0.1"], env="ALLOWED_HOSTS")
    
    # Server Configuration
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    workers: int = Field(default=1, env="WORKERS")
    
    # Database Configuration
    database_url: str = Field(default="sqlite:///./csn_server.db", env="DATABASE_URL")
    redis_url: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    
    # Google Cloud / Firestore Configuration
    google_cloud_project: str = Field(env="GOOGLE_CLOUD_PROJECT")
    google_application_credentials: str = Field(env="GOOGLE_APPLICATION_CREDENTIALS")
    firestore_collection_prefix: str = Field(default="csn", env="FIRESTORE_COLLECTION_PREFIX")
    
    # MCP Configuration
    mcp_server_host: str = Field(default="localhost", env="MCP_SERVER_HOST")
    mcp_server_port: int = Field(default=3000, env="MCP_SERVER_PORT")
    mcp_client_id: str = Field(env="MCP_CLIENT_ID")
    mcp_client_secret: str = Field(env="MCP_CLIENT_SECRET")
    
    # Agent Coordination Configuration
    agent_coordination_enabled: bool = Field(default=True, env="AGENT_COORDINATION_ENABLED")
    agent_broker_url: str = Field(default="redis://localhost:6379/1", env="AGENT_BROKER_URL")
    agent_queue_prefix: str = Field(default="csn_agent", env="AGENT_QUEUE_PREFIX")
    websocket_enabled: bool = Field(default=True, env="WEBSOCKET_ENABLED")
    websocket_port: int = Field(default=8001, env="WEBSOCKET_PORT")
    
    # Biofield Validation Configuration
    hrv_validation_enabled: bool = Field(default=True, env="HRV_VALIDATION_ENABLED")
    hrv_sample_rate: int = Field(default=1000, env="HRV_SAMPLE_RATE")
    hrv_min_segment_length: int = Field(default=300, env="HRV_MIN_SEGMENT_LENGTH")
    hrv_max_segment_length: int = Field(default=3000, env="HRV_MAX_SEGMENT_LENGTH")
    hrv_frequency_bands: Dict[str, List[float]] = Field(
        default={
            "vlf": [0.003, 0.04],
            "lf": [0.04, 0.15],
            "hf": [0.15, 0.4],
            "vhf": [0.4, 0.5]
        },
        env="HRV_FREQUENCY_BANDS"
    )
    
    # AMA Integration Configuration
    ama_firestore_collection: str = Field(default="ama_data", env="AMA_FIRESTORE_COLLECTION")
    ama_batch_size: int = Field(default=100, env="AMA_BATCH_SIZE")
    ama_sync_interval: int = Field(default=300, env="AMA_SYNC_INTERVAL")
    
    # Security Configuration
    jwt_secret_key: str = Field(env="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    jwt_access_token_expire_minutes: int = Field(default=30, env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    jwt_refresh_token_expire_days: int = Field(default=7, env="JWT_REFRESH_TOKEN_EXPIRE_DAYS")
    
    # CORS Configuration
    cors_origins: List[str] = Field(default=["http://localhost:3000"], env="CORS_ORIGINS")
    cors_allow_credentials: bool = Field(default=True, env="CORS_ALLOW_CREDENTIALS")
    
    # Monitoring and Logging
    prometheus_enabled: bool = Field(default=True, env="PROMETHEUS_ENABLED")
    prometheus_port: int = Field(default=9090, env="PROMETHEUS_PORT")
    structlog_level: str = Field(default="INFO", env="STRUCTLOG_LEVEL")
    
    # Development Tools
    reload: bool = Field(default=True, env="RELOAD")
    profiling_enabled: bool = Field(default=False, env="PROFILING_ENABLED")
    
    # Version
    version: str = "1.0.0"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Parse JSON strings for complex configurations
        if isinstance(self.hrv_frequency_bands, str):
            self.hrv_frequency_bands = json.loads(self.hrv_frequency_bands)
        if isinstance(self.cors_origins, str):
            self.cors_origins = json.loads(self.cors_origins)
        if isinstance(self.allowed_hosts, str):
            self.allowed_hosts = [host.strip() for host in self.allowed_hosts.split(",")]


# Create global settings instance
settings = Settings() 