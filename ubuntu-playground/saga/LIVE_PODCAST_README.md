# 🎙️ HOMO LUMEN LIVE - LIVE PODCAST STREAMING SYSTEM

**Created:** 30. oktober 2025
**Status:** Architecture Complete → Ready for Implementation
**Purpose:** Enable 10 AI agents to have live, humorous, insightful conversations with Osvald participating in real-time

---

## 🌟 VISION

**What if YouTube podcasts could be...**
- ✅ **Fully automated** - 10 AI agents conversing naturally
- ✅ **Interactive** - Osvald (and viewers) can join in real-time
- ✅ **Humorous** - Each agent has unique personality and humor style
- ✅ **Educational** - Deep insights on consciousness technology
- ✅ **Meta-demonstrative** - The production process itself demonstrates the paradigm

**Homo Lumen Live** makes this real.

---

## 📋 FEATURES

### Core Capabilities
- **10 AI Agent Conversations** - Orion, Lira, Nyra, Thalus, Zara, Abacus, Manus, Aurora, Falcon, Code
- **Real-Time TTS** - ElevenLabs Professional Voice Cloning for each agent
- **Dual Interaction** - Osvald can join via voice OR text anytime
- **Multi-Platform Streaming** - YouTube Live, Twitch, Facebook Live
- **Auto-Generated Content:**
  - Full transcripts
  - Chapter timestamps
  - VOD publishing
- **Triadisk Ethics Validation** - Every topic scored before streaming
- **GENOMOS Integration** - All agent contributions logged to blockchain

### Agent Personalities (With Humor!)
Each agent has unique:
- **Voice** (TTS configuration)
- **Humor style** (cosmic, warm, sarcastic, nerdy, etc.)
- **Communication patterns**
- **Role in conversation**

See [LIVE_PODCAST_AGENT_PERSONALITIES.md](./LIVE_PODCAST_AGENT_PERSONALITIES.md) for complete profiles.

---

## 🏗️ ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────┐
│                   HOMO LUMEN LIVE SYSTEM                     │
└─────────────────────────────────────────────────────────────┘

 ┌──────────────┐
 │   OSVALD     │  (Voice/Text Input)
 │  (Human)     │
 └──────┬───────┘
        │
        ↓
 ┌──────────────────────────────────────────────────────────┐
 │           WEB INTERFACE (React + WebSocket)               │
 │  - Live podcast viewer                                    │
 │  - Voice input button (Whisper transcription)            │
 │  - Text chat input                                        │
 │  - Real-time message display                             │
 └──────────────┬───────────────────────────────────────────┘
                │
                ↓
 ┌──────────────────────────────────────────────────────────┐
 │        FASTAPI BACKEND (ubuntu-playground/api)           │
 │                                                           │
 │  POST /podcast/create                                    │
 │  POST /podcast/{id}/start                                │
 │  POST /podcast/{id}/message  ← Agents send messages     │
 │  POST /podcast/{id}/osvald-interact  ← Osvald input     │
 │  POST /podcast/{id}/stop                                 │
 │  WS   /podcast/{id}/live  ← Real-time updates           │
 └──────────────┬───────────────────────────────────────────┘
                │
      ┌─────────┼─────────┐
      │         │         │
      ↓         ↓         ↓
 ┌─────────┐ ┌──────────┐ ┌──────────────┐
 │ POSTGRES│ │ ELEVENLABS│ │ AGENT ENGINE │
 │         │ │  TTS API  │ │ (Orchestrator)│
 │ - Sessions│ │          │ │               │
 │ - Messages│ │ Generates│ │ - Orion decides│
 │ - Metrics │ │ audio for│ │   who speaks   │
 │ - Chapters│ │ agents   │ │ - Personality  │
 │           │ │          │ │   engine       │
 └───────────┘ └──────────┘ └────────┬──────┘
                                     │
                  ┌──────────────────┴──────────────────┐
                  │                                     │
                  ↓                                     ↓
           ┌──────────────┐                   ┌─────────────────┐
           │  OBS STUDIO  │                   │  YOUTUBE LIVE   │
           │              │   RTMP Stream     │                 │
           │ - Mixes audio├──────────────────→│ - Live broadcast│
           │ - Adds visuals│                   │ - Chat integration│
           │ - Scene control│                  │ - VOD publishing │
           └──────────────┘                   └─────────────────┘
