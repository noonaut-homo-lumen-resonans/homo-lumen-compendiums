# Connector Implementation - Complete Code
**Status:** Ready to implement
**Created:** 30. oktober 2025

---

## Quick Summary

Jeg har opprettet:
1. ✅ [API_KEYS_SETUP_GUIDE.md](docs/API_KEYS_SETUP_GUIDE.md) - Steg-for-steg guide for å få API-nøkler
2. ✅ [MCP_INTEGRATION_PLAN.md](docs/MCP_INTEGRATION_PLAN.md) - Komplett plan for MCP-integrasjoner
3. ⏳ Kode nedenfor - Klar til å copy-paste

**Din action:**
1. Få API-nøklene (følg API_KEYS_SETUP_GUIDE.md)
2. Copy-paste koden nedenfor til riktige filer
3. Installer dependencies
4. Start serveren

---

## File 1: `api/connectors/vertex_ai_connector.py`

```python
"""
Vertex AI Connector
Provides multi-modal LLM capabilities via Google Cloud Vertex AI
"""

import os
import logging
from typing import Optional, List, Dict, Any
from google.cloud import aiplatform
from google.oauth2 import service_account
from vertexai.preview.generative_models import GenerativeModel, Part, GenerationConfig

logger = logging.getLogger(__name__)

class VertexAIConnector:
    """
    Connector for Google Cloud Vertex AI

    Features:
    - Multi-modal LLM (text, images, video)
    - Gemini Pro and Gemini Pro Vision
    - Production-ready AI models
    """

    def __init__(self):
        """Initialize Vertex AI with credentials"""
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        self.location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
        self.credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

        if not self.project_id:
            logger.warning("⚠️ GOOGLE_CLOUD_PROJECT not set - Vertex AI disabled")
            self.enabled = False
            return

        try:
            # Initialize Vertex AI
            if self.credentials_path and os.path.exists(self.credentials_path):
                credentials = service_account.Credentials.from_service_account_file(
                    self.credentials_path
                )
                aiplatform.init(
                    project=self.project_id,
                    location=self.location,
                    credentials=credentials
                )
            else:
                # Use default credentials (for Cloud Run, GKE, etc.)
                aiplatform.init(
                    project=self.project_id,
                    location=self.location
                )

            self.enabled = True
            logger.info(f"✅ Vertex AI initialized - Project: {self.project_id}, Location: {self.location}")

        except Exception as e:
            logger.error(f"❌ Failed to initialize Vertex AI: {e}")
            self.enabled = False

    async def generate_text(
        self,
        prompt: str,
        model: str = "gemini-pro",
        temperature: float = 0.7,
        max_tokens: int = 1024
    ) -> Optional[str]:
        """
        Generate text using Vertex AI

        Args:
            prompt: Text prompt
            model: Model name (gemini-pro, gemini-pro-vision, etc.)
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate

        Returns:
            Generated text or None if error
        """
        if not self.enabled:
            logger.warning("Vertex AI not enabled")
            return None

        try:
            model_instance = GenerativeModel(model)

            generation_config = GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens
            )

            response = await model_instance.generate_content_async(
                prompt,
                generation_config=generation_config
            )

            return response.text

        except Exception as e:
            logger.error(f"Vertex AI generation error: {e}")
            return None

    async def analyze_image(
        self,
        image_bytes: bytes,
        prompt: str = "Describe this image in detail",
        mime_type: str = "image/jpeg"
    ) -> Optional[str]:
        """
        Analyze image using Gemini Pro Vision

        Args:
            image_bytes: Image data
            prompt: Analysis prompt
            mime_type: Image MIME type

        Returns:
            Image analysis or None if error
        """
        if not self.enabled:
            logger.warning("Vertex AI not enabled")
            return None

        try:
            model = GenerativeModel("gemini-pro-vision")

            image_part = Part.from_data(image_bytes, mime_type=mime_type)

            response = await model.generate_content_async([image_part, prompt])

            return response.text

        except Exception as e:
            logger.error(f"Vertex AI image analysis error: {e}")
            return None

    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: str = "gemini-pro",
        temperature: float = 0.7
    ) -> Optional[str]:
        """
        Multi-turn chat conversation

        Args:
            messages: List of {"role": "user"/"model", "content": "..."}
            model: Model name
            temperature: Sampling temperature

        Returns:
            Response text or None if error
        """
        if not self.enabled:
            logger.warning("Vertex AI not enabled")
            return None

        try:
            model_instance = GenerativeModel(model)
            chat = model_instance.start_chat()

            # Send all messages except the last one
            for msg in messages[:-1]:
                if msg["role"] == "user":
                    await chat.send_message_async(msg["content"])

            # Send final message and get response
            final_message = messages[-1]["content"]
            response = await chat.send_message_async(final_message)

            return response.text

        except Exception as e:
            logger.error(f"Vertex AI chat error: {e}")
            return None

    def get_status(self) -> Dict[str, Any]:
        """Get connector status"""
        return {
            "name": "Vertex AI",
            "enabled": self.enabled,
            "project": self.project_id if self.enabled else None,
            "location": self.location if self.enabled else None,
            "models": ["gemini-pro", "gemini-pro-vision"] if self.enabled else []
        }
```

