from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import os
import redis
import sqlite3
from pathlib import Path
import json
from datetime import datetime
import logging
import sys
import threading
from dotenv import load_dotenv
from fastapi_mcp import FastApiMCP

# Triadiske Portvokter (Triadic Gates)
from gates import BiofeltGate, BiofeltContext, ResonanceLevel
from gates import ThalosFilter, ThalosContext, EthicalSeverity
from gates import MutationLog, MutationLevel, ValidationOutcome

# GENOMOS DNA API Router
from routers import dna_router, initialize_dna_blockchain
# Orchestration API Router (Multi-Agent Live Streaming)
from routers.orchestration_api import router as orchestration_router
# Health Connect API Router (Real-Time Biofelt Synchronization)
from routers.health_connect_api import router as health_router
# Connector Status Router (Google AI, ElevenLabs, Vercel)
from routers.connector_status import router as connector_router
# YouTube Saga Workflow Router (Automated Video Production)
# TEMP DISABLED: Missing asyncpg dependency
# from routers.saga_workflow import router as saga_router
from blockchain.agent_dna_chain import AgentDNAChain
from blockchain.dna_block import GeneType
from blockchain.reference_extractor import extract_smk_references_from_consultation, merge_smk_references

# Google Workspace Integration
from blockchain.google_drive_manager import initialize_drive_manager
from blockchain.google_sheets_manager import initialize_sheets_manager
from scripts.scheduled_jobs import initialize_scheduler

# Redis Event Subscriber
from redis_subscriber import ubuntu_subscriber

# Load .env files (try both locations)
load_dotenv(dotenv_path="../.env.local")  # Legacy location
load_dotenv(dotenv_path=".env")  # New location (api/.env)

# Fix Windows console encoding for emoji
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="Ubuntu Playground API (Local MVP)",
    description="Shared workspace API for Homo Lumen Agent Coalition - Local Development",
    version="1.0.0-local"
)

# CORS - Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===========================
# MCP INTEGRATION (Model Context Protocol)
# ===========================
# Expose Ubuntu Playground workspace operations as MCP tools
# This enables standardized agent-to-resource communication
mcp = FastApiMCP(app)
logger.info("SUCCESS: MCP (Model Context Protocol) initialized")

# ===========================
# GENOMOS DNA API Router
# ===========================
# Include DNA blockchain query endpoints
app.include_router(dna_router)
logger.info("SUCCESS: GENOMOS DNA API router included")

# Include Orchestration API (Multi-Agent Live Streaming)
app.include_router(orchestration_router)
logger.info("SUCCESS: Orchestration API router included (SSE live streaming)")

# Include Health Connect API (Real-Time Biofelt Synchronization)
app.include_router(health_router)
logger.info("SUCCESS: Health Connect API router included (real-time biofelt data)")

# Include Connector Status API (Google AI, ElevenLabs, Vercel)
app.include_router(connector_router)
logger.info("SUCCESS: Connector Status API router included (Google AI + ElevenLabs + Vercel)")

# Include YouTube Saga Workflow API (Automated Video Production)
# TEMP DISABLED: Missing asyncpg dependency
# app.include_router(saga_router)
# logger.info("SUCCESS: YouTube Saga Workflow API router included")

# Redis connection (optional - only for binary protocol if needed)
# Note: Upstash uses REST API via redis_subscriber.py, not binary protocol
REDIS_CLIENT = None
redis_url = os.getenv("REDIS_URL", "")

if redis_url.startswith("redis://"):
    # Only try binary Redis if URL uses redis:// protocol (local Redis)
    try:
        REDIS_CLIENT = redis.Redis.from_url(redis_url, decode_responses=True)
        REDIS_CLIENT.ping()
        logger.info("SUCCESS: Connected to binary Redis")
    except Exception as e:
        logger.info(f"INFO: Binary Redis not available (using REST API): {e}")
        REDIS_CLIENT = None
