from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import os
import redis
import psycopg2
from pathlib import Path
import json
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="Ubuntu Playground API",
    description="Shared workspace API for Homo Lumen Agent Coalition",
    version="1.0.0"
)

# CORS - Allow all origins for development (restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis connection
try:
    REDIS_CLIENT = redis.Redis.from_url(
        os.getenv("REDIS_URL", "redis://redis:6379"),
        decode_responses=True
    )
    REDIS_CLIENT.ping()
    logger.info("✅ Connected to Redis")
except Exception as e:
    logger.error(f"❌ Redis connection failed: {e}")
    REDIS_CLIENT = None

# PostgreSQL connection helper
def get_db_connection():
    try:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        return conn
    except Exception as e:
        logger.error(f"❌ PostgreSQL connection failed: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")

# Workspace root
WORKSPACE_ROOT = Path("/workspace")
WORKSPACE_ROOT.mkdir(parents=True, exist_ok=True)

# ===========================
# MODELS (Pydantic)
# ===========================

class ReadRequest(BaseModel):
    path: str

class WriteRequest(BaseModel):
    path: str
    content: str

class ListRequest(BaseModel):
    path: str = ""

class CommitRequest(BaseModel):
    message: str
    files: List[str]
    agent_name: str

class AgentEvent(BaseModel):
    agent: str
    action: str
    path: Optional[str] = None
    timestamp: str
    metadata: Optional[Dict] = None

# ===========================
# AUTHENTICATION & RBAC
# ===========================

# Simple API key authentication (TODO: Move to environment variables in production)
AGENT_API_KEYS = {
    "manus": os.getenv("MANUS_API_KEY", "manus-dev-key"),
    "code": os.getenv("CODE_API_KEY", "code-dev-key"),
    "lira": os.getenv("LIRA_API_KEY", "lira-dev-key"),
    "orion": os.getenv("ORION_API_KEY", "orion-dev-key"),
    "abacus": os.getenv("ABACUS_API_KEY", "abacus-dev-key"),
    "nyra": os.getenv("NYRA_API_KEY", "nyra-dev-key"),
    "thalus": os.getenv("THALUS_API_KEY", "thalus-dev-key"),
    "aurora": os.getenv("AURORA_API_KEY", "aurora-dev-key"),
    "thalamus": os.getenv("THALAMUS_API_KEY", "thalamus-dev-key"),
    "scribe": os.getenv("SCRIBE_API_KEY", "scribe-dev-key"),
}

# RBAC permissions per agent
AGENT_PERMISSIONS = {
    "manus": ["read:all", "write:shared", "write:manus", "commit:all", "deploy:all"],
    "code": ["read:all", "write:shared", "write:code", "commit:code"],
    "lira": ["read:all", "write:shared", "write:lira", "commit:lira"],
    "orion": ["read:all", "write:all", "commit:all", "approve:all"],
    "abacus": ["read:all", "write:shared", "write:abacus", "analytics:run"],
    "nyra": ["read:all", "write:shared", "write:nyra", "design:create"],
    "thalus": ["read:all", "audit:all", "block:unethical", "validate:ethics"],
    "aurora": ["read:all", "write:shared", "write:aurora", "research:validate"],
    "thalamus": ["read:all", "route:requests", "orchestrate:agents"],
    "scribe": ["read:all", "write:shared", "write:scribe", "document:create"],
}

def verify_api_key(x_api_key: str = Header(..., alias="X-API-Key")) -> str:
    """Verify API key and return agent name"""
    for agent_name, key in AGENT_API_KEYS.items():
        if key == x_api_key:
            logger.info(f"✅ Authenticated agent: {agent_name}")
            return agent_name

    logger.warning(f"❌ Invalid API key attempted")
    raise HTTPException(status_code=401, detail="Invalid API key")

def check_permission(agent_name: str, required_permission: str) -> bool:
    """Check if agent has required permission"""
    permissions = AGENT_PERMISSIONS.get(agent_name, [])

    # Check for exact permission or wildcard
    if required_permission in permissions:
        return True

    # Check for wildcard permissions (e.g., "write:all" includes "write:shared")
    permission_type, permission_target = required_permission.split(":")
    wildcard = f"{permission_type}:all"
    if wildcard in permissions:
        return True

    return False

# ===========================
# ENDPOINTS
# ===========================

@app.get("/")
def root():
    """Root endpoint - API info"""
    return {
        "message": "Ubuntu Playground API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": [
            "/api/workspace/read",
            "/api/workspace/write",
            "/api/workspace/list",
            "/api/git/commit",
            "/health"
        ]
    }

