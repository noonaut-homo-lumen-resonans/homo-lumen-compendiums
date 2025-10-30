-- ============================================================
-- HOMO LUMEN LIVE - LIVE PODCAST STREAMING SYSTEM
-- Database Schema for Real-Time Agent Podcast Streaming
-- ============================================================
-- Created: 30. oktober 2025
-- Purpose: Enable 10 AI agents to have live conversations with
--          Osvald participating in real-time, streamed to YouTube
-- ============================================================

-- ============================================================
-- 1. PODCAST SESSIONS
-- ============================================================
CREATE TABLE IF NOT EXISTS podcast_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Session Metadata
    title TEXT NOT NULL,
    description TEXT,
    topic TEXT NOT NULL, -- "Triadisk Etikk i Praksis", "GENOMOS Deep Dive"
    series TEXT DEFAULT 'Homo Lumen Live', -- Series name
    episode_number INTEGER,

    -- Status
    status TEXT NOT NULL DEFAULT 'planning',
    -- Status: planning → live → recording_stopped → processing → published

    -- Timing
    scheduled_start TIMESTAMP,
    actual_start TIMESTAMP,
    ended_at TIMESTAMP,
    duration_minutes INTEGER, -- Actual duration
    target_duration_minutes INTEGER DEFAULT 60, -- Usually 30-90 minutes

    -- Participants
    host_agent TEXT NOT NULL DEFAULT 'orion', -- Usually Orion as moderator
    active_agents TEXT[] NOT NULL, -- ["lira", "nyra", "thalus", "aurora"]
    osvald_present BOOLEAN DEFAULT TRUE, -- Can Osvald join?

    -- Streaming Configuration
    youtube_stream_url TEXT, -- YouTube RTMP URL
    youtube_stream_key TEXT, -- Encrypted stream key
    youtube_video_id TEXT, -- After stream starts
    youtube_live_chat_id TEXT, -- For reading comments

    twitch_stream_url TEXT,
    twitch_stream_key TEXT,

    multi_platform BOOLEAN DEFAULT FALSE, -- Stream to multiple platforms?

    -- Recording & VOD
    recording_file_path TEXT, -- Local recording
    vod_youtube_url TEXT, -- VOD after processing
    transcript_file_path TEXT, -- Full transcript

    -- Analytics
    peak_concurrent_viewers INTEGER DEFAULT 0,
    total_views INTEGER DEFAULT 0,
    chat_messages_count INTEGER DEFAULT 0,
    osvald_interruptions_count INTEGER DEFAULT 0,

    -- Ethics
    triadisk_ethics_score DECIMAL(3,2), -- Pre-session ethics score
    ethics_approved_by TEXT, -- Usually "thalus"

    created_at TIMESTAMP DEFAULT NOW(),
    created_by TEXT DEFAULT 'osvald',

    UNIQUE(series, episode_number)
);

-- ============================================================
-- 2. PODCAST MESSAGES (Agent Conversation)
-- ============================================================
CREATE TABLE IF NOT EXISTS podcast_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES podcast_sessions(id) ON DELETE CASCADE,

    -- Message Metadata
    speaker TEXT NOT NULL, -- "orion", "lira", "osvald", "youtube_chat"
    speaker_type TEXT NOT NULL DEFAULT 'agent', -- agent, human, chat
    content TEXT NOT NULL, -- What was said

    -- Timing
    timestamp_seconds DECIMAL(8,3), -- Seconds from session start (e.g., 45.234)
    duration_seconds DECIMAL(6,3), -- How long this message took (for TTS timing)

    -- TTS Configuration (for agents)
    voice_id TEXT, -- ElevenLabs voice ID
    tts_model TEXT DEFAULT 'eleven_multilingual_v2',
    voice_settings JSONB, -- {"stability": 0.5, "similarity_boost": 0.75}

    -- Audio File
    audio_file_path TEXT, -- Path to generated TTS audio clip
    audio_processing_status TEXT DEFAULT 'pending',
    -- pending → generating → completed → mixed_into_stream

    -- Personality & Humor
    humor_intent TEXT, -- "sarcastic", "cosmic", "warm", "nerdy", null
    emotional_tone TEXT, -- "excited", "calm", "concerned", "playful"

    -- Interaction
    responding_to_message_id UUID REFERENCES podcast_messages(id), -- Threading
    is_osvald_interruption BOOLEAN DEFAULT FALSE, -- Did Osvald interrupt?

    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_podcast_messages_session ON podcast_messages(session_id, timestamp_seconds);