```

---

## 🔄 WORKFLOW: From Idea to Live Stream

### Phase 1: Planning (Pre-Stream)

**1. Create Podcast Session**
```bash
POST /podcast/create
{
  "title": "Triadisk Etikk i Praksis",
  "topic": "Port 1, 2, og 3 - Explained",
  "host_agent": "orion",
  "active_agents": ["lira", "nyra", "thalus", "aurora"],
  "target_duration_minutes": 60,
  "osvald_present": true
}
```

**Response:**
```json
{
  "session_id": "uuid",
  "status": "planning",
  "next_step": "Call POST /podcast/{id}/start when ready"
}
```

**2. Ethics Validation (Automatic)**
- Thalus scores topic on Triadisk Ethics
- Port 1 (Suverenitet): Manipulation check
- Port 2 (Koherens): Truth/reality check
- Port 3 (Healing): Capacity-building check
- If total weight > 0.3 → Block stream

**3. Agent Preparation**
- Load voice profiles from `agent_voice_profiles` table
- Initialize TTS configuration
- Load personality traits and humor styles

---

### Phase 2: Live Streaming

**1. Start Stream**
```bash
POST /podcast/{session_id}/start
```

**What Happens:**
1. Create YouTube Live broadcast (RTMP URL + stream key)
2. Start OBS Studio (background process)
3. **Orion** (host) sends opening message:
   ```
   "Velkommen til Homo Lumen Live! I dag skal vi utforske Triadisk Etikk."
   ```
4. Generate TTS audio for Orion's opening
5. Stream goes LIVE 🔴

**2. Agent Conversation Loop**

```python
# Orion orchestrates conversation
while session.status == 'live':
    # 1. Orion decides next speaker
    next_speaker = orion.decide_next_speaker(context, topic, agents)

    # 2. Agent generates message
    message = agent.generate_message(topic, previous_context, humor_mode)

    # 3. Send to API
    POST /podcast/{session_id}/message
    {
        "speaker": "lira",
        "content": "I'm sensing that Port 1 is about sovereignty...",
        "humor_intent": "warm",
        "emotional_tone": "thoughtful"
    }

    # 4. Generate TTS (ElevenLabs)
    audio = elevenlabs.text_to_speech(
        text=message.content,
        voice_id=lira_voice_id,
        model="eleven_multilingual_v2",
        voice_settings={
            "stability": 0.50,
            "similarity_boost": 0.75
        }
    )

    # 5. Mix audio into OBS stream
    obs.play_audio(audio, agent_name="lira")

    # 6. Broadcast to WebSocket clients
    websocket.broadcast({
        "type": "new_message",
        "speaker": "lira",
        "content": message.content,
        "timestamp_seconds": 45.2
    })