---

## File 2: `api/connectors/vercel_connector.py`

```python
"""
Vercel Connector
Manages deployments and project configuration on Vercel
"""

import os
import logging
import aiohttp
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)

class VercelConnector:
    """
    Connector for Vercel deployment platform

    Features:
    - Trigger deployments
    - Check deployment status
    - Manage project settings
    - Get deployment logs
    """

    def __init__(self):
        """Initialize Vercel connector"""
        self.token = os.getenv("VERCEL_TOKEN")
        self.team_id = os.getenv("VERCEL_TEAM_ID")
        self.project_id = os.getenv("VERCEL_PROJECT_ID")
        self.base_url = "https://api.vercel.com"

        if not self.token:
            logger.warning("⚠️ VERCEL_TOKEN not set - Vercel connector disabled")
            self.enabled = False
        else:
            self.enabled = True
            logger.info(f"✅ Vercel connector initialized - Project: {self.project_id}")

    async def deploy_project(
        self,
        project_name: Optional[str] = None,
        git_ref: str = "main"
    ) -> Optional[Dict[str, Any]]:
        """
        Trigger deployment for a project

        Args:
            project_name: Project name (uses VERCEL_PROJECT_ID if None)
            git_ref: Git branch/tag to deploy

        Returns:
            Deployment info or None if error
        """
        if not self.enabled:
            logger.warning("Vercel not enabled")
            return None

        project_name = project_name or self.project_id

        if not project_name:
            logger.error("No project specified")
            return None

        try:
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }

            payload = {
                "name": project_name,
                "gitSource": {
                    "type": "github",
                    "ref": git_ref
                }
            }

            if self.team_id:
                payload["teamId"] = self.team_id

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/v13/deployments",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        logger.info(f"✅ Deployment triggered: {data.get('url')}")
                        return data
                    else:
                        error_text = await response.text()
                        logger.error(f"❌ Deployment failed: {error_text}")
                        return None

        except Exception as e:
            logger.error(f"Vercel deployment error: {e}")
            return None

    async def get_deployment_status(self, deployment_id: str) -> Optional[Dict[str, Any]]:
        """
        Check deployment status

        Args:
            deployment_id: Deployment ID

        Returns:
            Deployment status or None if error
        """
        if not self.enabled:
            return None

        try:
            headers = {"Authorization": f"Bearer {self.token}"}

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/v13/deployments/{deployment_id}",
                    headers=headers
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"Failed to get deployment status: {response.status}")
                        return None

        except Exception as e:
            logger.error(f"Vercel status check error: {e}")
            return None

    async def list_deployments(
        self,
        project_id: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        List recent deployments

        Args:
            project_id: Project ID (uses VERCEL_PROJECT_ID if None)
            limit: Maximum deployments to return

        Returns:
            List of deployments
        """
        if not self.enabled:
            return []

        project_id = project_id or self.project_id

        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            params = {"limit": limit}

            if project_id:
                params["projectId"] = project_id

            if self.team_id:
                params["teamId"] = self.team_id

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/v6/deployments",
                    headers=headers,
                    params=params
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("deployments", [])
                    else:
                        logger.error(f"Failed to list deployments: {response.status}")
                        return []

        except Exception as e:
            logger.error(f"Vercel list error: {e}")
            return []

    async def list_projects(self) -> List[Dict[str, Any]]:
        """
        List all Vercel projects

        Returns:
            List of projects
        """
        if not self.enabled:
            return []

        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            params = {}

            if self.team_id:
                params["teamId"] = self.team_id

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/v9/projects",
                    headers=headers,
                    params=params
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("projects", [])
                    else:
                        logger.error(f"Failed to list projects: {response.status}")
                        return []

        except Exception as e:
            logger.error(f"Vercel projects error: {e}")
            return []

    def get_status(self) -> Dict[str, Any]:
        """Get connector status"""
        return {
            "name": "Vercel",
            "enabled": self.enabled,
            "project_id": self.project_id if self.enabled else None,
            "team_id": self.team_id if self.enabled else None
        }
```

