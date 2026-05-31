from datetime import datetime
from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel
from supabase_auth import User as SupabaseAuthUser


class User(BaseModel):
    id: str
    aud: str
    created_at: datetime


class UserFactory:
    @classmethod
    def user_from_spb_auth(cls, spb_auth: SupabaseAuthUser) -> User:
        return User(
            id=spb_auth.id,
            aud=spb_auth.aud,
            created_at=spb_auth.created_at,
        )


UserFactoryDep = Annotated[UserFactory, Depends()]
