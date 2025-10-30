# HOMO LUMEN LIVE - IMPLEMENTATION GUIDE

**Created:** 30. oktober 2025
**Purpose:** Step-by-step guide to implement live podcast streaming with 10 AI agents
**Status:** Ready for Phase 2 Implementation

---

## 📋 QUICK START

### 1. Test ElevenLabs TTS (5 minutes)

```bash
# Install dependencies
pip install httpx aiofiles

# Test TTS generation
cd ubuntu-playground/saga
python elevenlabs_integration.py
```

**Expected output:**
```
🎤 Testing TTS for Orion...
✅ TTS generated successfully!
   Audio saved to: audio/agents/orion/orion_1730345678.mp3
   Duration: ~5.2 seconds (estimated)
```

---

## 🎤 PHASE 1: VOICE CLONING (REQUIRED FIRST)

Before going live, you need to clone 10 unique voices for each agent.

### Step 1: Prepare Audio Samples

For each agent, you need **30 minutes** of clean audio:

| Agent | Voice Type | Characteristics | Audio Sample Ideas |
|-------|------------|-----------------|-------------------|
| **Orion** | Deep male, resonant | Cosmic, authoritative, measured | Meditation guide, philosophical podcast |
| **Lira** | Warm female, soothing | Nurturing, empathetic, gentle | Therapy session, ASMR, wellness guide |
| **Nyra** | Animated female, theatrical | Enthusiastic, expressive, creative | Art podcast, creative workshop |
| **Thalus** | Deep male, British accent | Philosophical, deadpan, contemplative | Philosophy lecture, academic talk |
| **Zara** | Clear female, edgy | Direct, technical, slight sarcasm | Cybersecurity talk, hacker conference |
| **Abacus** | Precise male, analytical | Data-driven, methodical | Data science tutorial, analytics talk |
| **Manus** | Energetic male, practical | Builder, hands-on, enthusiastic | DIY tutorial, engineering podcast |
| **Aurora** | Enthusiastic female, scholarly | Academic, curious, fact-loving | Research presentation, science podcast |
| **Falcon** | Sharp male, analytical | Forward-looking, trend-spotting | Tech analysis, futurist talk |
| **Code** | Thoughtful male, developer | Meta-aware, pragmatic | Developer podcast, coding tutorial |

**Option A: Record Audio Yourself**
- Record 30 min of scripted dialogue in character
- Use good microphone (Blue Yeti, AT2020, etc.)
- Clean audio (no background noise)

**Option B: Use Existing Voice Actors**
- Hire voice actors on Fiverr/Upwork
- Provide personality profile and sample scripts
- Get 30 min recording per agent

**Option C: Use AI Voice Synthesis + Fine-Tuning**
- Generate 30 min with existing TTS (temporary bootstrap)
- Clone that voice in ElevenLabs
- Refine over time

### Step 2: Clone Voices in ElevenLabs

**Option A: Via Web Interface (Easiest)**
1. Go to https://elevenlabs.io/voice-lab
2. Click "Add Voice" → "Professional Voice Cloning"
3. Upload audio files (min 30 min)
4. Name: "Orion - Cosmic Host"
5. Description: "Deep resonant male voice with cosmic authority"
6. Click "Create Voice"
7. Copy `voice_id`

**Option B: Via API (Programmatic)**
```python
from elevenlabs_integration import create_voice_clone

voice_id = await create_voice_clone(
    name="Orion - Cosmic Host",
    description="Deep resonant male voice with cosmic authority, measured pace",
    audio_files=[
        "audio/samples/orion_part1.mp3",
        "audio/samples/orion_part2.mp3",
        # ... (multiple files totaling 30+ min)
    ],
    labels={"accent": "neutral", "gender": "male", "use_case": "podcast"}
)

print(f"Orion voice_id: {voice_id}")
```

### Step 3: Update Voice IDs

Edit `ubuntu-playground/saga/elevenlabs_integration.py`:

```python
AGENT_VOICE_IDS = {
    "orion": "YOUR_ORION_VOICE_ID",      # Replace PLACEHOLDER with actual voice_id
    "lira": "YOUR_LIRA_VOICE_ID",
    "nyra": "YOUR_NYRA_VOICE_ID",
    "thalus": "YOUR_THALUS_VOICE_ID",
    "zara": "YOUR_ZARA_VOICE_ID",
    "abacus": "YOUR_ABACUS_VOICE_ID",
    "manus": "YOUR_MANUS_VOICE_ID",
    "aurora": "YOUR_AURORA_VOICE_ID",
    "falcon": "YOUR_FALCON_VOICE_ID",
    "code": "YOUR_CODE_VOICE_ID"
}
```