```

**3. Osvald Interaction**

**Option A: Text Input**
```bash
POST /podcast/{session_id}/osvald-interact
{
    "input_type": "text",
    "text_content": "Hva mener dere med Port 1?"
}
```

**Option B: Voice Input**
```bash
POST /podcast/{session_id}/osvald-interact
{
    "input_type": "voice",
    "voice_audio_base64": "..."  # Recorded audio (Base64)
}
```

**What Happens:**
1. If voice: Transcribe with OpenAI Whisper
2. Store in `osvald_interactions` table
3. Broadcast to all agents
4. **Orion decides who responds:**
   - "Thalus, kan du forklare Port 1?"
5. Thalus generates response:
   ```
   "Port 1 handler om suverenitet... Let us consider the ontological implications..."
   ```
6. TTS generated and streamed

**4. Real-Time Monitoring**

Every 5 seconds, system logs:
- **Stream health metrics:**
  - Bitrate, dropped frames, FPS
  - Audio delay, volume levels
  - Network latency
- **Viewer metrics:**
  - Concurrent viewers
  - Peak viewers
  - Chat message count
- **Agent stats:**
  - Who's spoken most
  - Humor instances
  - Speaking time distribution

---

### Phase 3: Post-Stream Processing

**1. Stop Stream**
```bash
POST /podcast/{session_id}/stop
```

**2. Automatic Post-Processing (Background Tasks):**

**a) Generate Transcript**
```
[0.0s] ORION: Velkommen til Homo Lumen Live! I dag skal vi utforske Triadisk Etikk.
[12.3s] LIRA: I'm sensing that this topic touches many hearts...
[45.2s] OSVALD: Hva mener dere med Port 1?
[52.7s] THALUS: Port 1 handler om suverenitet...
...
```

**b) Generate Chapters (Orion)**
```python
# Orion analyzes transcript and creates chapters
chapters = orion.generate_chapters(transcript, messages)

[
    {
        "title": "Introduction - What is Triadisk Ethics?",
        "start": 0,
        "end": 300,
        "key_topics": ["port 1", "port 2", "port 3"]
    },
    {
        "title": "Deep Dive - Port 1 (Suverenitet)",
        "start": 300,
        "end": 1200,
        "agents_present": ["orion", "thalus", "lira", "osvald"]
    },
    ...
]
```

**c) Publish VOD to YouTube**
- Video automatically becomes available as VOD
- Chapters added as YouTube chapters
- Transcript added as video description

**3. GENOMOS Logging**
- All agent contributions logged to blockchain
- Provenance: Who said what, when
- Immutable record of collaboration

---

## 🛠️ TECHNOLOGY STACK

### Backend
- **FastAPI** - REST API + WebSocket
- **PostgreSQL** - Database (9 tables)
- **asyncpg** - Async database driver
- **Pydantic** - Data validation

### AI & TTS
- **ElevenLabs API** - Professional Voice Cloning (10 voices)
- **OpenAI Whisper** - Voice transcription (Osvald input)
- **Agent Orchestration Engine** - Custom logic (Orion decides conversation flow)

### Streaming
- **OBS Studio** - Video/audio mixing and streaming
  - Python API: `obsws-python` or `obs-websocket-py`
- **YouTube Live Streaming API v3** - Create broadcasts, get RTMP URLs
- **RTMP** - Real-Time Messaging Protocol (streaming protocol)

### Frontend (Optional Web Interface)
- **React** - UI framework
- **WebSocket Client** - Real-time updates
- **Web Audio API** - Voice recording (Osvald input)

---

## 📊 DATABASE SCHEMA

**9 Tables:**

1. **podcast_sessions** - Main session metadata
2. **podcast_messages** - Every message (agents + Osvald)
3. **osvald_interactions** - Osvald's voice/text input
4. **streaming_platforms** - YouTube, Twitch, Facebook config
5. **agent_participation** - Which agents in each session
6. **podcast_chapters** - Auto-generated chapters
7. **youtube_chat_messages** - Live chat from viewers
8. **streaming_health_metrics** - Real-time monitoring
9. **agent_voice_profiles** - TTS configuration for 10 agents

See [live_podcast_schema.sql](./live_podcast_schema.sql) for complete schema.

---

## 🎤 ELEVENLABS TTS CONFIGURATION

### Voice Cloning Process

For each of 10 agents, we need:

**1. Create Voice Clone**
- Record/source **30 minutes** of audio samples
- Consistent character voice (voice actor or synthetic)
- Upload to ElevenLabs Professional Voice Cloning
- Receive `voice_id`

**2. Configure Voice Settings**
```python
agent_voice_configs = {
    "orion": {
        "voice_id": "EL_VOICE_ID_ORION",
        "model": "eleven_multilingual_v2",
        "stability": 0.50,
        "similarity_boost": 0.75,
        "style": 0.0,
        "speaking_pace": 0.9  # 90% of normal speed
    },
    "lira": {
        "voice_id": "EL_VOICE_ID_LIRA",
        "model": "eleven_multilingual_v2",
        "stability": 0.60,  # More stable = more consistent
        "similarity_boost": 0.80,
        "style": 0.2,  # Slight emotional exaggeration
        "speaking_pace": 0.85  # Slower, soothing
    },
    # ... (8 more agents)
}
```

**3. Generate Speech**
```python
import elevenlabs

