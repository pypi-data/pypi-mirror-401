"""Tests for gateway endpoints."""

import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch, MagicMock

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.gateway.session import Conversation, ConversationManager
from app.models.schemas import (
    CohortResponse,
    JourneyResponse,
    SimulationResponse,
    SimulationOutput,
    SimulationDelta,
    FinalState,
    Touchpoint,
    TouchpointType,
)


# Create mock conversation manager for all tests
@pytest.fixture(autouse=True)
def mock_conversation_manager():
    """Mock the conversation manager for all tests."""
    mock_conv = Conversation(
        id=str(uuid.uuid4()),
        session_id="sess_test123",
        surface="cli",
        user_id=None,
        state={"messages": []},
        current_intent=None,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    with patch("app.gateway.router.conversation_manager") as mock_manager:
        mock_manager.get_or_create_conversation = AsyncMock(return_value=mock_conv)
        mock_manager.update_conversation_state = AsyncMock(return_value=mock_conv)
        mock_manager.get_conversation_by_session = AsyncMock(return_value=mock_conv)
        yield mock_manager


@pytest.fixture(autouse=True)
def mock_synthwell_tools():
    """Mock the SynthWell-backed tools."""
    # Mock cohort response
    mock_cohort = CohortResponse(
        cohort_id="cohort_test123",
        name="Test Cohort for Miami",
        size=1000,
        members=[],
        summary={
            "avg_age": 72,
            "avg_risk_score": 0.45,
            "avg_ltv": 3200.0,
            "channel_distribution": {"email": 0.45, "sms": 0.30, "mailer": 0.25},
        },
        created_at=datetime.now(timezone.utc),
    )

    # Mock journey response
    mock_journey = JourneyResponse(
        journey_id="journey_test123",
        name="Test Journey",
        description="Test journey description",
        touchpoints=[
            Touchpoint(id="tp1", type=TouchpointType.EMAIL, name="Welcome Email", day=1, estimated_cost=0.15, expected_response_rate=0.25),
            Touchpoint(id="tp2", type=TouchpointType.SMS, name="Follow-up SMS", day=7, estimated_cost=0.08, expected_response_rate=0.35),
        ],
        total_duration_days=7,
        estimated_total_cost=0.23,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    # Mock simulation response (baseline vs modified comparison)
    mock_final_state = FinalState(
        cumulative_fatigue=0.15,
        trust_balance=0.72,
        confusion_level=0.08,
    )
    mock_simulation = SimulationResponse(
        journey_id="journey_test123",
        baseline=SimulationOutput(
            total_advance_probability=0.042,
            total_dropout_probability=0.15,
            journey_duration_days=21,
            total_cost=9.00,
            final_state=mock_final_state,
        ),
        modified=SimulationOutput(
            total_advance_probability=0.055,
            total_dropout_probability=0.12,
            journey_duration_days=24,
            total_cost=10.25,
            final_state=mock_final_state,
        ),
        delta=SimulationDelta(
            advance_probability_change=0.013,
            dropout_probability_change=-0.03,
            duration_change_days=3,
            cost_change=1.25,
            interpretation="Adding a direct mail touchpoint increases enrollment by 1.3% with a modest cost increase.",
        ),
    )

    # Mock SynthWell client for chat_fast
    mock_client = MagicMock()
    mock_client.chat_fast = AsyncMock(return_value={
        "response": "I'm TerryAnn, your Medicare campaign strategist. How can I help you today?",
        "conversation_id": "conv_test123",
        "citations": None,
    })

    with patch("app.gateway.router.generate_cohort", new_callable=AsyncMock) as mock_gen_cohort, \
         patch("app.gateway.router.create_journey", new_callable=AsyncMock) as mock_create_journey, \
         patch("app.gateway.router.optimize_journey", new_callable=AsyncMock) as mock_optimize, \
         patch("app.gateway.router.simulate_journey_changes", new_callable=AsyncMock) as mock_simulate, \
         patch("app.gateway.router.get_synthwell_client", return_value=mock_client) as mock_get_client:

        mock_gen_cohort.return_value = mock_cohort
        mock_create_journey.return_value = mock_journey
        mock_optimize.return_value = mock_journey
        mock_simulate.return_value = mock_simulation

        yield {
            "generate_cohort": mock_gen_cohort,
            "create_journey": mock_create_journey,
            "optimize_journey": mock_optimize,
            "simulate_journey_changes": mock_simulate,
            "synthwell_client": mock_client,
        }


client = TestClient(app)


def test_root():
    """Test root endpoint returns service info."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "TerryAnn" in data["service"]


def test_health():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_message_creates_session():
    """Test that sending a message creates a new session."""
    response = client.post(
        "/gateway/message",
        json={"message": "Hello TerryAnn"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert "response" in data


def test_message_with_existing_session():
    """Test continuing a conversation with an existing session."""
    session_id = "sess_existing123"

    response = client.post(
        "/gateway/message",
        json={"message": "Help me create a cohort", "session_id": session_id},
    )
    assert response.status_code == 200
    assert response.json()["session_id"] == session_id


def test_message_with_surface():
    """Test sending a message with a specific surface."""
    response = client.post(
        "/gateway/message",
        json={"message": "Hello", "surface": "slack"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["metadata"]["surface"] == "cli"  # From mock


def test_tools_list():
    """Test listing available MCP tools."""
    response = client.get("/gateway/tools")
    assert response.status_code == 200
    data = response.json()
    assert "tools" in data
    tool_names = [t["name"] for t in data["tools"]]
    assert "generate_cohort" in tool_names
    assert "simulate_journey_changes" in tool_names
    assert "create_journey" in tool_names


def test_cohort_keyword_triggers_tool(mock_synthwell_tools):
    """Test that 'cohort' keyword triggers generate_cohort tool."""
    response = client.post(
        "/gateway/message",
        json={"message": "Generate a cohort for Miami"},
    )
    data = response.json()
    assert "generate_cohort" in data["tools_used"]
    mock_synthwell_tools["generate_cohort"].assert_called_once()


def test_simulate_keyword_triggers_tool(mock_synthwell_tools):
    """Test that 'simulate' keyword triggers simulate_journey tool."""
    response = client.post(
        "/gateway/message",
        json={"message": "Simulate this journey"},
    )
    data = response.json()
    assert "simulate_journey" in data["tools_used"]
    mock_synthwell_tools["simulate_journey_changes"].assert_called_once()


def test_journey_keyword_uses_chat(mock_synthwell_tools):
    """Test that 'journey' keyword goes through chat_fast for conversational gathering."""
    response = client.post(
        "/gateway/message",
        json={"message": "Create a new journey"},
    )
    data = response.json()
    # Journey creation now goes through chat_fast for conversational gathering
    assert "chat_fast" in data["tools_used"]
    mock_synthwell_tools["synthwell_client"].chat_fast.assert_called()


def test_optimize_keyword_triggers_tool(mock_synthwell_tools):
    """Test that 'optimize' keyword triggers optimize_journey tool."""
    response = client.post(
        "/gateway/message",
        json={"message": "Optimize the journey"},
    )
    data = response.json()
    assert "optimize_journey" in data["tools_used"]
    mock_synthwell_tools["optimize_journey"].assert_called_once()


def test_get_session(mock_conversation_manager):
    """Test getting session details."""
    mock_conversation_manager.get_conversation_by_session.return_value = Conversation(
        id="conv-123",
        session_id="sess_test123",
        surface="cli",
        user_id=None,
        state={"messages": [{"role": "user", "content": "Hello"}]},
        current_intent="greeting",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    response = client.get("/gateway/session/sess_test123")
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == "sess_test123"
    assert data["surface"] == "cli"
    assert data["message_count"] == 1


def test_get_session_not_found(mock_conversation_manager):
    """Test getting a non-existent session."""
    mock_conversation_manager.get_conversation_by_session.return_value = None

    response = client.get("/gateway/session/nonexistent")
    assert response.status_code == 200
    data = response.json()
    assert "error" in data


def test_message_response_includes_metadata():
    """Test that message response includes expected metadata."""
    response = client.post(
        "/gateway/message",
        json={"message": "Hello"},
    )
    data = response.json()
    assert "metadata" in data
    assert "conversation_id" in data["metadata"]
    assert "surface" in data["metadata"]
    assert "message_count" in data["metadata"]


def test_cohort_response_includes_tool_results(mock_synthwell_tools):
    """Test that cohort generation includes tool results in metadata."""
    response = client.post(
        "/gateway/message",
        json={"message": "Generate a cohort for seniors in Miami"},
    )
    data = response.json()
    assert "tool_results" in data["metadata"]
    assert "cohort" in data["metadata"]["tool_results"]
    assert data["metadata"]["tool_results"]["cohort"]["cohort_id"] == "cohort_test123"


def test_simulation_response_includes_delta(mock_synthwell_tools):
    """Test that simulation includes delta in response."""
    response = client.post(
        "/gateway/message",
        json={"message": "Simulate the journey"},
    )
    data = response.json()
    assert "simulation" in data["metadata"]["tool_results"]
    assert "delta" in data["metadata"]["tool_results"]["simulation"]
    assert data["metadata"]["tool_results"]["simulation"]["baseline_enrollment"] == 0.042


def test_affirmative_continues_cohort_to_journey(mock_conversation_manager, mock_synthwell_tools):
    """Test that saying 'yes' after cohort generation triggers create_journey."""
    # Set up conversation with previous cohort generation that offered journey creation
    mock_conv = Conversation(
        id=str(uuid.uuid4()),
        session_id="sess_continuation",
        surface="cli",
        user_id=None,
        state={
            "messages": [
                {"role": "user", "content": "Generate a cohort for Miami"},
                {
                    "role": "assistant",
                    "content": "I've generated a cohort for Miami. Would you like me to create a journey for this cohort?",
                    "tools_used": ["generate_cohort"],
                },
            ],
            "last_tool_results": {"cohort": {"cohort_id": "cohort_test123"}},
        },
        current_intent="generate_cohort",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    mock_conversation_manager.get_or_create_conversation.return_value = mock_conv

    response = client.post(
        "/gateway/message",
        json={"message": "yes", "session_id": "sess_continuation"},
    )
    data = response.json()
    assert "create_journey" in data["tools_used"]
    mock_synthwell_tools["create_journey"].assert_called()


def test_affirmative_ready_to_generate_triggers_journey(mock_conversation_manager, mock_synthwell_tools):
    """Test that saying 'yes' after TerryAnn asks 'Ready to generate?' triggers create_journey."""
    # This matches the actual TerryAnn response pattern from production
    mock_conv = Conversation(
        id=str(uuid.uuid4()),
        session_id="sess_ready_generate",
        surface="cli",
        user_id=None,
        state={
            "messages": [
                {"role": "user", "content": "Create an AEP acquisition journey for Tampa Bay"},
                {
                    "role": "assistant",
                    "content": "**AEP acquisition journey for Tampa Bay Area** — got it.\n\n**Ready to generate?** This takes about 60-90 seconds.",
                    "tools_used": [],
                },
            ],
            "last_tool_results": {
                "pending_journey_confirmation": {
                    "params": {"campaign_type": "aep", "geography": {"zip_codes": ["33601"]}},
                    "awaiting_confirmation": True,
                }
            },
        },
        current_intent=None,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    mock_conversation_manager.get_or_create_conversation.return_value = mock_conv

    response = client.post(
        "/gateway/message",
        json={"message": "yes", "session_id": "sess_ready_generate"},
    )
    data = response.json()
    assert "create_journey" in data["tools_used"]
    mock_synthwell_tools["create_journey"].assert_called()


def test_affirmative_continues_journey_to_simulation(mock_conversation_manager, mock_synthwell_tools):
    """Test that saying 'yes' after journey creation triggers simulate_journey."""
    mock_conv = Conversation(
        id=str(uuid.uuid4()),
        session_id="sess_sim_continuation",
        surface="cli",
        user_id=None,
        state={
            "messages": [
                {"role": "user", "content": "Create a journey"},
                {
                    "role": "assistant",
                    "content": "I've created a journey. Shall I simulate this journey with a cohort?",
                    "tools_used": ["create_journey"],
                },
            ],
            "last_tool_results": {"journey": {"journey_id": "journey_test123"}},
        },
        current_intent="create_journey",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    mock_conversation_manager.get_or_create_conversation.return_value = mock_conv

    response = client.post(
        "/gateway/message",
        json={"message": "sure", "session_id": "sess_sim_continuation"},
    )
    data = response.json()
    assert "simulate_journey" in data["tools_used"]
    mock_synthwell_tools["simulate_journey_changes"].assert_called()


def test_affirmative_continues_simulation_to_optimization(mock_conversation_manager, mock_synthwell_tools):
    """Test that saying 'yes' after simulation triggers optimize_journey."""
    mock_conv = Conversation(
        id=str(uuid.uuid4()),
        session_id="sess_opt_continuation",
        surface="cli",
        user_id=None,
        state={
            "messages": [
                {"role": "user", "content": "Simulate the journey"},
                {
                    "role": "assistant",
                    "content": "Simulation complete. Would you like me to optimize the journey based on these results?",
                    "tools_used": ["simulate_journey"],
                },
            ],
            "last_tool_results": {"simulation": {"simulation_id": "sim_test123"}},
        },
        current_intent="simulate_journey",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    mock_conversation_manager.get_or_create_conversation.return_value = mock_conv

    response = client.post(
        "/gateway/message",
        json={"message": "go ahead", "session_id": "sess_opt_continuation"},
    )
    data = response.json()
    assert "optimize_journey" in data["tools_used"]
    mock_synthwell_tools["optimize_journey"].assert_called()
