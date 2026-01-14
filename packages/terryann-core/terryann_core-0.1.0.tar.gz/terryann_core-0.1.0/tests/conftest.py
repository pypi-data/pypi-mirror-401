"""Test configuration and fixtures."""

import uuid
from datetime import datetime, timezone
from typing import Any
from unittest.mock import MagicMock

import pytest

from app.gateway.session import ConversationManager, Conversation


class MockSupabaseResponse:
    """Mock Supabase query response."""

    def __init__(self, data: list[dict] | dict | None = None):
        self.data = data if data is not None else []


class MockSupabaseQuery:
    """Mock Supabase query builder."""

    def __init__(self, data: list[dict] | None = None):
        self._data = data or []
        self._filters = {}

    def select(self, *args):
        return self

    def insert(self, data: dict):
        # Simulate insert with generated fields
        now = datetime.now(timezone.utc).isoformat()
        new_record = {
            "id": str(uuid.uuid4()),
            "created_at": now,
            "updated_at": now,
            **data,
        }
        self._data = [new_record]
        return self

    def update(self, data: dict):
        if self._data:
            self._data[0].update(data)
            self._data[0]["updated_at"] = datetime.now(timezone.utc).isoformat()
        return self

    def eq(self, field: str, value: Any):
        self._filters[field] = value
        # Filter data based on field
        if self._data:
            self._data = [r for r in self._data if r.get(field) == value]
        return self

    def limit(self, n: int):
        self._data = self._data[:n]
        return self

    def single(self):
        return self

    def execute(self):
        return MockSupabaseResponse(self._data)


class MockSupabaseTable:
    """Mock Supabase table."""

    def __init__(self, name: str, data: list[dict] | None = None):
        self.name = name
        self._data = data or []

    def select(self, *args):
        return MockSupabaseQuery(self._data.copy())

    def insert(self, data: dict):
        query = MockSupabaseQuery(self._data)
        return query.insert(data)

    def update(self, data: dict):
        query = MockSupabaseQuery(self._data)
        return query.update(data)


class MockSupabaseSchema:
    """Mock Supabase schema."""

    def __init__(self, tables: dict[str, list[dict]] | None = None):
        self._tables = tables or {}

    def table(self, name: str):
        return MockSupabaseTable(name, self._tables.get(name, []))


class MockSupabaseClient:
    """Mock Supabase client for testing."""

    def __init__(self, tables: dict[str, list[dict]] | None = None):
        self._tables = tables or {}

    def schema(self, name: str):
        return MockSupabaseSchema(self._tables)


@pytest.fixture
def mock_supabase_client():
    """Create a mock Supabase client."""
    return MockSupabaseClient()


@pytest.fixture
def conversation_manager(mock_supabase_client):
    """Create a ConversationManager with mock client."""
    return ConversationManager(client=mock_supabase_client)


@pytest.fixture
def mock_conversation():
    """Create a mock conversation for testing."""
    return Conversation(
        id=str(uuid.uuid4()),
        session_id="sess_test123",
        surface="cli",
        user_id=None,
        state={"messages": []},
        current_intent=None,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
