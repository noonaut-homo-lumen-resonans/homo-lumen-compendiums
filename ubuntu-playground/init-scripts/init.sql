-- ===========================
-- Ubuntu Playground - PostgreSQL Initialization
-- ===========================
--
-- This script runs automatically when PostgreSQL container starts for the first time.
-- It creates the necessary databases and users for Ubuntu Playground.
--

-- Create Gitea database and user
CREATE DATABASE gitea;
CREATE USER gitea WITH ENCRYPTED PASSWORD 'gitea-password-from-env';
GRANT ALL PRIVILEGES ON DATABASE gitea TO gitea;

-- Create audit trail table for workspace events
CREATE TABLE IF NOT EXISTS workspace_events (
    id SERIAL PRIMARY KEY,
    agent_name VARCHAR(50) NOT NULL,
    action VARCHAR(50) NOT NULL,
    path TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

-- Create commit log table
CREATE TABLE IF NOT EXISTS git_commits (
    id SERIAL PRIMARY KEY,
    agent_name VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    files TEXT[] NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create agent session table (for tracking active agents)
CREATE TABLE IF NOT EXISTS agent_sessions (
    id SERIAL PRIMARY KEY,
    agent_name VARCHAR(50) UNIQUE NOT NULL,
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    api_calls INTEGER DEFAULT 0,
    metadata JSONB
);

-- Create indexes for performance
CREATE INDEX idx_workspace_events_agent ON workspace_events(agent_name);
CREATE INDEX idx_workspace_events_timestamp ON workspace_events(timestamp);
CREATE INDEX idx_git_commits_agent ON git_commits(agent_name);
CREATE INDEX idx_git_commits_timestamp ON git_commits(timestamp);

-- Grant permissions to playground_user
GRANT ALL PRIVILEGES ON TABLE workspace_events TO playground_user;
GRANT ALL PRIVILEGES ON TABLE git_commits TO playground_user;
GRANT ALL PRIVILEGES ON TABLE agent_sessions TO playground_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO playground_user;

-- Insert initial agent sessions (placeholder)
INSERT INTO agent_sessions (agent_name, api_calls, metadata)
VALUES
    ('manus', 0, '{"role": "Infrastructure & Deployment"}'),
    ('code', 0, '{"role": "Frontend Development"}'),
    ('lira', 0, '{"role": "Empathic AI & Mental Health"}'),
    ('orion', 0, '{"role": "Meta-Coordination"}'),
    ('abacus', 0, '{"role": "Analytics & Data"}'),
    ('nyra', 0, '{"role": "Visual Design"}'),
    ('thalus', 0, '{"role": "Ethics & Governance"}'),
    ('aurora', 0, '{"role": "Research & Epistemic Validation"}'),
    ('thalamus', 0, '{"role": "Routing & Integration"}'),
    ('scribe', 0, '{"role": "Documentation"}')
ON CONFLICT (agent_name) DO NOTHING;
