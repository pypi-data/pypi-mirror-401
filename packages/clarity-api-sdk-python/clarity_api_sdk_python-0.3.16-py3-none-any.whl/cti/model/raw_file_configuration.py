"""Pydantic models for raw file. This is the data that has been uploaded but not ingested into the database."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class RawFileConfigurationBase(BaseModel):
    """Base model for raw file configuration.

    Attributes:
        survey_id: Foreign key reference to Survey.
        name: Name of the raw file configuration.
        configuration: Configuration settings for the raw file.
    """

    survey_id: UUID
    name: str
    configuration: dict


class RawFileConfigurationCreate(RawFileConfigurationBase):
    """Model for creating raw file configuration (with survey_id in body)."""


class RawFileConfigurationUpdate(RawFileConfigurationBase):
    """Model for updating raw file configuration.

    Attributes:
    """


class RawFileConfiguration(RawFileConfigurationBase):
    """Model for raw file configuration data with database fields.

    Attributes:
        survey_id: Unique identifier for the survey.
        raw_file_configuration_id: Unique identifier for the raw file configuration.
    """

    raw_file_configuration_id: UUID
    created_date: datetime
    updated_date: datetime
    updated_by: str

    model_config = ConfigDict(from_attributes=True)