else:
    # Upstash Cloud uses HTTPS REST API (handled by redis_subscriber.py)
    logger.info("INFO: Using Upstash REST API for Redis (no binary connection needed)")

# Redis subscriber thread (will be started in startup event)
subscriber_thread = None

# SQLite database helper
DATABASE_PATH = Path(os.getenv("DATABASE_PATH", "./data/ubuntu-playground.db"))
DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

def get_db_connection():
    """Get SQLite database connection"""
    try:
        conn = sqlite3.connect(str(DATABASE_PATH))
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        logger.error(f"❌ SQLite connection failed: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")

def init_database():
    """Initialize SQLite database schema"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Events table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent TEXT NOT NULL,
            action TEXT NOT NULL,
            path TEXT,
            timestamp TEXT NOT NULL,
            metadata TEXT
        )
    """)

    # Actions table (for CSN Server integration)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent TEXT NOT NULL,
            action_type TEXT NOT NULL,
            payload TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            result TEXT,
            created_at TEXT NOT NULL,
            completed_at TEXT
        )
    """)

    # Consultations table (GENOMOS Phase 7)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consultations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            consultation_id TEXT UNIQUE NOT NULL,
            human_query TEXT NOT NULL,
            agent_responses TEXT NOT NULL,
            synthesis TEXT NOT NULL,
            biofelt_context TEXT,
            thalos_context TEXT,
            blockchain_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    # Agent Learning table (GENOMOS Phase 5)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agent_learning (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            learning_id TEXT UNIQUE NOT NULL,
            agent_name TEXT NOT NULL,
            learning_event_type TEXT NOT NULL,
            context TEXT NOT NULL,
            before_state TEXT,
            after_state TEXT,
            trigger TEXT NOT NULL,
            metrics TEXT,
            related_smk TEXT,
            related_consultations TEXT,
            blockchain_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    logger.info("✅ SQLite database initialized")

# Workspace root
WORKSPACE_ROOT = Path("/workspace" if os.path.exists("/workspace") else "./workspace")
WORKSPACE_ROOT.mkdir(parents=True, exist_ok=True)

# CSN Server URL
CSN_SERVER_URL = os.getenv("CSN_SERVER_URL", "http://localhost:8001")

# ===========================
# MODELS (Pydantic)
# ===========================

class ReadRequest(BaseModel):
    path: str

class WriteRequest(BaseModel):
    path: str
    content: str
    biofelt_context: Optional[BiofeltContext] = None  # REQUIRED for critical operations
    thalos_context: Optional[ThalosContext] = None    # RECOMMENDED for ethical validation

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

class ExecuteActionRequest(BaseModel):
    agent: str
    action_type: str
    payload: Dict
    biofelt_context: Optional[BiofeltContext] = None  # REQUIRED for action execution
    thalos_context: Optional[ThalosContext] = None    # RECOMMENDED for ethical validation

class ConsultationRequest(BaseModel):
    """Request model for storing pentagonal consultations in GENOMOS blockchain."""
    consultation_id: str
    human_query: str
    agent_responses: Dict[str, Dict]  # agent_name -> {response, confidence, processing_time_ms}
    synthesis: Dict  # {summary, key_insights, related_smk}
    biofelt_context: Optional[BiofeltContext] = None
    thalos_context: Optional[ThalosContext] = None
    timestamp: Optional[str] = None

class AgentLearningRequest(BaseModel):
    """Request model for storing agent learning events in GENOMOS blockchain."""
    learning_id: str
    agent_name: str
    learning_event_type: str  # "feedback_correction", "pattern_discovery", "skill_improvement", "error_correction"
    context: str  # Description of what triggered the learning
    before_state: Optional[Dict] = None  # State/approach before learning
    after_state: Optional[Dict] = None   # State/approach after learning
    trigger: Dict  # {type: "consultation"|"feedback"|"self_reflection", consultation_id: "...", description: "..."}
    metrics: Optional[Dict] = None  # {confidence_delta: +0.17, response_time_improvement_ms: -300, ...}
    related_smk: Optional[List[str]] = None
    related_consultations: Optional[List[str]] = None
    timestamp: Optional[str] = None

# ===========================
# AUTHENTICATION & RBAC
# ===========================

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
    "zara": os.getenv("ZARA_API_KEY", "zara-dev-key"),  # Added Zara (DeepSeek)
}

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
    "zara": ["read:all", "write:shared", "write:zara", "research:deep"],  # Zara permissions
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

    if required_permission in permissions:
        return True

    # Check for wildcard permissions
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
        "message": "Ubuntu Playground API (Local MVP)",
        "version": "1.0.0-local",
        "mode": "local-development",
        "status": "operational",
        "csn_server": CSN_SERVER_URL,
        "endpoints": [
            "/api/workspace/read",
            "/api/workspace/write",
            "/api/workspace/list",
            "/api/git/commit",
            "/api/execute-action",
            "/health"
        ]
    }

@app.get("/health")
def health():
    """Health check endpoint"""
    # Check Redis subscriber status (REST API via Upstash)
    if ubuntu_subscriber.enabled and subscriber_thread and subscriber_thread.is_alive():
        redis_status = "connected (subscriber)"
    elif REDIS_CLIENT:
        try:
            REDIS_CLIENT.ping()
            redis_status = "connected (binary)"
        except:
            redis_status = "disconnected"
    else:
        redis_status = "disconnected"

    try:
        conn = get_db_connection()
        conn.close()
        db_status = "connected"
    except:
        db_status = "disconnected"

    return {
        "status": "healthy" if "connected" in redis_status and db_status == "connected" else "degraded",
        "redis": redis_status,
        "database": f"sqlite ({db_status})",
        "workspace": str(WORKSPACE_ROOT),
        "csn_server": CSN_SERVER_URL,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/workspace/read")
def read_file(request: ReadRequest, agent_name: str = Depends(verify_api_key)):
    """Read a file from the shared workspace"""

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

        # Log read event
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
    """
    Write a file to the shared workspace.

    PROTECTED BY: BiofeltGate / ResonanceGuard
    Requires positive biofelt-resonans for critical operations.
    """

    # RBAC Permission Check
    workspace_area = request.path.split("/")[0] if "/" in request.path else request.path
    required_perm = f"write:{workspace_area}"

    if not (check_permission(agent_name, required_perm) or check_permission(agent_name, "write:all")):
        raise HTTPException(
            status_code=403,
            detail=f"Permission denied: {required_perm} or write:all required"
        )

    # TRIADISK PORTVOKTER - LAYERED VALIDATION
    # Layer 1: BiofeltGate (Consciousness-Aware Processing)
    if request.biofelt_context:
        gate_result = BiofeltGate.validate_write_operation(
            biofelt=request.biofelt_context,
            file_path=request.path
        )

        if not gate_result.allowed:
            logger.warning(f"🛑 BiofeltGate blocked write by {agent_name}: {gate_result.message}")

            # Layer 3: MutationLog (Audit Trail)
            MutationLog.log_blocked_operation(
                agent=agent_name,
                operation_type=MutationLevel.WRITE,
                target=request.path,
                action=f"write file ({len(request.content)} chars)",
                blocked_by="biofelt",
                error_message=gate_result.message,
                biofelt_resonance=gate_result.resonance_level.value,
                intent=request.thalos_context.intent if request.thalos_context else None,
                justification=request.thalos_context.justification if request.thalos_context else None
            )

            raise HTTPException(
                status_code=403,
                detail={
                    "error": "BiofeltGate blocked operation",
                    "message": gate_result.message,
                    "resonance_level": gate_result.resonance_level.value,
                    "hrv_status": gate_result.hrv_status,
                    "coherence_status": gate_result.coherence_status,
                    "recommendations": gate_result.recommendations
                }
            )
        else:
            logger.info(f"✅ BiofeltGate approved write by {agent_name}: {gate_result.message}")
    else:
        logger.warning(f"⚠️ Write by {agent_name} without biofelt context: {request.path}")

    # Layer 2: ThalosFilter (Ethical Veto / Ontological Coherence)
    thalos_result = ThalosFilter.validate_write(
        file_path=request.path,
        content=request.content,
        agent=agent_name,
        thalos_context=request.thalos_context
    )

    if not thalos_result.allowed:
        logger.warning(f"🛑 ThalosFilter blocked write by {agent_name}: {thalos_result.message}")

        # Layer 3: MutationLog (Audit Trail)
        MutationLog.log_blocked_operation(
            agent=agent_name,
            operation_type=MutationLevel.WRITE,
            target=request.path,
            action=f"write file ({len(request.content)} chars)",
            blocked_by="thalos",
            error_message=thalos_result.message,
            thalos_severity=thalos_result.severity.value,
            intent=request.thalos_context.intent if request.thalos_context else None,
            justification=request.thalos_context.justification if request.thalos_context else None,
            affected_agents=request.thalos_context.affected_agents if request.thalos_context else [],
            reversible=request.thalos_context.reversible if request.thalos_context else True,
            reviewed_by=request.thalos_context.reviewed_by if request.thalos_context else None
        )

        raise HTTPException(
            status_code=403,
            detail={
                "error": "ThalosFilter blocked operation",
                "message": thalos_result.message,
                "severity": thalos_result.severity.value,
                "violated_principles": [p.value for p in thalos_result.violated_principles],
                "warnings": thalos_result.warnings,
                "recommendations": thalos_result.recommendations,
                "requires_review": thalos_result.requires_review
            }
        )

    if thalos_result.severity in [EthicalSeverity.WARNING, EthicalSeverity.CONCERN]:
        logger.warning(f"{thalos_result.message} - Warnings: {', '.join(thalos_result.warnings)}")
    else:
        logger.info(f"✅ ThalosFilter approved write by {agent_name}: {thalos_result.message}")

    file_path = WORKSPACE_ROOT / request.path

    # Security: Prevent path traversal
    if not file_path.resolve().is_relative_to(WORKSPACE_ROOT.resolve()):
        raise HTTPException(status_code=403, detail="Path traversal attempt detected")

    file_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        file_path.write_text(request.content, encoding="utf-8")

        # Publish write event
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

        # Layer 3: MutationLog (Audit Trail) - Log successful operation
        biofelt_resonance = gate_result.resonance_level.value if request.biofelt_context and 'gate_result' in locals() else None
        MutationLog.log_approved_operation(
            agent=agent_name,
            operation_type=MutationLevel.WRITE,
            target=request.path,
            action=f"write file ({len(request.content)} chars)",
            biofelt_resonance=biofelt_resonance,
            thalos_severity=thalos_result.severity.value,
            result_summary=f"Successfully wrote {len(request.content)} chars to {request.path}",
            intent=request.thalos_context.intent if request.thalos_context else None,
            justification=request.thalos_context.justification if request.thalos_context else None,
            affected_agents=request.thalos_context.affected_agents if request.thalos_context else [],
            reversible=request.thalos_context.reversible if request.thalos_context else True,
            reviewed_by=request.thalos_context.reviewed_by if request.thalos_context else None
        )

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
    """Commit changes to Git (simplified logging for MVP)"""

    if not check_permission(agent_name, f"commit:{agent_name}") and not check_permission(agent_name, "commit:all"):
        raise HTTPException(
            status_code=403,
            detail=f"Permission denied: commit:{agent_name} or commit:all required"
        )

    try:
        # Log commit intent to SQLite
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO events (agent, action, path, timestamp, metadata)
            VALUES (?, ?, ?, ?, ?)
        """, (
            request.agent_name,
            "git_commit",
            None,
            datetime.now().isoformat(),
            json.dumps({"message": request.message, "files": request.files})
        ))

        conn.commit()
        conn.close()

        # Publish to Redis
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

