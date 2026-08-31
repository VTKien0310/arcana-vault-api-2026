from sqlmodel import Field, SQLModel, Column, ARRAY, Integer, MetaData, DateTime
from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID, uuid4
from app.core.config import settings

model_common_metadata = MetaData(schema=settings.DB_SCHEMA)


class Key(SQLModel, table=True):
    metadata = model_common_metadata
    __tablename__ = "keys"

    id: UUID = Field(
        default_factory=uuid4, primary_key=True, nullable=False, unique=True
    )
    user_id: UUID = Field(nullable=False, unique=True)
    value: str = Field(max_length=255, nullable=False)
    channels: List[int] = Field(sa_column=Column(ARRAY(Integer), nullable=False))
    expiration: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    email: Optional[str] = Field(default=None, max_length=255)
    telegram_chat_id: Optional[str] = Field(default=None, max_length=255)
    phone: Optional[str] = Field(default=None, max_length=255)
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
        default_factory=lambda: datetime.now(timezone.utc),
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
        default_factory=lambda: datetime.now(timezone.utc),
    )