---

## File 3: `api/connectors/elevenlabs_connector.py`

```python
"""
ElevenLabs Connector
Text-to-Speech for Lira voice chatbot
"""

import os
import logging
import aiohttp
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)

class ElevenLabsConnector:
    """
    Connector for ElevenLabs Text-to-Speech API

    Features:
    - Convert text to speech (Lira voice)
    - Multiple voice options
    - Adjustable voice settings
    - Streaming audio support
    """

    def __init__(self):
        """Initialize ElevenLabs connector"""
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        self.base_url = "https://api.elevenlabs.io/v1"

        # Lira's voice configuration
        self.lira_voice_id = os.getenv(
            "ELEVENLABS_VOICE_ID_LIRA",
            "21m00Tcm4TlvDq8ikWAM"  # Rachel (default)
        )

        # Voice settings
        self.stability = float(os.getenv("ELEVENLABS_STABILITY", "0.75"))
        self.similarity_boost = float(os.getenv("ELEVENLABS_SIMILARITY_BOOST", "0.75"))
        self.style = float(os.getenv("ELEVENLABS_STYLE", "0.5"))

        if not self.api_key:
            logger.warning("⚠️ ELEVENLABS_API_KEY not set - ElevenLabs disabled")
            self.enabled = False
        else:
            self.enabled = True
            logger.info(f"✅ ElevenLabs initialized - Lira voice: {self.lira_voice_id}")

    async def text_to_speech(
        self,
        text: str,
        voice_id: Optional[str] = None,
        stability: Optional[float] = None,
        similarity_boost: Optional[float] = None,
        style: Optional[float] = None
    ) -> Optional[bytes]:
        """
        Convert text to speech

        Args:
            text: Text to convert
            voice_id: Voice ID (uses Lira's voice if None)
            stability: Voice stability (0-1)
            similarity_boost: Voice similarity boost (0-1)
            style: Style exaggeration (0-1)

        Returns:
            Audio bytes (MP3) or None if error
        """
        if not self.enabled:
            logger.warning("ElevenLabs not enabled")
            return None

        voice_id = voice_id or self.lira_voice_id
        stability = stability if stability is not None else self.stability
        similarity_boost = similarity_boost if similarity_boost is not None else self.similarity_boost
        style = style if style is not None else self.style

        try:
            headers = {
                "xi-api-key": self.api_key,
                "Content-Type": "application/json"
            }

            payload = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": stability,
                    "similarity_boost": similarity_boost,
                    "style": style
                }
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/text-to-speech/{voice_id}",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        audio_bytes = await response.read()
                        logger.info(f"✅ Generated speech: {len(audio_bytes)} bytes")
                        return audio_bytes
                    else:
                        error_text = await response.text()
                        logger.error(f"❌ TTS failed: {error_text}")
                        return None

        except Exception as e:
            logger.error(f"ElevenLabs TTS error: {e}")
            return None

    async def list_voices(self) -> List[Dict[str, Any]]:
        """
        Get available voices

        Returns:
            List of voice information
        """
        if not self.enabled:
            return []

        try:
            headers = {"xi-api-key": self.api_key}

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/voices",
                    headers=headers
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("voices", [])
                    else:
                        logger.error(f"Failed to list voices: {response.status}")
                        return []

        except Exception as e:
            logger.error(f"ElevenLabs list voices error: {e}")
            return []

    async def get_voice_info(self, voice_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get information about a specific voice

        Args:
            voice_id: Voice ID (uses Lira's voice if None)

        Returns:
            Voice information or None if error
        """
        if not self.enabled:
            return None

        voice_id = voice_id or self.lira_voice_id

        try:
            headers = {"xi-api-key": self.api_key}

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/voices/{voice_id}",
                    headers=headers
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"Failed to get voice info: {response.status}")
                        return None

        except Exception as e:
            logger.error(f"ElevenLabs voice info error: {e}")
            return None

    def get_status(self) -> Dict[str, Any]:
        """Get connector status"""
        return {
            "name": "ElevenLabs",
            "enabled": self.enabled,
            "lira_voice_id": self.lira_voice_id if self.enabled else None,
            "voice_settings": {
                "stability": self.stability,
                "similarity_boost": self.similarity_boost,
                "style": self.style
            } if self.enabled else None
        }
```

