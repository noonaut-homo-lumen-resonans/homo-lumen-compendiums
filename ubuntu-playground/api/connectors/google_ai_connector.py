"""Google AI / Gemini Connector"""
import os
import logging
import google.generativeai as genai

logger = logging.getLogger(__name__)

class GoogleAIConnector:
    def __init__(self):
        api_key = os.getenv("GOOGLE_AI_STUDIO_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.enabled = True
            logger.info("✅ Google AI initialized")
        else:
            self.enabled = False
            logger.warning("⚠️ Google AI not configured")

    async def generate_text(self, prompt: str, model: str = "gemini-pro"):
        if not self.enabled:
            return None
        try:
            model_instance = genai.GenerativeModel(model)
            response = await model_instance.generate_content_async(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Google AI error: {e}")
            return None

    def get_status(self):
        return {
            "name": "Google AI / Gemini",
            "enabled": self.enabled,
            "models": ["gemini-pro", "gemini-pro-vision"] if self.enabled else []
        }