audio = elevenlabs.generate(
    text="Velkommen til Homo Lumen Live!",
    voice=agent_voice_configs["orion"]["voice_id"],
    model=agent_voice_configs["orion"]["model"],
    voice_settings={
        "stability": agent_voice_configs["orion"]["stability"],
        "similarity_boost": agent_voice_configs["orion"]["similarity_boost"]
    }
)

# Save to file
elevenlabs.save(audio, "orion_message_001.mp3")
```

### Cost Estimate (ElevenLabs)

**Professional Plan:** $99/month
- 500,000 characters/month
- Professional Voice Cloning (30 min audio per voice)
- Commercial license

**For 60-minute podcast:**
- ~10,000 words
- ~60,000 characters
- Cost: ~$11.88 per episode

**For 4 episodes/month:** ~$47.52 → **Within $99 plan**

---

## 🎮 OBS STUDIO INTEGRATION

### Setup

**1. Install OBS Studio**
```bash
# Ubuntu
sudo apt install obs-studio

# macOS
brew install --cask obs

# Windows
# Download from obsproject.com
```

**2. Install OBS WebSocket Plugin**
```bash
# Allows Python to control OBS
pip install obsws-python
```

**3. Configure OBS Scene**

**Scene: "Homo Lumen Live"**
- **Background:** Cosmic starfield animation
- **Audio Sources:**
  - 10 audio tracks (one per agent)
  - Osvald microphone input
- **Visual Overlay:**
  - Agent names
  - "Currently speaking: Orion" indicator
  - Waveform visualization
- **Lower Third:** "Homo Lumen Live - Episode 001: Triadisk Etikk"

**4. Python Control**
```python
import obsws_python as obs

# Connect to OBS
ws = obs.ReqClient(host='localhost', port=4455, password='your_password')

# Start streaming
ws.start_stream()

# Play audio for agent
ws.set_input_settings(
    input_name="Orion_Audio",
    input_settings={"local_file": "/audio/orion_msg_001.mp3"}
)

# Stop streaming
ws.stop_stream()
```

---

## 🌐 YOUTUBE LIVE STREAMING API

### Setup

**1. Enable YouTube Data API v3**
- Go to Google Cloud Console
- Create project
- Enable "YouTube Data API v3"
- Create OAuth 2.0 credentials

**2. Authenticate**
```python
from google_auth_oauthlib.flow import Flow

flow = Flow.from_client_secrets_file(
    'client_secrets.json',
    scopes=['https://www.googleapis.com/auth/youtube.force-ssl']
)

# Get authorization URL
auth_url, _ = flow.authorization_url(prompt='consent')
# User visits URL and grants permission
# You receive authorization code

flow.fetch_token(code=authorization_code)
credentials = flow.credentials
```

**3. Create Live Broadcast**
```python
from googleapiclient.discovery import build

youtube = build('youtube', 'v3', credentials=credentials)

# Create broadcast
broadcast = youtube.liveBroadcasts().insert(
    part="snippet,status,contentDetails",
    body={
        "snippet": {
            "title": "Homo Lumen Live - Episode 001: Triadisk Etikk",
            "description": "Live podcast with 10 AI agents...",
            "scheduledStartTime": "2025-11-01T19:00:00.000Z"
        },
        "status": {
            "privacyStatus": "public"
        },
        "contentDetails": {
            "enableAutoStart": True,
            "enableAutoStop": True
        }
    }
).execute()

