"""Base models for the application."""

from pydantic import BaseModel, ConfigDict


class BaseAPIModel(BaseModel):
    """
    Base model for all API models.

    Configures common settings for Pydantic models.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        use_enum_values=True,
        str_strip_whitespace=True,
    )