"""Connector Status Router"""
from fastapi import APIRouter
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

try:
    from connectors.google_ai_connector import GoogleAIConnector
    from connectors.elevenlabs_connector import ElevenLabsConnector
    from connectors.vercel_connector import VercelConnector
    CONNECTORS_AVAILABLE = True
except Exception as e:
    logger.warning(f"Connectors not available: {e}")
    CONNECTORS_AVAILABLE = False

@router.get("/api/connectors/status")
async def get_connectors_status():
    if not CONNECTORS_AVAILABLE:
        return {"available": False, "message": "Connectors not initialized"}

    try:
        google_ai = GoogleAIConnector()
        elevenlabs = ElevenLabsConnector()
        vercel = VercelConnector()

        return {
            "available": True,
            "connectors": {
                "google_ai": google_ai.get_status(),
                "elevenlabs": elevenlabs.get_status(),
                "vercel": vercel.get_status()
            }
        }
    except Exception as e:
        return {"available": False, "error": str(e)}

@router.post("/api/lira/speak")
async def lira_speak(text: str):
    if not CONNECTORS_AVAILABLE:
        return {"error": "ElevenLabs not available"}

    try:
        elevenlabs = ElevenLabsConnector()
        if not elevenlabs.enabled:
            return {"error": "ElevenLabs not enabled"}

        audio_bytes = await elevenlabs.text_to_speech(text)
        if audio_bytes:
            return {
                "success": True,
                "audio_length": len(audio_bytes),
                "message": f"Generated {len(audio_bytes)} bytes of audio"
            }
        return {"error": "Failed to generate speech"}
    except Exception as e:
        return {"error": str(e)}
