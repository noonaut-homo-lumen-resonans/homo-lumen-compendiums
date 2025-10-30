# DO THIS NOW - Implementation Steps
**Time:** 10 minutes total
**Status:** All code is ready!

---

## ✅ Already Done:
1. ✅ Supabase migration (tabeller opprettet)
2. ✅ `.env` file created with all API keys
3. ✅ NAV Jobs backend & frontend (fungerer)

---

## 🚀 DO THIS (in order):

### Step 1: Install Dependency (1 min)
```bash
cd "c:\Users\onigo\NAV LOSEN\homo-lumen-compendiums\ubuntu-playground\api"
pip install google-generativeai
```

### Step 2: Copy All Connector Files (5 min)

**Open this file:**
```
c:\Users\onigo\NAV LOSEN\homo-lumen-compendiums\ubuntu-playground\CONNECTOR_IMPLEMENTATION_COMPLETE.md
```

**Copy-paste these 5 code blocks to create 5 files:**

1. Copy code from "File 1" → Create:
   ```
   api/connectors/vertex_ai_connector.py
   ```

2. Copy code from "File 2" → Create:
   ```
   api/connectors/vercel_connector.py
   ```

3. Copy code from "File 3" → Create:
   ```
   api/connectors/elevenlabs_connector.py
   ```

4. Copy code from "File 4" → Create:
   ```
   api/routers/connector_status.py
   ```

5. Copy code from "File 5" → Update:
   ```
   api/main.py
   ```
   (Add these lines to main.py)

**OR use the simple connector versions in this file below!**

---

### Step 3: Server Auto-Reload (0 min - happens automatically!)

Server is already running with `--reload` flag.
When you save files, server restarts automatically.

---

### Step 4: Test! (2 min)

```bash
# Test 1: Connector status
curl http://localhost:8004/api/connectors/status | python -m json.tool

# Test 2: Lira speaks!
curl -X POST http://localhost:8004/api/lira/speak \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"Hei, jeg er Lira!\"}"
```

---

## ⚡ ULTRA-QUICK METHOD (if CONNECTOR_IMPLEMENTATION_COMPLETE.md is too long):

I'll create simplified versions below. Just copy-paste!

---

## 📄 Simplified Connector Files (Copy These!)

### File 1: `api/connectors/google_ai_connector.py`

```python
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
```

### File 2: `api/connectors/elevenlabs_connector.py`

```python
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
```

### File 3: `api/connectors/vercel_connector.py`

```python
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
```

### File 4: `api/routers/connector_status.py`

```python
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
```

### File 5: Update `api/main.py`

**Add these lines near the top (after other router imports):**

```python
# Import connector status router
from routers.connector_status import router as connector_router
```

**Add this line after other `app.include_router()` calls:**

```python
# Include connector status router
app.include_router(connector_router)
logger.info("SUCCESS: Connector status router included")
```

---

## ✅ Done!

After copying all files:

1. Server auto-reloads
2. Test with curl commands above
3. Lira can speak! 🎤

---

## 🎯 Expected Results

### Test 1: Status
```json
{
  "available": true,
  "connectors": {
    "google_ai": {
      "name": "Google AI / Gemini",
      "enabled": true,
      "models": ["gemini-pro", "gemini-pro-vision"]
    },
    "elevenlabs": {
      "name": "ElevenLabs",
      "enabled": true,
      "voice_id": "21m00Tcm4TlvDq8ikWAM"
    },
    "vercel": {
      "name": "Vercel",
      "enabled": false,
      "message": "Add VERCEL_TOKEN to enable"
    }
  }
}
```

### Test 2: Lira Speak
```json
{
  "success": true,
  "audio_length": 234567,
  "message": "Generated 234567 bytes of audio"
}
```

---

**Time to complete: 10 minutes!** 🚀

Start now!
