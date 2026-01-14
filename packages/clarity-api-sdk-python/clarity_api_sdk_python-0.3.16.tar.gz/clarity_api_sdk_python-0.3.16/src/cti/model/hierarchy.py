"""Pydantic models for hierarchy operations."""

from uuid import UUID

from pydantic import BaseModel


class Organization(BaseModel):
    """Pydantic model for organization hierarchy data."""

    organization_id: UUID
    organization_name: str


class Project(Organization):
    """Pydantic model for project hierarchy data."""

    project_id: UUID
    project_name: str


class Survey(Project):
    """Pydantic model for survey hierarchy data."""

    survey_id: UUID
    survey_name: str


class Source(Survey):
    """Pydantic model for source hierarchy data."""

    source_id: UUID


class RawFile(Survey):
    """Pydantic model for raw file hierarchy data."""

    raw_file_id: UUID
    raw_file_file_name: str
