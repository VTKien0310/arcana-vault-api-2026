from dataclasses import dataclass
from datetime import datetime
from typing import Annotated
from fastapi import Depends
from pydantic import BaseModel
from supabase_auth import User as SupabaseAuthUser

from app.ports import SupabasePortDep


class User(BaseModel):
    id: str
    aud: str
    created_at: datetime


class UserRepository:
    def __init__(self, supabase: SupabasePortDep):
        self.__supabase = supabase

    @classmethod
    def user_from_spb_auth(cls, spb_auth: SupabaseAuthUser) -> User:
        return User(
            id=spb_auth.id,
            aud=spb_auth.aud,
            created_at=spb_auth.created_at,
        )


UserRepositoryDep = Annotated[UserRepository, Depends()]
