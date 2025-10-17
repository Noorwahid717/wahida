"""Supabase authentication utilities."""

from __future__ import annotations

from fastapi import Depends, HTTPException, Request, status
from supabase import Client, create_client

from app.core.config import settings


def get_supabase_client() -> Client:
    """Get Supabase client."""
    if not settings.supabase_url or not settings.supabase_anon_key:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Supabase not configured")
    return create_client(settings.supabase_url, settings.supabase_anon_key)


def get_current_user(request: Request) -> dict:
    """Extract user from Supabase JWT token."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Missing or invalid token")

    token = auth_header.split(" ")[1]
    supabase = get_supabase_client()
    try:
        user = supabase.auth.get_user(token)
        return user.user.model_dump() if user.user else {}
    except Exception as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, f"Invalid token: {str(e)}") from e