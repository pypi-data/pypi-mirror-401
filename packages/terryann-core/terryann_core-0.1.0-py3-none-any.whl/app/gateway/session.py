"""Session management for conversation state with Supabase persistence."""

import uuid
from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel
from supabase import Client

from app.db import get_supabase_client


class Conversation(BaseModel):
    """Conversation record from Supabase."""

    id: str
    session_id: str
    surface: str
    user_id: str | None = None
    state: dict[str, Any] = {}
    current_intent: str | None = None
    created_at: datetime
    updated_at: datetime


class Journey(BaseModel):
    """Journey record from Supabase."""

    id: str
    conversation_id: str | None = None
    cohort_config: dict[str, Any] = {}
    journey_data: dict[str, Any] | None = None
    simulation_results: dict[str, Any] | None = None
    status: str = "draft"
    created_at: datetime
    updated_at: datetime


class ConversationManager:
    """
    Manages conversations with Supabase persistence.

    Conversations are stored in core.conversations table.
    """

    def __init__(self, client: Client | None = None):
        self._client = client

    @property
    def client(self) -> Client:
        """Get Supabase client (lazy initialization)."""
        if self._client is None:
            self._client = get_supabase_client()
        return self._client

    async def get_or_create_conversation(
        self,
        session_id: str,
        surface: str = "cli",
        user_id: str | None = None,
    ) -> Conversation:
        """
        Get existing conversation by session_id or create a new one.

        Args:
            session_id: Unique session identifier
            surface: Client surface (cli, slack, web, mobile)
            user_id: Optional authenticated user ID

        Returns:
            Conversation record
        """
        # Try to find existing conversation
        result = (
            self.client.schema("core")
            .table("conversations")
            .select("*")
            .eq("session_id", session_id)
            .limit(1)
            .execute()
        )

        if result.data:
            row = result.data[0]
            return Conversation(
                id=row["id"],
                session_id=row["session_id"],
                surface=row["surface"],
                user_id=row["user_id"],
                state=row["state"] or {},
                current_intent=row["current_intent"],
                created_at=row["created_at"],
                updated_at=row["updated_at"],
            )

        # Create new conversation
        new_conversation = {
            "session_id": session_id,
            "surface": surface,
            "user_id": user_id,
            "state": {},
            "current_intent": None,
        }

        result = (
            self.client.schema("core")
            .table("conversations")
            .insert(new_conversation)
            .execute()
        )

        row = result.data[0]
        return Conversation(
            id=row["id"],
            session_id=row["session_id"],
            surface=row["surface"],
            user_id=row["user_id"],
            state=row["state"] or {},
            current_intent=row["current_intent"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    async def update_conversation_state(
        self,
        conversation_id: str,
        state: dict[str, Any] | None = None,
        current_intent: str | None = None,
    ) -> Conversation:
        """
        Update conversation state and/or current intent.

        Args:
            conversation_id: UUID of the conversation
            state: New state dict (merged with existing state)
            current_intent: New current intent value

        Returns:
            Updated conversation record
        """
        # Build update payload
        updates: dict[str, Any] = {}

        if state is not None:
            # Get current state and merge
            current = (
                self.client.schema("core")
                .table("conversations")
                .select("state")
                .eq("id", conversation_id)
                .single()
                .execute()
            )
            current_state = current.data.get("state") or {}
            current_state.update(state)
            updates["state"] = current_state

        if current_intent is not None:
            updates["current_intent"] = current_intent

        if not updates:
            # Nothing to update, just fetch current
            result = (
                self.client.schema("core")
                .table("conversations")
                .select("*")
                .eq("id", conversation_id)
                .single()
                .execute()
            )
        else:
            result = (
                self.client.schema("core")
                .table("conversations")
                .update(updates)
                .eq("id", conversation_id)
                .execute()
            )

        row = result.data[0] if isinstance(result.data, list) else result.data
        return Conversation(
            id=row["id"],
            session_id=row["session_id"],
            surface=row["surface"],
            user_id=row["user_id"],
            state=row["state"] or {},
            current_intent=row["current_intent"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    async def get_conversation(self, conversation_id: str) -> Conversation | None:
        """Get conversation by ID."""
        result = (
            self.client.schema("core")
            .table("conversations")
            .select("*")
            .eq("id", conversation_id)
            .limit(1)
            .execute()
        )

        if not result.data:
            return None

        row = result.data[0]
        return Conversation(
            id=row["id"],
            session_id=row["session_id"],
            surface=row["surface"],
            user_id=row["user_id"],
            state=row["state"] or {},
            current_intent=row["current_intent"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    async def get_conversation_by_session(self, session_id: str) -> Conversation | None:
        """Get conversation by session_id."""
        result = (
            self.client.schema("core")
            .table("conversations")
            .select("*")
            .eq("session_id", session_id)
            .limit(1)
            .execute()
        )

        if not result.data:
            return None

        row = result.data[0]
        return Conversation(
            id=row["id"],
            session_id=row["session_id"],
            surface=row["surface"],
            user_id=row["user_id"],
            state=row["state"] or {},
            current_intent=row["current_intent"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    async def list_journeys(self, limit: int = 20) -> list[Journey]:
        """List recent journeys."""
        result = (
            self.client.schema("core")
            .table("journeys")
            .select("*")
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )

        return [
            Journey(
                id=row["id"],
                conversation_id=row["conversation_id"],
                cohort_config=row["cohort_config"] or {},
                journey_data=row["journey_data"],
                simulation_results=row["simulation_results"],
                status=row["status"],
                created_at=row["created_at"],
                updated_at=row["updated_at"],
            )
            for row in result.data
        ]

    async def get_journey(self, journey_id: str) -> Journey | None:
        """Get journey by ID (supports full UUID or short prefix)."""
        row = None

        # Try exact match first (full UUID)
        try:
            result = (
                self.client.schema("core")
                .table("journeys")
                .select("*")
                .eq("id", journey_id)
                .limit(1)
                .execute()
            )
            if result.data:
                row = result.data[0]
        except Exception:
            # Invalid UUID format, try prefix match
            pass

        # If no exact match and looks like a short ID, try prefix match
        if not row and len(journey_id) < 36 and len(journey_id) >= 4:
            try:
                # Fetch recent journeys and filter by prefix
                result = (
                    self.client.schema("core")
                    .table("journeys")
                    .select("*")
                    .order("created_at", desc=True)
                    .limit(100)
                    .execute()
                )
                for r in result.data:
                    if r["id"].startswith(journey_id):
                        row = r
                        break
            except Exception:
                return None

        if not row:
            return None

        return Journey(
            id=row["id"],
            conversation_id=row["conversation_id"],
            cohort_config=row["cohort_config"] or {},
            journey_data=row["journey_data"],
            simulation_results=row["simulation_results"],
            status=row["status"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    async def save_journey(
        self,
        conversation_id: str | None,
        cohort_config: dict[str, Any],
        journey_data: dict[str, Any] | None = None,
        status: str = "draft",
    ) -> Journey:
        """Save a new journey."""
        new_journey = {
            "conversation_id": conversation_id,
            "cohort_config": cohort_config,
            "journey_data": journey_data,
            "status": status,
        }

        result = (
            self.client.schema("core")
            .table("journeys")
            .insert(new_journey)
            .execute()
        )

        row = result.data[0]
        return Journey(
            id=row["id"],
            conversation_id=row["conversation_id"],
            cohort_config=row["cohort_config"] or {},
            journey_data=row["journey_data"],
            simulation_results=row["simulation_results"],
            status=row["status"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )


def generate_session_id() -> str:
    """Generate a new session ID."""
    return f"sess_{uuid.uuid4().hex}"


# Global conversation manager instance
conversation_manager = ConversationManager()
