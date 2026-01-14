"""Pydantic models for source data."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SourceBase(BaseModel):
    """Base model for source data.

    Attributes:
        survey_id: Foreign key reference to Survey.
    """

    survey_id: UUID


class SourceCreate(SourceBase):
    """Model for creating source data (with survey_id in body)."""


class SourceUpdate(SourceBase):
    """Model for updating source data.

    Attributes:
    """


class Source(SourceBase):
    """Model for source data with database fields.

    Attributes:
        source_id: Unique identifier for the source.
    """

    source_id: UUID
    created_date: datetime
    updated_date: datetime
    updated_by: str

    model_config = ConfigDict(from_attributes=True)


class SourceWithUpload(Source):
    """Source response including upload information.

    Overrides optional fields from Source to be required for upload responses.
    """
