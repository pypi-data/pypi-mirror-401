"""Supabase database client initialization."""

from functools import lru_cache

from supabase import Client, create_client

from app.config import get_settings


@lru_cache
def get_supabase_client() -> Client:
    """
    Get cached Supabase client instance.

    Uses service key for server-side operations with full access.
    """
    settings = get_settings()

    if not settings.supabase_url or not settings.supabase_service_key:
        raise ValueError(
            "SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in environment"
        )

    return create_client(
        settings.supabase_url,
        settings.supabase_service_key,
    )


def get_db() -> Client:
    """FastAPI dependency for Supabase client."""
    return get_supabase_client()
