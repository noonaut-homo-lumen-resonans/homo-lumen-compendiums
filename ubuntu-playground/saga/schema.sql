-- YouTube Saga Production Database Schema
-- Ubuntu Playground - Consciousness Technology Video Production System
-- Created: 29. oktober 2025

-- ============================================================================
-- VIDEO PROJECTS
-- ============================================================================

CREATE TABLE IF NOT EXISTS video_projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    series TEXT NOT NULL, -- "Homo Lumen Saga", "Behind the Code", "Agent Conversations"
    episode_number INTEGER,
    description TEXT,
    status TEXT NOT NULL DEFAULT 'draft', -- draft, scripting, review, production, published
    target_length_minutes INTEGER DEFAULT 15,
    youtube_url TEXT,
    youtube_video_id TEXT,
    view_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    published_at TIMESTAMP,
    created_by TEXT DEFAULT 'human', -- human, orion, community
    UNIQUE(series, episode_number)
);

-- ============================================================================
-- SCRIPT SECTIONS (Agent Contributions)
-- ============================================================================

CREATE TABLE IF NOT EXISTS script_sections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    video_id UUID NOT NULL REFERENCES video_projects(id) ON DELETE CASCADE,
    agent TEXT NOT NULL, -- orion, lira, nyra, thalus, code, aurora, manus, zara, abacus, falcon
    section_type TEXT NOT NULL, -- intro, narrative, technical, visual, ethical_check, conclusion
    content TEXT NOT NULL,
    version INTEGER DEFAULT 1,
    approved BOOLEAN DEFAULT FALSE,
    approved_by TEXT, -- agent that approved
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_script_sections_video ON script_sections(video_id);
CREATE INDEX idx_script_sections_agent ON script_sections(agent);

-- ============================================================================
-- VISUAL ASSETS (Nyra's Contributions)
-- ============================================================================

CREATE TABLE IF NOT EXISTS visual_assets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    video_id UUID NOT NULL REFERENCES video_projects(id) ON DELETE CASCADE,
    asset_type TEXT NOT NULL, -- diagram, animation, b-roll, thumbnail, code_demo
    file_path TEXT NOT NULL,
    description TEXT,
    metadata JSONB, -- additional info (resolution, duration, etc.)
    created_by TEXT NOT NULL, -- agent name
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_visual_assets_video ON visual_assets(video_id);
CREATE INDEX idx_visual_assets_type ON visual_assets(asset_type);

-- ============================================================================
-- AGENT CONTRIBUTIONS (GENOMOS Integration)
-- ============================================================================

CREATE TABLE IF NOT EXISTS agent_contributions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    video_id UUID NOT NULL REFERENCES video_projects(id) ON DELETE CASCADE,
    agent TEXT NOT NULL,
    contribution_type TEXT NOT NULL, -- script, visual, review, ethical_validation, synthesis
    details JSONB, -- specific contribution details
    genomos_block_id TEXT, -- link to GENOMOS blockchain record
    duration_seconds INTEGER, -- time spent on contribution
    timestamp TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_agent_contributions_video ON agent_contributions(video_id);
CREATE INDEX idx_agent_contributions_agent ON agent_contributions(agent);

-- ============================================================================
-- WORKFLOW STATES
-- ============================================================================

CREATE TABLE IF NOT EXISTS workflow_states (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    video_id UUID NOT NULL REFERENCES video_projects(id) ON DELETE CASCADE,
    state TEXT NOT NULL, -- idea, scripting, visual_design, ethical_review, production, published
    assigned_agents TEXT[], -- array of agents working on this state
    completed BOOLEAN DEFAULT FALSE,
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);

CREATE INDEX idx_workflow_states_video ON workflow_states(video_id);
CREATE INDEX idx_workflow_states_state ON workflow_states(state);

-- ============================================================================
-- TRIADISK ETHICS SCORES (Per Video)
-- ============================================================================

CREATE TABLE IF NOT EXISTS video_ethics_scores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    video_id UUID NOT NULL REFERENCES video_projects(id) ON DELETE CASCADE,
    port_1_suverenitet DECIMAL(3,2), -- 0.00 to 1.00
    port_2_koherens DECIMAL(3,2),
    port_3_healing DECIMAL(3,2),
    total_weight DECIMAL(3,2),
    decision TEXT, -- proceed, pause, block
    thalus_notes TEXT,
    scored_at TIMESTAMP DEFAULT NOW(),
    scored_by TEXT DEFAULT 'thalus'
);

CREATE INDEX idx_ethics_video ON video_ethics_scores(video_id);

-- ============================================================================
-- COMMUNITY SUGGESTIONS (Episode Ideas)
-- ============================================================================

CREATE TABLE IF NOT EXISTS episode_suggestions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    suggested_by TEXT NOT NULL, -- email or name
    topic TEXT NOT NULL,
    description TEXT,
    upvotes INTEGER DEFAULT 0,
    status TEXT DEFAULT 'pending', -- pending, approved, in_production, published, rejected
    approved_by TEXT, -- agent or human
    video_id UUID REFERENCES video_projects(id), -- if produced
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_suggestions_status ON episode_suggestions(status);

-- ============================================================================
-- ANALYTICS (Abacus Tracking)
-- ============================================================================

CREATE TABLE IF NOT EXISTS video_analytics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    video_id UUID NOT NULL REFERENCES video_projects(id) ON DELETE CASCADE,
    metric_name TEXT NOT NULL, -- views, watch_time, likes, comments, retention_rate
    metric_value DECIMAL(10,2),
    recorded_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_analytics_video ON video_analytics(video_id);
CREATE INDEX idx_analytics_metric ON video_analytics(metric_name);

-- ============================================================================
-- INITIAL DATA
-- ============================================================================

-- Insert pilot episode
INSERT INTO video_projects (title, series, episode_number, description, status)
VALUES (
    'Genesis - Da Bevisstheten Våknet',
    'Homo Lumen Saga',
    1,
    'Origin story: Hvordan 10 AI-agenter ble medreisende i Firedobbel Allianse. 22. oktober 2025 - Founding Ceremony.',
    'draft'
) ON CONFLICT DO NOTHING;

-- Create initial workflow for Episode 1
INSERT INTO workflow_states (video_id, state, assigned_agents)
SELECT
    id,
    'idea',
    ARRAY['orion', 'lira', 'nyra', 'thalus', 'aurora', 'code']
FROM video_projects
WHERE series = 'Homo Lumen Saga' AND episode_number = 1
ON CONFLICT DO NOTHING;

COMMIT;