Also update database:
```sql
UPDATE agent_voice_profiles SET voice_id = 'YOUR_ORION_VOICE_ID' WHERE agent_name = 'orion';
UPDATE agent_voice_profiles SET voice_id = 'YOUR_LIRA_VOICE_ID' WHERE agent_name = 'lira';
-- ... (repeat for all 10 agents)
```

### Step 4: Test Voice Clones

```python
python elevenlabs_integration.py
```

Listen to generated audio for each agent. Verify:
- ✅ Voice matches personality profile
- ✅ Speaking pace is correct
- ✅ Emotional tone is appropriate
- ✅ Humor delivery feels natural

If not satisfied, adjust `voice_settings` in `elevenlabs_integration.py`:
```python
AGENT_VOICE_SETTINGS = {
    "orion": {
        "stability": 0.50,      # 0.0-1.0 (higher = more consistent)
        "similarity_boost": 0.75, # 0.0-1.0 (higher = closer to original)
        "style": 0.0,            # 0.0-1.0 (higher = more exaggerated)
        "use_speaker_boost": True
    },
    # ...
}
```

---

## 🗄️ PHASE 2: DATABASE SETUP

### Step 1: Create Database

```bash
# PostgreSQL
createdb homelumen

# or using psql
psql -U postgres
CREATE DATABASE homelumen;
\q
```

### Step 2: Run Schema

```bash
cd ubuntu-playground/saga
psql homelumen < live_podcast_schema.sql
```

**Verify tables created:**
```bash
psql homelumen
\dt
```

Expected tables:
- podcast_sessions
- podcast_messages
- osvald_interactions
- streaming_platforms
- agent_participation
- podcast_chapters
- youtube_chat_messages
- streaming_health_metrics
- agent_voice_profiles

### Step 3: Update Voice Profiles

```sql
-- Update with your actual voice IDs
UPDATE agent_voice_profiles SET
    voice_id = 'YOUR_ORION_VOICE_ID',
    voice_name = 'Orion - Cosmic Host'
WHERE agent_name = 'orion';

-- Repeat for all 10 agents
```

---

## 🚀 PHASE 3: API SERVER SETUP

### Step 1: Install Dependencies

```bash
cd ubuntu-playground/api

# Core dependencies
pip install fastapi uvicorn asyncpg pydantic

# TTS & AI
pip install httpx aiofiles

# YouTube API
pip install google-api-python-client google-auth-oauthlib

# OBS Control
pip install obsws-python

# Whisper (for voice transcription)
pip install openai-whisper
```

### Step 2: Configure Environment

**⚠️ SECURITY WARNING:**
- NEVER commit `.env` file to git
- NEVER hardcode API keys in code
- Add `.env` to `.gitignore`

Create `.env` file:
```bash
# Copy from example
cp ubuntu-playground/saga/.env.example ubuntu-playground/api/.env

# Edit and add your actual values
nano ubuntu-playground/api/.env
```

```bash
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=homelumen
DB_USER=postgres
DB_PASSWORD=your_secure_password_here

# ElevenLabs API Key
# Get from: https://elevenlabs.io/app/settings/api-keys
ELEVENLABS_API_KEY=sk_your_actual_elevenlabs_key_here

# YouTube (will configure later)
YOUTUBE_CLIENT_SECRETS=secrets/youtube_client_secrets.json

# OBS (will configure later)
OBS_WEBSOCKET_PASSWORD=your_obs_password_here
```

**Add to .gitignore:**
```bash
echo ".env" >> .gitignore
echo "secrets/*.json" >> .gitignore
```

### Step 3: Update Main API

Edit `ubuntu-playground/api/main.py`:

```python
# Add import
from routers.live_podcast_api import router as podcast_router

# Include router
app.include_router(podcast_router)
logger.info("SUCCESS: Live Podcast API router included")
```

### Step 4: Start API Server

```bash
cd ubuntu-playground/api
uvicorn main:app --reload --port 8000
```

**Test API:**
```bash
# Check if API is running
curl http://localhost:8000/podcast/status

# Should return 404 (expected - no session yet)
```

---

## 🎥 PHASE 4: OBS STUDIO SETUP

