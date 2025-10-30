"""
Health Connect API - Real-Time Biofelt Data Synchronization

Receives biofelt data from mobile devices (Google Health Connect, Apple HealthKit, etc.)
and makes it available for consciousness-aware AI consultations.

Philosophy: "The body knows before the mind understands"
"""

from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime, timedelta
import logging
from enum import Enum

# Import BiofeltContext for validation
from gates import BiofeltContext, BiofeltGate, ResonanceLevel

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/health", tags=["Health Connect"])

# ============================================================================
# DATA MODELS
# ============================================================================

class HealthDataSource(str, Enum):
    """Source of health data"""
    GOOGLE_HEALTH_CONNECT = "google_health_connect"
    APPLE_HEALTHKIT = "apple_healthkit"
    SAMSUNG_HEALTH = "samsung_health"
    FITBIT = "fitbit"
    GARMIN = "garmin"
    MANUAL = "manual"
    SIMULATED = "simulated"


class HealthMetrics(BaseModel):
    """Health metrics from wearable/mobile device"""
    hrv_ms: float = Field(..., description="Heart Rate Variability in milliseconds", ge=0, le=200)
    heart_rate_bpm: Optional[float] = Field(None, description="Heart rate in beats per minute", ge=30, le=220)
    coherence: float = Field(..., description="Heart coherence level (0-1)", ge=0, le=1)
    stress_level: float = Field(0, description="Stress level (0-10)", ge=0, le=10)
    energy_level: str = Field("balanced", description="Energy level assessment")
    pust_rytme: str = Field("4-6-8", description="Breathing pattern")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class HealthSyncRequest(BaseModel):
    """Request to sync health data from mobile device"""
    user_id: str = Field(..., description="User identifier")
    device_id: str = Field(..., description="Device identifier")
    source: HealthDataSource = Field(..., description="Data source")
    metrics: HealthMetrics
    metadata: Optional[Dict] = Field(default_factory=dict)


class HealthSyncResponse(BaseModel):
    """Response after syncing health data"""
    success: bool
    message: str
    resonance_level: ResonanceLevel
    recommendations: List[str] = []
    biofelt_validation: Dict


# ============================================================================
# IN-MEMORY CACHE (Replace with Redis in production)
# ============================================================================

class HealthDataCache:
    """In-memory cache for latest health data per user"""

    def __init__(self):
        self._cache: Dict[str, HealthMetrics] = {}
        self._last_updated: Dict[str, datetime] = {}

    def set(self, user_id: str, metrics: HealthMetrics):
        """Store latest health metrics for user"""
        self._cache[user_id] = metrics
        self._last_updated[user_id] = datetime.utcnow()
        logger.info(f"📊 Health data cached for user {user_id}: HRV={metrics.hrv_ms}ms")

    def get(self, user_id: str) -> Optional[HealthMetrics]:
        """Get latest health metrics for user"""
        if user_id not in self._cache:
            return None

        # Check if data is stale (older than 5 minutes)
        last_update = self._last_updated.get(user_id)
        if last_update and (datetime.utcnow() - last_update) > timedelta(minutes=5):
            logger.warning(f"⚠️ Health data for user {user_id} is stale (>5 min old)")

        return self._cache.get(user_id)

    def get_all_active(self, max_age_minutes: int = 5) -> Dict[str, HealthMetrics]:
        """Get all active users with recent health data"""
        cutoff = datetime.utcnow() - timedelta(minutes=max_age_minutes)
        active = {}

        for user_id, last_update in self._last_updated.items():
            if last_update > cutoff:
                active[user_id] = self._cache[user_id]

        return active


# Global cache instance
health_cache = HealthDataCache()


# ============================================================================
# API ENDPOINTS
# ============================================================================

@router.post("/sync", response_model=HealthSyncResponse)
async def sync_health_data(request: HealthSyncRequest):
    """
    Sync health data from mobile device.

    This endpoint receives real-time biofelt data from:
    - Google Health Connect (Android)
    - Apple HealthKit (iOS)
    - Wearable devices (Fitbit, Garmin, etc.)

    The data is cached and made available for AI consultations.
    """
    try:
        logger.info(f"🔄 Health sync request from {request.source.value} for user {request.user_id}")
        logger.info(f"   HRV: {request.metrics.hrv_ms}ms, Coherence: {request.metrics.coherence}")

        # Store in cache
        health_cache.set(request.user_id, request.metrics)

        # Create BiofeltContext for validation
        biofelt_context = BiofeltContext(
            hrv_ms=request.metrics.hrv_ms,
            coherence=request.metrics.coherence,
            pust_rytme=request.metrics.pust_rytme,
            energy_level=request.metrics.energy_level,
            stress_indicators=[
                f"Stress level: {request.metrics.stress_level}"
            ] if request.metrics.stress_level > 5 else [],
            timestamp=request.metrics.timestamp.isoformat()
        )

        # Validate using BiofeltGate
        validation_result = BiofeltGate.validate_critical_operation(
            biofelt=biofelt_context,
            operation_type="read"
        )

        logger.info(f"✅ Health data synced successfully. Resonance: {validation_result.resonance_level.value}")

        return HealthSyncResponse(
            success=True,
            message=f"Health data synced successfully from {request.source.value}",
            resonance_level=validation_result.resonance_level,
            recommendations=validation_result.recommendations,
            biofelt_validation={
                "allowed": validation_result.allowed,
                "hrv_status": validation_result.hrv_status,
                "coherence_status": validation_result.coherence_status,
                "message": validation_result.message
            }
        )

    except Exception as e:
        logger.error(f"❌ Health sync error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Health sync failed: {str(e)}")