@app.post("/api/execute-action")
def execute_action(request: ExecuteActionRequest, agent_name: str = Depends(verify_api_key)):
    """
    Execute an action from CSN Server (integration endpoint).

    PROTECTED BY: BiofeltGate / ResonanceGuard
    Requires BALANCED or higher resonans for action execution.
    """

    # TRIADISK PORTVOKTER - LAYERED VALIDATION
    # Layer 1: BiofeltGate (Consciousness-Aware Processing)
    if request.biofelt_context:
        gate_result = BiofeltGate.validate_execute_action(
            biofelt=request.biofelt_context,
            action_type=request.action_type
        )

        if not gate_result.allowed:
            logger.warning(f"🛑 BiofeltGate blocked action by {agent_name}: {gate_result.message}")
            raise HTTPException(
                status_code=403,
                detail={
                    "error": "BiofeltGate blocked action execution",
                    "message": gate_result.message,
                    "resonance_level": gate_result.resonance_level.value,
                    "hrv_status": gate_result.hrv_status,
                    "coherence_status": gate_result.coherence_status,
                    "recommendations": gate_result.recommendations
                }
            )
        else:
            logger.info(f"✅ BiofeltGate approved action by {agent_name}: {gate_result.message}")
    else:
        logger.warning(f"⚠️ Action execution by {agent_name} without biofelt context: {request.action_type}")

    # Layer 2: ThalosFilter (Ethical Veto / Ontological Coherence)
    thalos_result = ThalosFilter.validate_execute(
        action_type=request.action_type,
        payload=request.payload,
        agent=agent_name,
        thalos_context=request.thalos_context
    )

    if not thalos_result.allowed:
        logger.warning(f"🛑 ThalosFilter blocked action by {agent_name}: {thalos_result.message}")
        raise HTTPException(
            status_code=403,
            detail={
                "error": "ThalosFilter blocked action execution",
                "message": thalos_result.message,
                "severity": thalos_result.severity.value,
                "violated_principles": [p.value for p in thalos_result.violated_principles],
                "warnings": thalos_result.warnings,
                "recommendations": thalos_result.recommendations,
                "requires_review": thalos_result.requires_review
            }
        )

    if thalos_result.severity in [EthicalSeverity.WARNING, EthicalSeverity.CONCERN]:
        logger.warning(f"{thalos_result.message} - Warnings: {', '.join(thalos_result.warnings)}")
    else:
        logger.info(f"✅ ThalosFilter approved action by {agent_name}: {thalos_result.message}")

    try:
        # Store action in database
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO actions (agent, action_type, payload, status, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            request.agent,
            request.action_type,
            json.dumps(request.payload),
            "pending",
            datetime.now().isoformat()
        ))

        action_id = cursor.lastrowid
        conn.commit()
        conn.close()

        # Publish to Redis
        if REDIS_CLIENT:
            action_event = {
                "action_id": action_id,
                "agent": request.agent,
                "action_type": request.action_type,
                "payload": request.payload,
                "timestamp": datetime.now().isoformat()
            }
            REDIS_CLIENT.publish("ubuntu:actions", json.dumps(action_event))

        logger.info(f"🎯 Action queued: {request.action_type} by {request.agent} (ID: {action_id})")

        return {
            "success": True,
            "action_id": action_id,
            "status": "pending",
            "message": f"Action {request.action_type} queued for execution"
        }

    except Exception as e:
        logger.error(f"❌ Action execution error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# CONSULTATION STORAGE (GENOMOS Phase 7)
# ============================================================================

@app.post("/api/store-consultation")
def store_consultation(request: ConsultationRequest):
    """
    Store a pentagonal consultation in both SQLite and GENOMOS blockchain.

    GENOMOS Phase 7: Consultation Blockchain Storage
    """
    try:
        consultation_timestamp = request.timestamp or datetime.now().isoformat()

        # PHASE 6: Auto-detect SMK references from consultation text
        auto_detected_smk = extract_smk_references_from_consultation({
            "human_query": request.human_query,
            "agent_responses": request.agent_responses,
            "synthesis": request.synthesis
        })

        # Merge auto-detected with manually specified SMK refs
        manual_smk = request.synthesis.get("related_smk", [])
        if manual_smk:
            # Extract numbers from manual refs like "SMK#043" -> "043"
            from blockchain.reference_extractor import extract_smk_references
            manual_smk_nums = extract_smk_references(" ".join(manual_smk))
            all_smk = merge_smk_references(auto_detected_smk, manual_smk_nums)
        else:
            all_smk = auto_detected_smk

        # Update synthesis with complete SMK references
        updated_synthesis = request.synthesis.copy() if isinstance(request.synthesis, dict) else {}
        updated_synthesis["related_smk"] = [f"SMK#{num}" for num in all_smk]

        logger.info(f"🔍 Auto-detected {len(auto_detected_smk)} SMK refs, total: {len(all_smk)}")

        # Prepare consultation gene data
        consultation_gene = {
            "type": "consultation",
            "consultation_id": request.consultation_id,
            "timestamp": consultation_timestamp,
            "human_query": request.human_query,
            "agent_responses": request.agent_responses,
            "synthesis": updated_synthesis,
        }

        # Add biofelt context if available
        if request.biofelt_context:
            consultation_gene["biofelt_context"] = {
                "hrv_ms": request.biofelt_context.hrv_ms,
                "coherence": request.biofelt_context.coherence,
                "energy_level": request.biofelt_context.energy_level,
                "stress_indicators": request.biofelt_context.stress_indicators
            }

        # Add thalos validation if available
        if request.thalos_context:
            consultation_gene["thalos_validation"] = {
                "outcome": "APPROVED",
                "principles_checked": request.thalos_context.dict() if request.thalos_context else {}
            }

        # Store in GENOMOS blockchain
        blockchain = AgentDNAChain(db_path="./data/genomos.db")

        # Extract tags from synthesis and query (using auto-detected SMKs)
        tags = ["consultation", "pentagonal"]
        if all_smk:
            for smk_num in all_smk:
                tags.append(f"ref-smk{smk_num}")

        block = blockchain.add_gene(
            gene_type=GeneType.CONSULTATION,
            data=consultation_gene,
            agent="human-ai-collective",
            tags=tags
        )

        logger.info(f"🧬 Consultation stored in GENOMOS: {request.consultation_id}")
        logger.info(f"   Block #{block.index} | Hash: {block.hash[:16]}...")

        # Also store in SQLite for backward compatibility
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO consultations (
                consultation_id, human_query, agent_responses, synthesis,
                biofelt_context, thalos_context, blockchain_hash, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            request.consultation_id,
            request.human_query,
            json.dumps(request.agent_responses),
            json.dumps(request.synthesis),
            json.dumps(request.biofelt_context.dict()) if request.biofelt_context else None,
            json.dumps(request.thalos_context.dict()) if request.thalos_context else None,
            block.hash,
            consultation_timestamp
        ))

        consultation_db_id = cursor.lastrowid
        conn.commit()
        conn.close()

        logger.info(f"💾 Consultation also stored in SQLite (ID: {consultation_db_id})")

        # Also log to Google Sheets if available
        try:
            from blockchain.google_sheets_manager import get_sheets_manager
            sheets_manager = get_sheets_manager()
            if sheets_manager:
                sheets_result = sheets_manager.log_consultation(consultation_gene)
                if sheets_result.get("success"):
                    logger.info(f"📊 Consultation logged to Google Sheets")
        except Exception as e:
            logger.warning(f"⚠️  Failed to log consultation to Google Sheets: {e}")

        return {
            "success": True,
            "consultation_id": request.consultation_id,
            "blockchain_block_index": block.index,
            "blockchain_hash": block.hash,
            "database_id": consultation_db_id,
            "message": "Consultation stored in GENOMOS blockchain, SQLite, and Google Sheets"
        }

    except Exception as e:
        logger.error(f"❌ Consultation storage error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# AGENT LEARNING STORAGE (GENOMOS Phase 5)
# ============================================================================

@app.post("/api/store-agent-learning")
def store_agent_learning(request: AgentLearningRequest):
    """
    Store an agent learning event in both SQLite and GENOMOS blockchain.

    GENOMOS Phase 5: Agent Learning & Adaptation
    """
    try:
        learning_timestamp = request.timestamp or datetime.now().isoformat()

        # Prepare learning gene data
        learning_gene = {
            "type": "agent_learning",
            "learning_id": request.learning_id,
            "agent_name": request.agent_name,
            "learning_event_type": request.learning_event_type,
            "timestamp": learning_timestamp,
            "context": request.context,
            "trigger": request.trigger,
        }

        # Add optional fields if present
        if request.before_state:
            learning_gene["before_state"] = request.before_state
        if request.after_state:
            learning_gene["after_state"] = request.after_state
        if request.metrics:
            learning_gene["metrics"] = request.metrics
        if request.related_smk:
            learning_gene["related_smk"] = request.related_smk
        if request.related_consultations:
            learning_gene["related_consultations"] = request.related_consultations

        # Store in GENOMOS blockchain
        blockchain = AgentDNAChain(db_path="./data/genomos.db")

        # Extract tags
        tags = ["agent-learning", request.agent_name, request.learning_event_type]
        if request.related_smk:
            for smk in request.related_smk:
                tags.append(f"ref-{smk.lower().replace('#', '')}")

        block = blockchain.add_gene(
            gene_type=GeneType.AGENT_LEARNING,
            data=learning_gene,
            agent=request.agent_name,
            tags=tags
        )

        logger.info(f"🧠 Agent learning stored in GENOMOS: {request.agent_name} - {request.learning_event_type}")
        logger.info(f"   Block #{block.index} | Hash: {block.hash[:16]}...")

        # Also store in SQLite
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO agent_learning (
                learning_id, agent_name, learning_event_type, context,
                before_state, after_state, trigger, metrics,
                related_smk, related_consultations, blockchain_hash, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            request.learning_id,
            request.agent_name,
            request.learning_event_type,
            request.context,
            json.dumps(request.before_state) if request.before_state else None,
            json.dumps(request.after_state) if request.after_state else None,
            json.dumps(request.trigger),
            json.dumps(request.metrics) if request.metrics else None,
            json.dumps(request.related_smk) if request.related_smk else None,
            json.dumps(request.related_consultations) if request.related_consultations else None,
            block.hash,
            learning_timestamp
        ))

        learning_db_id = cursor.lastrowid
        conn.commit()
        conn.close()

        logger.info(f"💾 Agent learning also stored in SQLite (ID: {learning_db_id})")

        return {
            "success": True,
            "learning_id": request.learning_id,
            "agent_name": request.agent_name,
            "blockchain_block_index": block.index,
            "blockchain_hash": block.hash,
            "database_id": learning_db_id,
            "message": f"Agent learning stored in GENOMOS blockchain and SQLite"
        }

    except Exception as e:
        logger.error(f"❌ Agent learning storage error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===========================
# STARTUP/SHUTDOWN
# ===========================

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("🚀 Ubuntu Playground API (Local MVP) starting...")
    logger.info(f"📁 Workspace root: {WORKSPACE_ROOT}")
    logger.info(f"🗄️ Database: {DATABASE_PATH}")
    logger.info(f"🔗 CSN Server: {CSN_SERVER_URL}")

    # Initialize SQLite database
    init_database()

    # Initialize MutationLog (Append-only Audit Trail)
    MutationLog.initialize(
        log_file_path="./data/mutation_log.jsonl",
        blockchain_db_path="./data/genomos.db"
    )
    logger.info("📜 MutationLog initialized (Triadisk Portvokter #3)")

    # Initialize GENOMOS DNA Blockchain
    blockchain = initialize_dna_blockchain(db_path="./data/genomos.db")
    logger.info("🧬 GENOMOS DNA Blockchain initialized for API queries")

    # Initialize Google Workspace Integration (if configured)
    try:
        # Check if Google Workspace environment variables are set
        client_secret_file = os.getenv("GOOGLE_CLIENT_SECRET_FILE")
        token_file = os.getenv("GOOGLE_TOKEN_FILE", "./credentials/token.json")
        drive_folder_id = os.getenv("GOOGLE_DRIVE_FOLDER_ID")
        sheets_spreadsheet_id = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID")

        if client_secret_file and drive_folder_id and sheets_spreadsheet_id:
            # Initialize Google Drive Manager
            logger.info("🔄 Initializing Google Drive Manager...")
            drive_manager = initialize_drive_manager(
                client_secret_file=client_secret_file,
                token_file=token_file,
                folder_id=drive_folder_id
            )
            logger.info("✅ Google Drive Manager initialized")

            # Initialize Google Sheets Manager
            logger.info("🔄 Initializing Google Sheets Manager...")
            sheets_manager = initialize_sheets_manager(
                credentials=drive_manager.credentials,
                spreadsheet_id=sheets_spreadsheet_id
            )
            logger.info("✅ Google Sheets Manager initialized")

            # Initialize Scheduler (automated backup, pattern analysis, metrics)
            logger.info("🔄 Initializing Scheduler...")
            backup_hour = int(os.getenv("BACKUP_SCHEDULE_HOUR", "2"))
            pattern_interval = int(os.getenv("PATTERN_ANALYSIS_INTERVAL_HOURS", "6"))

            scheduler = initialize_scheduler(
                blockchain=blockchain,
                drive_manager=drive_manager,
                sheets_manager=sheets_manager,
                backup_hour=backup_hour,
                pattern_interval_hours=pattern_interval
            )
            logger.info(f"✅ Scheduler initialized (backup: {backup_hour}:00, pattern analysis: every {pattern_interval}h)")
        else:
            logger.info("ℹ️  Google Workspace not configured (missing environment variables)")
    except Exception as e:
        logger.warning(f"⚠️  Google Workspace initialization failed: {e}")
        logger.info("   Continuing without Google Workspace integration")

    # Create agent-specific directories
    agent_dirs = ["manus", "code", "lira", "orion", "abacus", "nyra", "thalus", "aurora", "thalamus", "scribe", "zara", "shared", "experiments"]
    for agent_dir in agent_dirs:
        (WORKSPACE_ROOT / agent_dir).mkdir(parents=True, exist_ok=True)

    logger.info(f"✅ Created {len(agent_dirs)} agent directories")

    # Mount MCP server - exposes all FastAPI endpoints as MCP tools
    # This enables standardized agent-to-resource communication
    mcp.mount()
    logger.info("🔌 MCP server mounted at /mcp")
    logger.info("✨ All workspace operations now available as MCP tools")

    # Start Redis subscriber in background thread
    global subscriber_thread
    if ubuntu_subscriber.enabled:
        subscriber_thread = threading.Thread(
            target=ubuntu_subscriber.start_polling,
            args=(5,),  # Poll every 5 seconds
            daemon=True
        )
        subscriber_thread.start()
        logger.info("🚀 Redis subscriber started in background thread")
    else:
        logger.info("⚠️  Redis subscriber not enabled (missing credentials)")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("🛑 Ubuntu Playground API shutting down...")

    # Stop scheduler if running
    try:
        from scripts.scheduled_jobs import get_scheduler
        scheduler = get_scheduler()
        if scheduler:
            scheduler.stop()
            logger.info("✅ Scheduler stopped")
    except Exception as e:
        logger.warning(f"⚠️  Scheduler shutdown warning: {e}")

    # Stop Redis subscriber
    if subscriber_thread and subscriber_thread.is_alive():
        ubuntu_subscriber.stop()
        subscriber_thread.join(timeout=5)
        logger.info("✅ Redis subscriber stopped")

    # Close binary Redis connection if exists
    if REDIS_CLIENT:
        REDIS_CLIENT.close()
        logger.info("✅ Redis connection closed")