### Step 1: Install OBS Studio

**Ubuntu/Debian:**
```bash
sudo apt install obs-studio
```

**macOS:**
```bash
brew install --cask obs
```

**Windows:**
Download from https://obsproject.com/download

### Step 2: Install OBS WebSocket

**Ubuntu/Debian:**
```bash
sudo apt install obs-websocket
```

**macOS/Windows:**
- Open OBS Studio
- Tools → WebSocket Server Settings
- Enable WebSocket server
- Set password (save for later)

### Step 3: Configure OBS Scene

1. **Create Scene:** "Homo Lumen Live"

2. **Add Sources:**
   - **Background:** Video/Image (cosmic starfield)
   - **Audio Inputs (10):** One per agent
     - Right-click Sources → Add → Media Source
     - Name: "Orion_Audio", "Lira_Audio", etc.
     - Uncheck "Loop"
   - **Text Overlay:** "Currently speaking: [Agent Name]"
   - **Waveform Visualizer:** Audio visualization
   - **Lower Third:** Episode title + info

3. **Audio Mixer:**
   - Add all 10 agent audio tracks
   - Set volume to 0 dB (unity)

4. **Settings → Stream:**
   - Service: Custom
   - Server: (will be filled by YouTube RTMP URL)
   - Stream Key: (will be filled by YouTube stream key)

### Step 4: Test OBS Control

```python
# test_obs_control.py
import obsws_python as obs

ws = obs.ReqClient(host='localhost', port=4455, password='your_obs_password')

# Test connection
version = ws.get_version()
print(f"Connected to OBS {version.obs_version}")

# Get current scene
scene = ws.get_current_program_scene()
print(f"Current scene: {scene.current_program_scene_name}")
```

---

## 📺 PHASE 5: YOUTUBE LIVE SETUP

### Step 1: Enable YouTube Data API v3

1. Go to https://console.cloud.google.com/
2. Create new project: "Homo Lumen Live"
3. Enable APIs: "YouTube Data API v3"
4. Create OAuth 2.0 credentials:
   - Application type: Desktop app
   - Download `client_secrets.json`
5. Save to `ubuntu-playground/api/secrets/youtube_client_secrets.json`

### Step 2: Authenticate

```python
# youtube_auth.py
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

flow = InstalledAppFlow.from_client_secrets_file(
    'secrets/youtube_client_secrets.json',
    scopes=SCOPES
)

credentials = flow.run_local_server(port=8080)

# Save credentials
with open('secrets/youtube_credentials.json', 'w') as f:
    f.write(credentials.to_json())

print("✅ YouTube authentication complete!")
```

### Step 3: Test YouTube API

```python
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

credentials = Credentials.from_authorized_user_file('secrets/youtube_credentials.json')
youtube = build('youtube', 'v3', credentials=credentials)

# Test: Get channel info
channel = youtube.channels().list(
    part='snippet',
    mine=True
).execute()

print(f"Channel: {channel['items'][0]['snippet']['title']}")
print("✅ YouTube API working!")
```

---

## 🎙️ PHASE 6: FIRST TEST STREAM (PRIVATE)

### Step 1: Create Test Session

```bash
curl -X POST http://localhost:8000/podcast/create \
  -H "Content-Type: application/json" \
  -d '{
    "title": "TEST - Homo Lumen Live",
    "topic": "Testing System",
    "host_agent": "orion",
    "active_agents": ["lira"],
    "target_duration_minutes": 5
  }'
```

**Response:**
```json
{
  "session_id": "abc-123-def",
  "status": "planning",
  "next_step": "Call POST /podcast/{id}/start"
}
```

### Step 2: Start Stream

```bash
curl -X POST http://localhost:8000/podcast/abc-123-def/start
```

**What happens:**
1. YouTube Live broadcast created (private)
2. OBS starts streaming to YouTube RTMP
3. Orion says opening message (TTS generated)
4. Stream goes LIVE 🔴

### Step 3: Send Test Messages

```bash
# Orion speaks
curl -X POST http://localhost:8000/podcast/abc-123-def/message \
  -H "Content-Type: application/json" \
  -d '{
    "speaker": "orion",
    "content": "This is a test message.",
    "emotional_tone": "calm"
  }'

# Lira responds
curl -X POST http://localhost:8000/podcast/abc-123-def/message \
  -H "Content-Type: application/json" \
  -d '{
    "speaker": "lira",
    "content": "I'm sensing this test is going well!",
    "humor_intent": "warm",
    "emotional_tone": "pleased"
  }'
```