---

## File 4: Update `api/routers/connector_status.py` (NEW)

```python
"""
Connector Status Router
Provides status information for all connectors
"""

from fastapi import APIRouter
from typing import Dict, Any
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Import connectors (will be None if credentials missing)
try:
    from connectors import VertexAIConnector, VercelConnector, ElevenLabsConnector
    CONNECTORS_AVAILABLE = True
except Exception as e:
    logger.warning(f"Connectors not available: {e}")
    CONNECTORS_AVAILABLE = False

@router.get("/api/connectors/status")
async def get_connectors_status() -> Dict[str, Any]:
    """
    Get status of all connectors

    Returns:
        Status of Vertex AI, Vercel, and ElevenLabs connectors
    """
    if not CONNECTORS_AVAILABLE:
        return {
            "available": False,
            "message": "Connectors not initialized - check environment variables"
        }

    try:
        vertex_ai = VertexAIConnector()
        vercel = VercelConnector()
        elevenlabs = ElevenLabsConnector()

        return {
            "available": True,
            "connectors": {
                "vertex_ai": vertex_ai.get_status(),
                "vercel": vercel.get_status(),
                "elevenlabs": elevenlabs.get_status()
            }
        }

    except Exception as e:
        logger.error(f"Error getting connector status: {e}")
        return {
            "available": False,
            "error": str(e)
        }

@router.post("/api/lira/speak")
async def lira_speak(text: str) -> Dict[str, Any]:
    """
    Make Lira speak using ElevenLabs

    Args:
        text: Text for Lira to speak

    Returns:
        Audio URL or error
    """
    if not CONNECTORS_AVAILABLE:
        return {"error": "ElevenLabs not available"}

    try:
        elevenlabs = ElevenLabsConnector()

        if not elevenlabs.enabled:
            return {"error": "ElevenLabs not enabled - check API key"}

        audio_bytes = await elevenlabs.text_to_speech(text)

        if not audio_bytes:
            return {"error": "Failed to generate speech"}

        # TODO: Save audio to file or stream directly
        return {
            "success": True,
            "audio_length": len(audio_bytes),
            "message": "Audio generated successfully"
        }

    except Exception as e:
        logger.error(f"Lira speak error: {e}")
        return {"error": str(e)}
```

