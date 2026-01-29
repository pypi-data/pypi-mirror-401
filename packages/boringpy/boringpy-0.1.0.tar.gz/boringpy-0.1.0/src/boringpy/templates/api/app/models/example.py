"""Example database models."""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class ExampleBase(SQLModel):
    """Base fields for Example model."""

    name: str = Field(index=True, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    is_active: bool = Field(default=True)


class Example(ExampleBase, table=True):
    """
    Example database model.
    
    This is a sample model showing SQLModel usage.
    Replace or extend this for your application needs.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ExampleCreate(ExampleBase):
    """Schema for creating an Example."""

    pass


class ExampleUpdate(SQLModel):
    """Schema for updating an Example."""

    name: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    is_active: Optional[bool] = None


class ExamplePublic(ExampleBase):
    """Schema for public Example data."""

    id: int
    created_at: datetime
    updated_at: datetime