@app.get("/health")
def health():
    """Health check endpoint"""
    redis_status = "connected" if REDIS_CLIENT and REDIS_CLIENT.ping() else "disconnected"

    try:
        conn = get_db_connection()
        conn.close()
        db_status = "connected"
    except:
        db_status = "disconnected"

    return {
        "status": "healthy" if redis_status == "connected" and db_status == "connected" else "degraded",
        "redis": redis_status,
        "database": db_status,
        "workspace": str(WORKSPACE_ROOT),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/workspace/read")
def read_file(request: ReadRequest, agent_name: str = Depends(verify_api_key)):
    """Read a file from the shared workspace"""

    # Permission check
    if not check_permission(agent_name, "read:all"):
        raise HTTPException(status_code=403, detail="Permission denied: read:all required")

    file_path = WORKSPACE_ROOT / request.path

    # Security: Prevent path traversal
    if not file_path.resolve().is_relative_to(WORKSPACE_ROOT.resolve()):
        raise HTTPException(status_code=403, detail="Path traversal attempt detected")

    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {request.path}")

    if not file_path.is_file():
        raise HTTPException(status_code=400, detail=f"Path is not a file: {request.path}")

    try:
        content = file_path.read_text(encoding="utf-8")

        # Log read event to Redis
        if REDIS_CLIENT:
            event = AgentEvent(
                agent=agent_name,
                action="read",
                path=request.path,
                timestamp=datetime.now().isoformat()
            )
            REDIS_CLIENT.publish("workspace:events", event.json())

        logger.info(f"📖 {agent_name} read: {request.path}")
        return {"content": content, "path": request.path}

    except Exception as e:
        logger.error(f"❌ Read error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/workspace/write")
def write_file(request: WriteRequest, agent_name: str = Depends(verify_api_key)):
    """Write a file to the shared workspace"""

    # Permission check
    workspace_area = request.path.split("/")[0] if "/" in request.path else request.path
    required_perm = f"write:{workspace_area}"

    if not (check_permission(agent_name, required_perm) or check_permission(agent_name, "write:all")):
        raise HTTPException(
            status_code=403,
            detail=f"Permission denied: {required_perm} or write:all required"
        )

    file_path = WORKSPACE_ROOT / request.path

    # Security: Prevent path traversal
    if not file_path.resolve().is_relative_to(WORKSPACE_ROOT.resolve()):
        raise HTTPException(status_code=403, detail="Path traversal attempt detected")

    # Create parent directories if they don't exist
    file_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        file_path.write_text(request.content, encoding="utf-8")

        # Publish write event to Redis
        if REDIS_CLIENT:
            event = AgentEvent(
                agent=agent_name,
                action="write",
                path=request.path,
                timestamp=datetime.now().isoformat(),
                metadata={"size": len(request.content)}
            )
            REDIS_CLIENT.publish("workspace:events", event.json())

        logger.info(f"✍️ {agent_name} wrote: {request.path} ({len(request.content)} chars)")
        return {"success": True, "path": request.path, "size": len(request.content)}

    except Exception as e:
        logger.error(f"❌ Write error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/workspace/list")
def list_files(request: ListRequest, agent_name: str = Depends(verify_api_key)):
    """List files in a directory"""

    if not check_permission(agent_name, "read:all"):
        raise HTTPException(status_code=403, detail="Permission denied: read:all required")

    dir_path = WORKSPACE_ROOT / request.path

    # Security: Prevent path traversal
    if not dir_path.resolve().is_relative_to(WORKSPACE_ROOT.resolve()):
        raise HTTPException(status_code=403, detail="Path traversal attempt detected")

    if not dir_path.exists():
        raise HTTPException(status_code=404, detail=f"Directory not found: {request.path}")

    if not dir_path.is_dir():
        raise HTTPException(status_code=400, detail=f"Path is not a directory: {request.path}")

    try:
        files = [
            {
                "path": str(p.relative_to(WORKSPACE_ROOT)),
                "type": "file" if p.is_file() else "directory",
                "size": p.stat().st_size if p.is_file() else None
            }
            for p in dir_path.rglob("*")
        ]

        logger.info(f"📂 {agent_name} listed: {request.path} ({len(files)} items)")
        return {"files": files, "count": len(files)}

    except Exception as e:
        logger.error(f"❌ List error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/git/commit")
def git_commit(request: CommitRequest, agent_name: str = Depends(verify_api_key)):
    """Commit changes to Git (simplified logging for now)"""

    if not check_permission(agent_name, f"commit:{agent_name}") and not check_permission(agent_name, "commit:all"):
        raise HTTPException(
            status_code=403,
            detail=f"Permission denied: commit:{agent_name} or commit:all required"
        )

    try:
        # TODO: Implement actual Git integration with GitPython
        # For now, just log the commit intent to Redis

        if REDIS_CLIENT:
            commit_event = {
                "agent": request.agent_name,
                "message": request.message,
                "files": request.files,
                "timestamp": datetime.now().isoformat()
            }
            REDIS_CLIENT.publish("git:commits", json.dumps(commit_event))

        logger.info(f"📝 {agent_name} committed: '{request.message}' ({len(request.files)} files)")
        return {
            "success": True,
            "message": "Commit logged (Git integration pending)",
            "agent": request.agent_name,
            "files": request.files
        }

    except Exception as e:
        logger.error(f"❌ Commit error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ===========================
# STARTUP/SHUTDOWN
# ===========================

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("🚀 Ubuntu Playground API starting...")
    logger.info(f"📁 Workspace root: {WORKSPACE_ROOT}")

    # Create agent-specific directories
    agent_dirs = ["manus", "code", "lira", "orion", "abacus", "nyra", "thalus", "aurora", "thalamus", "scribe", "shared", "experiments"]
    for agent_dir in agent_dirs:
        (WORKSPACE_ROOT / agent_dir).mkdir(parents=True, exist_ok=True)

    logger.info(f"✅ Created {len(agent_dirs)} agent directories")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("🛑 Ubuntu Playground API shutting down...")
    if REDIS_CLIENT:
        REDIS_CLIENT.close()
        logger.info("✅ Redis connection closed")
