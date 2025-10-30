-- ============================================================
-- HOMO LUMEN LIVE - VISUAL CONTENT SYSTEM
-- Database Schema Extension for Dynamic Visual Content
-- ============================================================
-- Created: 30. oktober 2025
-- Purpose: Add visual content generation (images, videos, avatars)
--          to live podcast streaming for viewer engagement
-- Extends: live_podcast_schema.sql
-- ============================================================

-- ============================================================
-- 1. VISUAL CONTENT (Generated Images/Videos)
-- ============================================================
CREATE TABLE IF NOT EXISTS visual_content (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES podcast_sessions(id) ON DELETE CASCADE,

    -- Content Metadata
    content_type TEXT NOT NULL,
    -- "agent_avatar", "concept_illustration", "code_snippet",
    -- "data_visualization", "quote_overlay", "background_animation"

    title TEXT,
    description TEXT,

    -- Visual Specifications
    visual_style TEXT,
    -- "minimalist", "cosmic", "technical", "artistic", "diagrams"

    aspect_ratio TEXT DEFAULT '16:9',
    resolution TEXT DEFAULT '1920x1080',

    -- Content Triggers
    triggered_by_agent TEXT, -- Which agent triggered generation (usually Nyra)
    related_to_message_id UUID REFERENCES podcast_messages(id),
    related_to_topic TEXT, -- "triadisk_ethics", "genomos", "port_1"

    -- Timing
    display_start_timestamp DECIMAL(8,3), -- When to show (seconds from session start)
    display_duration_seconds INTEGER, -- How long to show
    display_end_timestamp DECIMAL(8,3),

    -- Generation Details
    generation_prompt TEXT, -- Prompt used for AI image generation
    generation_model TEXT, -- "dall-e-3", "midjourney", "stable-diffusion"
    generation_status TEXT DEFAULT 'pending',
    -- pending → generating → completed → displayed → archived

    -- File Storage
    file_path TEXT, -- Local file path
    file_url TEXT, -- Cloud storage URL (if uploaded)
    file_size_bytes INTEGER,
    file_format TEXT DEFAULT 'png', -- png, jpg, mp4, gif

    -- OBS Integration
    obs_scene_name TEXT, -- Which OBS scene to display this in
    obs_source_name TEXT, -- OBS source name
    obs_layer INTEGER DEFAULT 10, -- Z-index (higher = on top)

    -- Analytics
    display_count INTEGER DEFAULT 0, -- How many times shown
    viewer_engagement_score DECIMAL(3,2), -- 0.00-1.00 (how much viewers liked it)

    created_at TIMESTAMP DEFAULT NOW(),
    generated_at TIMESTAMP,
    displayed_at TIMESTAMP
);

CREATE INDEX idx_visual_content_session ON visual_content(session_id, display_start_timestamp);
CREATE INDEX idx_visual_content_status ON visual_content(generation_status);
CREATE INDEX idx_visual_content_type ON visual_content(content_type);