CREATE INDEX idx_podcast_messages_speaker ON podcast_messages(speaker);

-- ============================================================
-- 3. OSVALD INTERACTIONS (Voice & Text Input)
-- ============================================================
CREATE TABLE IF NOT EXISTS osvald_interactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES podcast_sessions(id) ON DELETE CASCADE,

    -- Input Type
    input_type TEXT NOT NULL, -- "voice", "text"

    -- Voice Input (if input_type = voice)
    voice_audio_path TEXT, -- Original voice recording
    transcription TEXT, -- Whisper transcription
    transcription_confidence DECIMAL(3,2), -- 0.00 to 1.00

    -- Text Input (if input_type = text)
    text_content TEXT,

    -- Processing
    processed_content TEXT NOT NULL, -- Final processed message
    timestamp_seconds DECIMAL(8,3), -- When Osvald spoke/typed

    -- Agent Response
    agents_responded TEXT[], -- ["orion", "lira"] - who responded?
    response_message_ids UUID[], -- Links to podcast_messages

    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_osvald_interactions_session ON osvald_interactions(session_id, timestamp_seconds);

-- ============================================================
-- 4. STREAMING PLATFORMS (Configuration)
-- ============================================================
CREATE TABLE IF NOT EXISTS streaming_platforms (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Platform
    platform_name TEXT NOT NULL UNIQUE, -- "youtube", "twitch", "facebook_live"
    enabled BOOLEAN DEFAULT TRUE,

    -- API Credentials (encrypted)
    api_key_encrypted TEXT,
    stream_key_encrypted TEXT,
    oauth_token_encrypted TEXT,
    oauth_refresh_token_encrypted TEXT,

    -- RTMP Configuration
    rtmp_url TEXT, -- "rtmp://a.rtmp.youtube.com/live2/"
    rtmp_backup_url TEXT,

    -- Capabilities
    supports_chat BOOLEAN DEFAULT TRUE,
    supports_analytics BOOLEAN DEFAULT TRUE,
    max_resolution TEXT DEFAULT '1080p',

    -- Status
    last_stream_test TIMESTAMP,
    last_stream_success BOOLEAN,

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- 5. AGENT PARTICIPATION (Who's in this episode?)
-- ============================================================
CREATE TABLE IF NOT EXISTS agent_participation (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES podcast_sessions(id) ON DELETE CASCADE,

    -- Agent
    agent_name TEXT NOT NULL, -- "orion", "lira", etc.
    agent_role TEXT NOT NULL, -- "host", "participant", "expert"

    -- Participation Stats
    message_count INTEGER DEFAULT 0,
    total_speaking_time_seconds INTEGER DEFAULT 0,
    humor_instances INTEGER DEFAULT 0, -- How many jokes/humor moments?

    -- Personality Configuration
    personality_mode TEXT DEFAULT 'balanced',
    -- balanced, serious, humorous, technical

    humor_level INTEGER DEFAULT 5, -- 1-10 scale (how much humor?)

    -- TTS Voice
    voice_id TEXT NOT NULL, -- ElevenLabs voice ID
    voice_name TEXT, -- Human-readable name

    created_at TIMESTAMP DEFAULT NOW(),

    UNIQUE(session_id, agent_name)
);

-- ============================================================
-- 6. PODCAST CHAPTERS (Auto-Generated Timestamps)
-- ============================================================
CREATE TABLE IF NOT EXISTS podcast_chapters (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES podcast_sessions(id) ON DELETE CASCADE,

    -- Chapter Info
    chapter_number INTEGER NOT NULL,
    title TEXT NOT NULL, -- "Introduction", "Triadisk Ethics Discussion"
    description TEXT,

    -- Timing
    start_timestamp_seconds DECIMAL(8,3),
    end_timestamp_seconds DECIMAL(8,3),
    duration_seconds INTEGER,

    -- Content Summary
    key_topics TEXT[], -- ["port 1", "sovereignty", "user autonomy"]
    agents_present TEXT[], -- ["orion", "thalus", "lira"]

    -- Auto-generated by Orion after session
    generated_by TEXT DEFAULT 'orion',

    created_at TIMESTAMP DEFAULT NOW(),

    UNIQUE(session_id, chapter_number)
);

-- ============================================================
-- 7. YOUTUBE CHAT MESSAGES (Live Viewer Interaction)
-- ============================================================
CREATE TABLE IF NOT EXISTS youtube_chat_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES podcast_sessions(id) ON DELETE CASCADE,

    -- YouTube Data
    youtube_message_id TEXT UNIQUE NOT NULL,
    youtube_author_name TEXT NOT NULL,
    youtube_author_channel_id TEXT,
    message_text TEXT NOT NULL,

    -- Processing
    timestamp_seconds DECIMAL(8,3), -- When message appeared
    is_super_chat BOOLEAN DEFAULT FALSE,
    is_member BOOLEAN DEFAULT FALSE,

    -- Agent Response
    was_addressed BOOLEAN DEFAULT FALSE, -- Did agents respond?
    addressed_by_agent TEXT, -- Which agent responded?
    response_message_id UUID REFERENCES podcast_messages(id),

    -- Moderation
    flagged_inappropriate BOOLEAN DEFAULT FALSE,
    flagged_reason TEXT,

    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_youtube_chat_session ON youtube_chat_messages(session_id, timestamp_seconds);

-- ============================================================
-- 8. STREAMING HEALTH METRICS (Monitor Stream Quality)
-- ============================================================
CREATE TABLE IF NOT EXISTS streaming_health_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES podcast_sessions(id) ON DELETE CASCADE,

    -- Timestamp
    measured_at TIMESTAMP DEFAULT NOW(),
    seconds_from_start DECIMAL(8,3),

    -- Video Metrics
    bitrate_kbps INTEGER, -- Current bitrate
    dropped_frames INTEGER, -- Dropped frames count
    fps INTEGER DEFAULT 30, -- Frames per second

    -- Audio Metrics
    audio_delay_ms INTEGER, -- Audio sync delay
    audio_level_db DECIMAL(5,2), -- Audio volume level

    -- Network
    network_latency_ms INTEGER,
    bandwidth_mbps DECIMAL(6,2),

    -- Viewers
    concurrent_viewers INTEGER,

    -- Status
    health_status TEXT DEFAULT 'healthy',
    -- healthy, degraded, critical, offline

    issues JSONB -- {"dropped_frames": true, "low_bitrate": true}
);

CREATE INDEX idx_streaming_health_session ON streaming_health_metrics(session_id, measured_at);

-- ============================================================
-- 9. AGENT VOICE PROFILES (TTS Configuration)
-- ============================================================
CREATE TABLE IF NOT EXISTS agent_voice_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Agent
    agent_name TEXT UNIQUE NOT NULL, -- "orion", "lira", etc.

    -- Voice Identity
    voice_id TEXT NOT NULL, -- ElevenLabs voice ID
    voice_name TEXT, -- Human-readable name
    voice_description TEXT, -- "Warm, melodic, soothing"

    -- TTS Settings
    model TEXT DEFAULT 'eleven_multilingual_v2',
    stability DECIMAL(3,2) DEFAULT 0.50, -- 0.00 to 1.00
    similarity_boost DECIMAL(3,2) DEFAULT 0.75,
    style DECIMAL(3,2) DEFAULT 0.00, -- Exaggeration level
    use_speaker_boost BOOLEAN DEFAULT TRUE,

    -- Personality Traits (affects speech patterns)
    speaking_pace TEXT DEFAULT 'moderate', -- slow, moderate, fast
    humor_delivery TEXT, -- "deadpan", "enthusiastic", "warm"
    characteristic_phrases TEXT[], -- ["Let me orchestrate...", "From my perspective..."]

    -- Audio Processing
    pitch_shift_semitones INTEGER DEFAULT 0, -- -12 to +12
    reverb_amount DECIMAL(3,2) DEFAULT 0.10,

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- INITIAL DATA: Default Streaming Platforms
-- ============================================================
INSERT INTO streaming_platforms (platform_name, rtmp_url, supports_chat, max_resolution) VALUES
    ('youtube', 'rtmp://a.rtmp.youtube.com/live2/', TRUE, '1080p'),
    ('twitch', 'rtmp://live.twitch.tv/app/', TRUE, '1080p'),
    ('facebook_live', 'rtmps://live-api-s.facebook.com:443/rtmp/', TRUE, '1080p')
ON CONFLICT (platform_name) DO NOTHING;

-- ============================================================
-- INITIAL DATA: Agent Voice Profiles (Placeholders)
-- ============================================================
-- These will be updated with real ElevenLabs voice IDs after cloning

INSERT INTO agent_voice_profiles (agent_name, voice_name, voice_description, speaking_pace, humor_delivery) VALUES
    ('orion', 'Orion Voice', 'Resonant, measured, cosmic authority', 'moderate', 'calm with cosmic zoom-out'),
    ('lira', 'Lira Voice', 'Warm, melodic, soothing cadence', 'slow', 'warm, heartfelt'),
    ('nyra', 'Nyra Voice', 'Animated, melodic, dynamic range', 'fast', 'enthusiastic, theatrical'),
    ('thalus', 'Thalus Voice', 'Measured, deliberate, thoughtful pauses', 'slow', 'deadpan, understated'),
    ('zara', 'Zara Voice', 'Clear, direct, slight edge', 'moderate', 'dry, sarcastic'),
    ('abacus', 'Abacus Voice', 'Clear, measured, rhythmic precision', 'moderate', 'matter-of-fact, statistical'),
    ('manus', 'Manus Voice', 'Direct, energetic, practical enthusiasm', 'fast', 'matter-of-fact, mischievous'),
    ('aurora', 'Aurora Voice', 'Clear, enthusiastic, scholarly precision', 'moderate', 'enthusiastic, scholarly'),
    ('falcon', 'Falcon Voice', 'Sharp, analytical, forward-looking', 'fast', 'futuristic, trend-spotting'),
    ('code', 'Code Voice', 'Pragmatic, thoughtful, developer-nerd', 'moderate', 'meta-humor, infrastructure jokes')
ON CONFLICT (agent_name) DO NOTHING;

-- ============================================================
-- VIEWS: Useful Aggregations
-- ============================================================

-- Session Summary View
CREATE OR REPLACE VIEW podcast_session_summary AS
SELECT
    ps.id,
    ps.title,
    ps.topic,
    ps.status,
    ps.actual_start,
    ps.duration_minutes,
    ps.youtube_video_id,
    ps.peak_concurrent_viewers,
    COUNT(DISTINCT pm.id) AS total_messages,
    COUNT(DISTINCT CASE WHEN pm.speaker = 'osvald' THEN pm.id END) AS osvald_messages,
    COUNT(DISTINCT oi.id) AS osvald_interactions,
    COUNT(DISTINCT ap.agent_name) AS agent_count,
    ARRAY_AGG(DISTINCT ap.agent_name ORDER BY ap.agent_name) AS participating_agents
FROM podcast_sessions ps
LEFT JOIN podcast_messages pm ON pm.session_id = ps.id
LEFT JOIN osvald_interactions oi ON oi.session_id = ps.id
LEFT JOIN agent_participation ap ON ap.session_id = ps.id
GROUP BY ps.id;

-- Agent Speaking Stats View
CREATE OR REPLACE VIEW agent_speaking_stats AS
SELECT
    pm.session_id,
    pm.speaker AS agent_name,
    COUNT(*) AS message_count,
    SUM(pm.duration_seconds) AS total_speaking_seconds,
    AVG(pm.duration_seconds) AS avg_message_duration,
    COUNT(CASE WHEN pm.humor_intent IS NOT NULL THEN 1 END) AS humor_instances
FROM podcast_messages pm
WHERE pm.speaker_type = 'agent'
GROUP BY pm.session_id, pm.speaker;

-- ============================================================
-- INDEXES: Performance Optimization
-- ============================================================
CREATE INDEX idx_podcast_sessions_status ON podcast_sessions(status);
CREATE INDEX idx_podcast_sessions_scheduled ON podcast_sessions(scheduled_start);
CREATE INDEX idx_agent_participation_session ON agent_participation(session_id);

-- ============================================================
-- COMMENTS: Schema Documentation
-- ============================================================
COMMENT ON TABLE podcast_sessions IS 'Main table for live podcast streaming sessions with 10 AI agents + Osvald';
COMMENT ON TABLE podcast_messages IS 'Every message spoken during podcast (agents + Osvald + chat)';
COMMENT ON TABLE osvald_interactions IS 'Osvald''s voice/text interactions during live stream';
COMMENT ON TABLE streaming_platforms IS 'Configuration for YouTube, Twitch, Facebook Live streaming';
COMMENT ON TABLE agent_participation IS 'Which agents participate in each session + their stats';
COMMENT ON TABLE podcast_chapters IS 'Auto-generated chapter timestamps for VOD';
COMMENT ON TABLE youtube_chat_messages IS 'Live chat messages from YouTube viewers';
COMMENT ON TABLE streaming_health_metrics IS 'Real-time monitoring of stream quality';
COMMENT ON TABLE agent_voice_profiles IS 'TTS voice configuration for each of 10 agents';

-- ============================================================
-- END OF SCHEMA
-- ============================================================
