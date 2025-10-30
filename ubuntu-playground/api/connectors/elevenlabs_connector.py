"""ElevenLabs TTS Connector"""
import os
import logging
import aiohttp

logger = logging.getLogger(__name__)

class ElevenLabsConnector:
    def __init__(self):
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        self.voice_id = os.getenv("ELEVENLABS_VOICE_ID_LIRA", "21m00Tcm4TlvDq8ikWAM")
        self.enabled = bool(self.api_key)
        if self.enabled:
            logger.info(f"✅ ElevenLabs initialized - Voice: {self.voice_id}")
        else:
            logger.warning("⚠️ ElevenLabs not configured")

    async def text_to_speech(self, text: str):
        if not self.enabled:
            return None
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}",
                    headers={"xi-api-key": self.api_key, "Content-Type": "application/json"},
                    json={"text": text, "model_id": "eleven_monolingual_v1"}
                ) as response:
                    if response.status == 200:
                        return await response.read()
            return None
        except Exception as e:
            logger.error(f"ElevenLabs error: {e}")
            return None

    def get_status(self):
        return {
            "name": "ElevenLabs",
            "enabled": self.enabled,
            "voice_id": self.voice_id if self.enabled else None
        }