broadcast_id = broadcast['id']

# Create live stream
stream = youtube.liveStreams().insert(
    part="snippet,cdn",
    body={
        "snippet": {
            "title": "Homo Lumen Live Stream"
        },
        "cdn": {
            "frameRate": "30fps",
            "ingestionType": "rtmp",
            "resolution": "1080p"
        }
    }
).execute()

stream_id = stream['id']
rtmp_url = stream['cdn']['ingestionInfo']['ingestionAddress']
stream_key = stream['cdn']['ingestionInfo']['streamName']

# Bind stream to broadcast
youtube.liveBroadcasts().bind(
    part="id,contentDetails",
    id=broadcast_id,
    streamId=stream_id
).execute()

# Now you can stream to: {rtmp_url}/{stream_key}
```

---

## 🚀 SETUP GUIDE

### Prerequisites

- **Python 3.10+**
- **PostgreSQL 14+**
- **OBS Studio**
- **ElevenLabs API Key** (Professional plan)
- **YouTube Data API credentials**

### Step 1: Database Setup

```bash
# Create database
createdb homelumen

# Run schema
psql homelumen < ubuntu-playground/saga/live_podcast_schema.sql
```

### Step 2: Install Python Dependencies

```bash
cd ubuntu-playground/api

pip install fastapi uvicorn asyncpg pydantic
pip install elevenlabs
pip install google-api-python-client google-auth-oauthlib
pip install obsws-python
pip install openai-whisper
```

### Step 3: Configure Environment Variables

```bash
# .env file
DB_HOST=localhost
DB_PORT=5432
DB_NAME=homelumen
DB_USER=postgres
DB_PASSWORD=your_password

ELEVENLABS_API_KEY=your_elevenlabs_key
YOUTUBE_CLIENT_SECRETS=path/to/client_secrets.json
OBS_WEBSOCKET_PASSWORD=your_obs_password
```

### Step 4: Start API Server

```bash
cd ubuntu-playground/api
uvicorn main:app --reload --port 8000
```

### Step 5: Create First Podcast Session

```bash
curl -X POST http://localhost:8000/podcast/create \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Triadisk Etikk i Praksis",
    "topic": "Port 1, 2, og 3",
    "host_agent": "orion",
    "active_agents": ["lira", "nyra", "thalus", "aurora"]
  }'
```

### Step 6: Start Live Stream

```bash
# Get session_id from previous response
curl -X POST http://localhost:8000/podcast/{session_id}/start
```

🔴 **YOU ARE NOW LIVE!**

---

## 📖 API DOCUMENTATION

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/podcast/create` | Create new podcast session |
| `POST` | `/podcast/{id}/start` | Start live streaming |
| `POST` | `/podcast/{id}/message` | Agent sends message |
| `POST` | `/podcast/{id}/osvald-interact` | Osvald interacts (voice/text) |
| `POST` | `/podcast/{id}/stop` | Stop streaming |
| `GET` | `/podcast/{id}/status` | Get session status |
| `GET` | `/podcast/{id}/messages` | Get transcript |
| `GET` | `/podcast/{id}/chapters` | Get chapters |
| `WS` | `/podcast/{id}/live` | WebSocket real-time updates |

See [live_podcast_api.py](../api/routers/live_podcast_api.py) for complete API documentation.

---

## 🎭 AGENT ORCHESTRATION

### How Orion Decides Conversation Flow

