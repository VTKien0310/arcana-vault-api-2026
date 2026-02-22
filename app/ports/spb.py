from functools import lru_cache
from supabase import create_client, Client
from app.core.config import settings
from typing import Annotated
from fastapi import Depends


@lru_cache()
def _get_supabase_client() -> Client:
    """Create and cache a single Supabase client instance."""
    return create_client(
        supabase_url=settings.SUPABASE_URL,
        supabase_key=settings.SUPABASE_SERVICE_ROLE_KEY,
    )


class SupabasePort:
    def __init__(self):
        self.__client = _get_supabase_client()

    def auth(self):
        return self.__client.auth

    def storage_vault(self):
        return self.__client.storage.from_("arcana-vault")


SupabasePortDep = Annotated[SupabasePort, Depends()]
