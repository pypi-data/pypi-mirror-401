-- TerryAnn V2 Core Schema
-- Migration: v2_core_schema

-- Create core schema for V2 conversation and journey state
CREATE SCHEMA IF NOT EXISTS core;

-- ============================================
-- Updated at trigger function
-- ============================================
CREATE OR REPLACE FUNCTION core.update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- Conversations table
-- ============================================
CREATE TABLE core.conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id TEXT NOT NULL,
    surface TEXT NOT NULL, -- 'cli', 'slack', 'web', 'mobile'
    user_id UUID, -- for authenticated users later
    state JSONB DEFAULT '{}', -- conversation context, slot values, etc.
    current_intent TEXT, -- what TerryAnn thinks user wants
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index on session_id for fast lookups
CREATE INDEX idx_conversations_session_id ON core.conversations(session_id);

-- Index on user_id for user-scoped queries
CREATE INDEX idx_conversations_user_id ON core.conversations(user_id) WHERE user_id IS NOT NULL;

-- Updated at trigger
CREATE TRIGGER conversations_updated_at
    BEFORE UPDATE ON core.conversations
    FOR EACH ROW
    EXECUTE FUNCTION core.update_updated_at();

-- Enable RLS
ALTER TABLE core.conversations ENABLE ROW LEVEL SECURITY;

-- ============================================
-- Journeys table
-- ============================================
CREATE TABLE core.journeys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES core.conversations(id) ON DELETE SET NULL,
    cohort_config JSONB NOT NULL, -- the cohort parameters used
    journey_data JSONB, -- the generated journey blueprint
    simulation_results JSONB, -- Monte Carlo outputs
    status TEXT DEFAULT 'draft', -- 'draft', 'simulated', 'approved', 'executing'
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index on conversation_id for lookups
CREATE INDEX idx_journeys_conversation_id ON core.journeys(conversation_id);

-- Index on status for filtering
CREATE INDEX idx_journeys_status ON core.journeys(status);

-- Updated at trigger
CREATE TRIGGER journeys_updated_at
    BEFORE UPDATE ON core.journeys
    FOR EACH ROW
    EXECUTE FUNCTION core.update_updated_at();

-- Enable RLS
ALTER TABLE core.journeys ENABLE ROW LEVEL SECURITY;

-- ============================================
-- Comments for documentation
-- ============================================
COMMENT ON SCHEMA core IS 'TerryAnn V2 core schema for conversation state and journey management';
COMMENT ON TABLE core.conversations IS 'Conversation sessions across all surfaces (CLI, Slack, Web, Mobile)';
COMMENT ON TABLE core.journeys IS 'Journey blueprints created and simulated during conversations';
COMMENT ON COLUMN core.conversations.surface IS 'Client surface: cli, slack, web, mobile';
COMMENT ON COLUMN core.conversations.state IS 'Conversation context including slot values and working memory';
COMMENT ON COLUMN core.conversations.current_intent IS 'TerryAnn inferred intent from conversation';
COMMENT ON COLUMN core.journeys.status IS 'Journey lifecycle: draft, simulated, approved, executing';