---

## File 5: Update `api/main.py` to include new router

Add these lines to `main.py`:

```python
# Import connector status router
from routers.connector_status import router as connector_router

# Include connector status router
app.include_router(connector_router)
logger.info("SUCCESS: Connector status router included")
```

---

## File 6: Update `api/requirements.txt`

Add these dependencies:

```txt
# Existing dependencies...

# Vertex AI (Google Cloud)
google-cloud-aiplatform>=1.38.0
vertexai>=0.0.1

# Vercel API (uses aiohttp - already in requirements)
aiohttp>=3.9.0

# ElevenLabs API (uses aiohttp)
# No specific package needed - using REST API directly
```

---

## Installation Steps

```bash
# 1. Install new dependencies
cd c:\Users\onigo\NAV LOSEN\homo-lumen-compendiums\ubuntu-playground\api
pip install google-cloud-aiplatform vertexai

# 2. Create credentials directory
mkdir -p ../credentials

# 3. Add API keys to .env (after getting them from API_KEYS_SETUP_GUIDE.md)
# See .env template below

# 4. Restart server
# Server will auto-reload if already running with --reload flag
```

---

## .env Template

Add to `ubuntu-playground/api/.env`:

```bash
# ===========================================
# VERTEX AI (Google Cloud)
# ===========================================
GOOGLE_CLOUD_PROJECT=homo-lumen-project
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=../credentials/homo-lumen-project-1234567890ab.json

# ===========================================
# VERCEL
# ===========================================
VERCEL_TOKEN=vercel_1a2b3c4d5e6f7g8h9i0j
VERCEL_TEAM_ID=team_abc123xyz  # Optional
VERCEL_PROJECT_ID=prj_abc123xyz  # NAV-Losen

# ===========================================
# ELEVENLABS (Lira Voice)
# ===========================================
ELEVENLABS_API_KEY=sk_abc123def456ghi789jkl
ELEVENLABS_VOICE_ID_LIRA=21m00Tcm4TlvDq8ikWAM

# Voice settings
ELEVENLABS_STABILITY=0.75
ELEVENLABS_SIMILARITY_BOOST=0.75
ELEVENLABS_STYLE=0.5
```

---

## Testing

### Test 1: Check connector status
```bash
curl http://localhost:8004/api/connectors/status | python -m json.tool
```

**Expected output:**
```json
{
  "available": true,
  "connectors": {
    "vertex_ai": {
      "name": "Vertex AI",
      "enabled": true,
      "project": "homo-lumen-project",
      "location": "us-central1",
      "models": ["gemini-pro", "gemini-pro-vision"]
    },
    "vercel": {
      "name": "Vercel",
      "enabled": true,
      "project_id": "prj_abc123xyz"
    },
    "elevenlabs": {
      "name": "ElevenLabs",
      "enabled": true,
      "lira_voice_id": "21m00Tcm4TlvDq8ikWAM"
    }
  }
}
```

### Test 2: Make Lira speak
```bash
curl -X POST http://localhost:8004/api/lira/speak \
  -H "Content-Type: application/json" \
  -d '{"text": "Hei, jeg er Lira. Jeg er her for å hjelpe deg!"}'
```

---

## Next Steps

1. ✅ Get API keys (follow API_KEYS_SETUP_GUIDE.md)
2. ✅ Copy-paste all code above to respective files
3. ✅ Install dependencies (`pip install google-cloud-aiplatform vertexai`)
4. ✅ Add API keys to .env
5. ✅ Restart server
6. ✅ Test connectors

---

**Estimated time:** 45 minutes (30 min for API keys + 15 min for implementation)

**Status:** Ready to implement! 🚀