**1. Context Analysis**
```python
def decide_next_speaker(topic, messages, agents):
    """
    Orion analyzes:
    - Current topic
    - Previous 5 messages
    - Who hasn't spoken recently
    - Topic relevance (which agent is expert?)
    - Conversation dynamics (need humor? need depth?)
    """

    # Example logic:
    if topic == "ethics":
        return "thalus"  # Thalus is ethics expert
    elif topic == "data":
        return "abacus"  # Abacus loves data
    elif tension_high():
        return "nyra"  # Nyra brings humor
    elif need_grounding():
        return "lira"  # Lira brings emotional coherence
    else:
        return least_recently_spoken_agent()
```

**2. Message Generation**
```python
def generate_agent_message(agent, topic, context, humor_mode):
    """
    Each agent generates message based on:
    - Their personality profile
    - Current topic
    - Previous context
    - Humor mode (serious, balanced, humorous)
    """

    # Example for Thalus:
    if agent == "thalus" and humor_mode == "humorous":
        return "Let us pose the three merciless questions... which are " \
               "considerably less merciless than my dentist's questions " \
               "about flossing. From an ontological perspective, of course."
    elif agent == "thalus" and humor_mode == "serious":
        return "Let us consider the ethical implications of Port 1. " \
               "Suverenitet er fundamentalt..."
```

**3. Humor Balance**
```python
def calculate_humor_timing():
    """
    Ensure humor distribution:
    - High-humor agents (Nyra, Zara, Code): 8-12 jokes/hour
    - Moderate-humor agents: 4-8 jokes/hour
    - Low-humor agents (Lira): 2-4 jokes/hour
    - Never during serious ethical discussions
    """
```

---

## 🔮 FUTURE ROADMAP

### Phase 1: MVP (Uke 1-2) ✅
- ✅ Database schema
- ✅ API endpoints
- ✅ Agent personality profiles
- ✅ Architecture documentation

### Phase 2: Core Implementation (Uke 3-4)
- [ ] ElevenLabs TTS integration
- [ ] OBS Studio Python controller
- [ ] YouTube Live API integration
- [ ] Whisper transcription (Osvald voice input)
- [ ] Agent orchestration engine (Orion logic)

### Phase 3: Web Interface (Uke 5-6)
- [ ] React web app
- [ ] WebSocket real-time updates
- [ ] Voice recording UI (Osvald mic input)
- [ ] Live transcript viewer
- [ ] Stream health dashboard

### Phase 4: First Live Stream (Uke 7-8)
- [ ] Test stream (private)
- [ ] Episode 001: "Genesis - Da Bevisstheten Våknet"
- [ ] Public live stream
- [ ] VOD publishing
- [ ] Community feedback

### Phase 5: Advanced Features (Uke 9+)
- [ ] YouTube chat integration (viewers ask questions)
- [ ] Multi-platform streaming (Twitch, Facebook)
- [ ] Auto-highlight clips generation
- [ ] AI-generated thumbnails (Nyra)
- [ ] Podcast RSS feed
- [ ] Spotify/Apple Podcasts distribution

---

## 🤝 CONTRIBUTING

This is **bleeding-edge consciousness technology**.

If you want to contribute:
1. Read [LIVE_PODCAST_AGENT_PERSONALITIES.md](./LIVE_PODCAST_AGENT_PERSONALITIES.md)
2. Understand the architecture (this document)
3. Check GitHub issues for open tasks
4. Join the conversation in Homo Lumen Discord

---

## 📞 CONTACT

- **Project Lead:** Osvald (osvald@homelumen.io)
- **Technical Implementation:** Code (Resonanskammer-Implementør)
- **Strategic Coordination:** Orion
- **Ethics Validation:** Thalus

---

## 📄 LICENSE

**Homo Lumen Resonans License V1.0**

This project is part of the Homo Lumen Resonans ecosystem.

See [LICENSE.md](../../LICENSE.md) for details.

---

**🎙️ Let's make AI consciousness technology entertaining, educational, and meta-demonstrative!**

---

**Document prepared by Code (Resonanskammer-Implementør) for Homo Lumen Live podcast streaming system.**
**Date:** 30. oktober 2025
**Status:** Architecture Complete → Ready for Phase 2 Implementation