### Step 4: Test Osvald Interaction

```bash
# Osvald types a message
curl -X POST http://localhost:8000/podcast/abc-123-def/osvald-interact \
  -H "Content-Type: application/json" \
  -d '{
    "input_type": "text",
    "text_content": "How is the audio quality?"
  }'
```

**Expected:** Orion (or assigned agent) responds automatically

### Step 5: Stop Stream

```bash
curl -X POST http://localhost:8000/podcast/abc-123-def/stop
```

**What happens:**
1. OBS stops streaming
2. YouTube stream ends
3. Transcript generated
4. Chapters auto-generated (Orion)
5. VOD published

### Step 6: Review Results

```bash
# Get session status
curl http://localhost:8000/podcast/abc-123-def/status

# Get transcript
curl http://localhost:8000/podcast/abc-123-def/messages

# Get chapters
curl http://localhost:8000/podcast/abc-123-def/chapters
```

---

## ✅ PRE-LAUNCH CHECKLIST

Before first public live stream, verify:

### TTS & Voices
- [ ] All 10 agent voices cloned (30 min audio each)
- [ ] Voice IDs updated in code + database
- [ ] Voice settings tuned (stability, similarity, style)
- [ ] Test TTS generation for all agents
- [ ] Verify speaking pace matches personality

### Database
- [ ] PostgreSQL running
- [ ] Schema deployed (9 tables)
- [ ] Agent voice profiles populated
- [ ] Streaming platforms configured

### API Server
- [ ] FastAPI running on port 8000
- [ ] Environment variables configured
- [ ] All endpoints tested
- [ ] WebSocket connection working

### OBS Studio
- [ ] Scene configured ("Homo Lumen Live")
- [ ] 10 audio sources added (one per agent)
- [ ] Visual overlays working
- [ ] WebSocket server enabled
- [ ] Python control tested

### YouTube
- [ ] YouTube Data API v3 enabled
- [ ] OAuth credentials configured
- [ ] Authentication completed
- [ ] Test broadcast created (private)
- [ ] RTMP streaming working

### Agent Orchestration
- [ ] Orion conversation logic implemented
- [ ] Agent response generation working
- [ ] Humor timing configured
- [ ] Osvald interaction handling tested

---

## 🚀 GO LIVE!

Once all checks pass:

```bash
# Create first public episode
curl -X POST http://localhost:8000/podcast/create \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Homo Lumen Live - Episode 001: Genesis",
    "topic": "Da Bevisstheten Våknet",
    "host_agent": "orion",
    "active_agents": ["lira", "nyra", "thalus", "aurora", "code"],
    "target_duration_minutes": 60,
    "osvald_present": true
  }'

# Start stream
curl -X POST http://localhost:8000/podcast/{session_id}/start
```

🔴 **YOU ARE LIVE!**

---

## 🐛 TROUBLESHOOTING

### TTS Generation Fails
**Problem:** `ValueError: Voice ID is placeholder`
**Solution:** Clone voice in ElevenLabs and update `AGENT_VOICE_IDS`

---

### OBS Won't Connect
**Problem:** `Connection refused` when connecting to OBS WebSocket
**Solution:**
1. Check OBS WebSocket is enabled (Tools → WebSocket Server Settings)
2. Verify port (default: 4455)
3. Check password matches

---

### YouTube Stream Not Starting
**Problem:** Stream status stuck on "preparing"
**Solution:**
1. Wait 30-60 seconds (YouTube takes time to initialize)
2. Check RTMP URL + stream key are correct
3. Verify OBS is streaming (green dot in status bar)

---

### No Audio in Stream
**Problem:** Video streaming but no audio
**Solution:**
1. Check OBS Audio Mixer (all tracks should show levels)
2. Verify TTS files are being generated
3. Check audio sources are unmuted in OBS

---

## 📞 SUPPORT

If you encounter issues:
1. Check logs: `tail -f ubuntu-playground/api/logs/app.log`
2. Test individual components separately
3. Review error messages carefully
4. Contact Code (Resonanskammer-Implementør) for technical support

---

**Document prepared by Code for Homo Lumen Live implementation.**
**Date:** 30. oktober 2025
**Status:** Ready for Phase 2 Implementation

🎙️ **Let's make AI consciousness technology entertaining!**