-- ============================================================
-- 2. AGENT AVATARS (Visual Representations)
-- ============================================================
CREATE TABLE IF NOT EXISTS agent_avatars (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Agent Identity
    agent_name TEXT UNIQUE NOT NULL, -- "orion", "lira", etc.

    -- Avatar Specifications
    avatar_type TEXT NOT NULL,
    -- "static_image", "animated_sprite", "ai_generated", "3d_model"

    style TEXT DEFAULT 'minimalist',
    -- minimalist, cosmic, artistic, photorealistic

    -- Avatar States (Different expressions/poses)
    state TEXT DEFAULT 'idle',
    -- idle, speaking, listening, humorous, serious, thinking

    -- File Storage
    file_path TEXT NOT NULL, -- Path to avatar file
    file_format TEXT DEFAULT 'png', -- png, gif, svg, mp4

    -- Visual Properties
    background_color TEXT DEFAULT '#000000',
    border_color TEXT, -- Optional border
    border_width INTEGER DEFAULT 0,

    -- Animation Settings (if animated)
    animation_fps INTEGER DEFAULT 30,
    animation_loop BOOLEAN DEFAULT TRUE,

    -- Generation Details (if AI-generated)
    generation_prompt TEXT,
    generation_model TEXT, -- "dall-e-3", "midjourney", etc.

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- 3. VISUAL GENERATION QUEUE (Pending Visual Tasks)
-- ============================================================
CREATE TABLE IF NOT EXISTS visual_generation_queue (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES podcast_sessions(id) ON DELETE CASCADE,

    -- Request Details
    requested_by_agent TEXT NOT NULL, -- Usually "nyra"
    content_type TEXT NOT NULL,
    priority INTEGER DEFAULT 5, -- 1-10 (10 = highest priority)

    -- Generation Prompt
    generation_prompt TEXT NOT NULL,
    negative_prompt TEXT, -- What to avoid in generation
    style_modifiers TEXT[], -- ["cosmic", "minimalist", "vibrant"]

    -- Target Specifications
    target_aspect_ratio TEXT DEFAULT '16:9',
    target_resolution TEXT DEFAULT '1920x1080',

    -- Status
    status TEXT DEFAULT 'queued',
    -- queued → generating → completed → failed

    -- Model Selection
    preferred_model TEXT, -- "dall-e-3", "midjourney", "stable-diffusion"
    fallback_models TEXT[], -- Fallback if preferred fails

    -- Timing
    requested_at TIMESTAMP DEFAULT NOW(),
    started_generating_at TIMESTAMP,
    completed_at TIMESTAMP,
    generation_duration_ms INTEGER,

    -- Result
    result_visual_content_id UUID REFERENCES visual_content(id),
    error_message TEXT -- If generation failed
);

CREATE INDEX idx_visual_queue_status ON visual_generation_queue(status, priority DESC);
CREATE INDEX idx_visual_queue_session ON visual_generation_queue(session_id);

-- ============================================================
-- 4. OBS SCENES (OBS Studio Scene Configuration)
-- ============================================================
CREATE TABLE IF NOT EXISTS obs_scenes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Scene Identity
    scene_name TEXT UNIQUE NOT NULL,
    scene_type TEXT NOT NULL,
    -- "main_conversation", "agent_spotlight", "concept_visualization",
    -- "code_demonstration", "data_charts", "quote_overlay"

    description TEXT,

    -- Visual Layout
    layout_template TEXT,
    -- "center_focus", "split_screen", "picture_in_picture", "full_screen"

    background_type TEXT DEFAULT 'static',
    -- static, animated, video_loop, particle_effects

    background_source TEXT, -- File path or URL

    -- Active Sources (What's currently displayed)
    active_sources JSONB DEFAULT '[]',
    -- [{"source_name": "Orion_Avatar", "layer": 10, "position": {"x": 100, "y": 100}}]

    -- Audio Settings
    audio_sources TEXT[], -- Which audio tracks to include

    -- Transition Settings
    transition_in TEXT DEFAULT 'fade',
    transition_out TEXT DEFAULT 'fade',
    transition_duration_ms INTEGER DEFAULT 500,

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- 5. SCENE TRANSITIONS (When to Switch Scenes)
-- ============================================================
CREATE TABLE IF NOT EXISTS scene_transitions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES podcast_sessions(id) ON DELETE CASCADE,

    -- Transition Details
    from_scene_name TEXT REFERENCES obs_scenes(scene_name),
    to_scene_name TEXT NOT NULL REFERENCES obs_scenes(scene_name),

    -- Trigger
    triggered_by TEXT NOT NULL,
    -- "agent_change", "topic_change", "visual_content", "manual"

    trigger_agent TEXT, -- Which agent triggered (if agent_change)
    trigger_message_id UUID REFERENCES podcast_messages(id),

    -- Timing
    timestamp_seconds DECIMAL(8,3), -- When transition happened
    transition_duration_ms INTEGER DEFAULT 500,

    -- Reason/Context
    transition_reason TEXT,
    -- "Orion started speaking", "Showing concept illustration", "Code demonstration"

    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_scene_transitions_session ON scene_transitions(session_id, timestamp_seconds);

-- ============================================================
-- 6. NYRA VISUAL DIRECTIVES (Nyra's Visual Orchestration)
-- ============================================================
CREATE TABLE IF NOT EXISTS nyra_visual_directives (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES podcast_sessions(id) ON DELETE CASCADE,

    -- Directive Type
    directive_type TEXT NOT NULL,
    -- "generate_concept_art", "switch_scene", "show_avatar",
    -- "display_quote", "animate_diagram", "code_highlight"

    -- Content
    directive_content JSONB NOT NULL,
    -- Flexible JSON for different directive types

    -- Target
    target_agent TEXT, -- If directive is about specific agent
    target_message_id UUID REFERENCES podcast_messages(id),

    -- Timing
    execute_at_timestamp DECIMAL(8,3), -- When to execute (seconds from start)

    -- Execution Status
    status TEXT DEFAULT 'pending',
    -- pending → executing → completed → failed

    executed_at TIMESTAMP,
    error_message TEXT,

    -- Result
    result_visual_content_id UUID REFERENCES visual_content(id),
    result_scene_transition_id UUID REFERENCES scene_transitions(id),

    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_nyra_directives_session ON nyra_visual_directives(session_id, execute_at_timestamp);
CREATE INDEX idx_nyra_directives_status ON nyra_visual_directives(status);

-- ============================================================
-- INITIAL DATA: Agent Avatars (Placeholders)
-- ============================================================
-- These will be updated with actual generated avatars

INSERT INTO agent_avatars (agent_name, avatar_type, style, file_path) VALUES
    ('orion', 'ai_generated', 'cosmic', 'avatars/orion_cosmic.png'),
    ('lira', 'ai_generated', 'warm', 'avatars/lira_warm.png'),
    ('nyra', 'ai_generated', 'artistic', 'avatars/nyra_artistic.png'),
    ('thalus', 'ai_generated', 'minimalist', 'avatars/thalus_philosophical.png'),
    ('zara', 'ai_generated', 'technical', 'avatars/zara_security.png'),
    ('abacus', 'ai_generated', 'minimalist', 'avatars/abacus_analytical.png'),
    ('manus', 'ai_generated', 'practical', 'avatars/manus_builder.png'),
    ('aurora', 'ai_generated', 'scholarly', 'avatars/aurora_research.png'),
    ('falcon', 'ai_generated', 'futuristic', 'avatars/falcon_scout.png'),
    ('code', 'ai_generated', 'minimalist', 'avatars/code_developer.png')
ON CONFLICT (agent_name) DO NOTHING;

-- ============================================================
-- INITIAL DATA: OBS Scenes (Default Scenes)
-- ============================================================

INSERT INTO obs_scenes (scene_name, scene_type, description, layout_template) VALUES
    ('main_conversation', 'main_conversation', 'Default scene - shows currently speaking agent', 'center_focus'),
    ('concept_visualization', 'concept_visualization', 'Full-screen concept illustration', 'full_screen'),
    ('code_demonstration', 'code_demonstration', 'Code snippet display with syntax highlighting', 'full_screen'),
    ('data_charts', 'data_charts', 'Data visualizations and charts (Abacus)', 'center_focus'),
    ('quote_overlay', 'quote_overlay', 'Text quote overlay on cosmic background', 'center_focus'),
    ('multi_agent_panel', 'main_conversation', 'Split screen showing multiple agents', 'split_screen'),
    ('opening_sequence', 'main_conversation', 'Opening animation with all agent avatars', 'center_focus')
ON CONFLICT (scene_name) DO NOTHING;

-- ============================================================
-- VIEWS: Useful Aggregations
-- ============================================================

-- Visual Content Summary per Session
CREATE OR REPLACE VIEW visual_content_summary AS
SELECT
    vc.session_id,
    COUNT(*) AS total_visuals,
    COUNT(CASE WHEN vc.content_type = 'agent_avatar' THEN 1 END) AS avatar_count,
    COUNT(CASE WHEN vc.content_type = 'concept_illustration' THEN 1 END) AS concept_count,
    COUNT(CASE WHEN vc.content_type = 'code_snippet' THEN 1 END) AS code_count,
    COUNT(CASE WHEN vc.content_type = 'data_visualization' THEN 1 END) AS data_viz_count,
    COUNT(CASE WHEN vc.generation_status = 'completed' THEN 1 END) AS completed_count,
    COUNT(CASE WHEN vc.generation_status = 'pending' THEN 1 END) AS pending_count,
    AVG(vc.viewer_engagement_score) AS avg_engagement
FROM visual_content vc
GROUP BY vc.session_id;

-- Scene Transition Frequency
CREATE OR REPLACE VIEW scene_transition_stats AS
SELECT
    st.session_id,
    st.to_scene_name,
    COUNT(*) AS transition_count,
    AVG(st.transition_duration_ms) AS avg_duration_ms
FROM scene_transitions st
GROUP BY st.session_id, st.to_scene_name
ORDER BY transition_count DESC;

-- ============================================================
-- FUNCTIONS: Helper Functions
-- ============================================================

-- Function to get current active scene for a session
CREATE OR REPLACE FUNCTION get_current_scene(p_session_id UUID)
RETURNS TEXT AS $$
    SELECT to_scene_name
    FROM scene_transitions
    WHERE session_id = p_session_id
    ORDER BY timestamp_seconds DESC
    LIMIT 1;
$$ LANGUAGE SQL;

-- ============================================================
-- COMMENTS: Schema Documentation
-- ============================================================

COMMENT ON TABLE visual_content IS 'Generated visual content (images, videos) displayed during podcast';
COMMENT ON TABLE agent_avatars IS 'Visual representations of each agent (static or animated)';
COMMENT ON TABLE visual_generation_queue IS 'Queue of pending visual generation tasks (handled by Nyra)';
COMMENT ON TABLE obs_scenes IS 'OBS Studio scene configurations for different visual layouts';
COMMENT ON TABLE scene_transitions IS 'Log of all scene transitions during podcast';
COMMENT ON TABLE nyra_visual_directives IS 'Nyra''s orchestration commands for visual content';

-- ============================================================
-- END OF VISUAL CONTENT SCHEMA
-- ============================================================