@router.get("/latest/{user_id}")
async def get_latest_health_data(user_id: str):
    """
    Get the latest health data for a specific user.

    Returns:
    - Latest biofelt metrics
    - Resonance level
    - Age of data
    - Recommendations
    """
    try:
        metrics = health_cache.get(user_id)

        if not metrics:
            raise HTTPException(
                status_code=404,
                detail=f"No health data found for user {user_id}. Please sync from mobile device first."
            )

        # Calculate data age
        data_age_seconds = (datetime.utcnow() - metrics.timestamp).total_seconds()

        # Create BiofeltContext
        biofelt_context = BiofeltContext(
            hrv_ms=metrics.hrv_ms,
            coherence=metrics.coherence,
            pust_rytme=metrics.pust_rytme,
            energy_level=metrics.energy_level,
            stress_indicators=[],
            timestamp=metrics.timestamp.isoformat()
        )

        # Get resonance level
        resonance_level = BiofeltGate.get_resonance_level(metrics.hrv_ms)

        return {
            "user_id": user_id,
            "metrics": metrics.dict(),
            "resonance_level": resonance_level.value,
            "data_age_seconds": round(data_age_seconds, 1),
            "is_stale": data_age_seconds > 300,  # 5 minutes
            "biofelt_context": biofelt_context.dict()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error fetching health data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch health data: {str(e)}")


@router.get("/active")
async def get_active_users():
    """
    Get all users with active (recent) health data.

    Returns list of users who have synced data within the last 5 minutes.
    """
    try:
        active_users = health_cache.get_all_active(max_age_minutes=5)

        return {
            "active_count": len(active_users),
            "users": [
                {
                    "user_id": user_id,
                    "hrv_ms": metrics.hrv_ms,
                    "resonance_level": BiofeltGate.get_resonance_level(metrics.hrv_ms).value,
                    "timestamp": metrics.timestamp.isoformat()
                }
                for user_id, metrics in active_users.items()
            ]
        }

    except Exception as e:
        logger.error(f"❌ Error fetching active users: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch active users: {str(e)}")


@router.get("/status")
async def health_connect_status():
    """
    Get Health Connect API status.

    Returns information about the service and cached data.
    """
    active_users = health_cache.get_all_active(max_age_minutes=5)

    return {
        "service": "Health Connect API",
        "status": "operational",
        "version": "1.0.0",
        "active_users": len(active_users),
        "cache_type": "in-memory",
        "data_retention": "5 minutes",
        "supported_sources": [source.value for source in HealthDataSource],
        "philosophy": "The body knows before the mind understands"
    }


# ============================================================================
# HELPER FUNCTION FOR CONSULTATION INTEGRATION
# ============================================================================

def get_user_biofelt_context(user_id: str = "default") -> BiofeltContext:
    """
    Get BiofeltContext for a user, either from Health Connect cache or simulated.

    This function is used by the consultation API to get real-time biofelt data.
    """
    metrics = health_cache.get(user_id)

    if metrics:
        logger.info(f"📱 Using real Health Connect data for user {user_id}: HRV={metrics.hrv_ms}ms")
        return BiofeltContext(
            hrv_ms=metrics.hrv_ms,
            coherence=metrics.coherence,
            pust_rytme=metrics.pust_rytme,
            energy_level=metrics.energy_level,
            stress_indicators=[],
            timestamp=metrics.timestamp.isoformat()
        )
    else:
        # Fallback to simulated data
        logger.info(f"🎭 No Health Connect data for user {user_id}, using simulated data")
        import random
        return BiofeltContext(
            hrv_ms=75.0 + random.uniform(-10, 15),
            coherence=0.8 + random.uniform(-0.1, 0.1),
            pust_rytme="4-6-8",
            energy_level="balanced",
            stress_indicators=[],
            timestamp=datetime.utcnow().isoformat()
        )
