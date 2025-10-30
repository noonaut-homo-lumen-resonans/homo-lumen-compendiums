"""Vercel Connector (stub - add token later)"""
import os
import logging

logger = logging.getLogger(__name__)

class VercelConnector:
    def __init__(self):
        self.token = os.getenv("VERCEL_TOKEN")
        self.enabled = bool(self.token)
        if self.enabled:
            logger.info("✅ Vercel initialized")
        else:
            logger.warning("⚠️ Vercel not configured - add VERCEL_TOKEN to .env")

    def get_status(self):
        return {
            "name": "Vercel",
            "enabled": self.enabled,
            "message": "Add VERCEL_TOKEN to enable" if not self.enabled else "Ready"
        }
