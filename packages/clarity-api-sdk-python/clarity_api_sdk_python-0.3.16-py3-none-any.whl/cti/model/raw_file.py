"""Pydantic models for raw file. This is the data that has been uploaded but not ingested into the database."""

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator


class RawFileState(str, Enum):
    """State of a raw file upload."""

    UPLOADING = "uploading"
    READY = "ready"
    ERROR = "error"


class RawFileBase(BaseModel):
    """Base model for raw file data.

    Attributes:
        survey_id: Foreign key reference to Survey.
        raw_file_configuration_id: Foreign key reference to RawFileConfiguration.
        file_name: Name of the external raw file.
        file_size: Size of the external raw file in bytes.
    """

    survey_id: UUID
    raw_file_configuration_id: UUID
    file_name: str
    file_size: int

    @field_validator("file_name")
    @classmethod
    def validate_file_name(cls, value: str) -> str:
        """Validate that file_name has a '.xtf' or '.jsf' extension.

        Args:
            value: Name of the external raw file.

        Returns:
            The validated file_name.

        Raises:
            ValueError: If file_name does not have a '.xtf' or '.jsf' extension.
        """
        if not value.lower().endswith((".xtf", ".jsf")):
            raise ValueError("file_name must have a '.xtf' or '.jsf' extension")
        return value


class RawFileCreate(RawFileBase):
    """Model for creating raw file data (with survey_id in body)."""


class RawFileUpdate(RawFileBase):
    """Model for updating raw file data.

    Attributes:
    """


class RawFile(RawFileBase):
    """Model for raw file data with database fields.

    Attributes:
        raw_file_id: Unique identifier for the source.
        state: Upload state (uploading, ready, error).
        uri: uri for raw file, will allow AWS S3, Google Cloud Storage, NFS, URL, or Azure Blob URI (set after upload initiated).
        meta_data: meta data for the uri
        upload_id: S3 multipart upload ID (present while uploading, cleared when complete).
    """

    raw_file_id: UUID
    state: RawFileState = RawFileState.UPLOADING
    uri: str | None = None
    meta_data: dict
    upload_id: str | None = None
    created_date: datetime
    updated_date: datetime
    updated_by: str

    model_config = ConfigDict(from_attributes=True)


class RawFileWithUpload(RawFile):
    """RawFile response including upload information.

    Overrides optional fields from RawFile to be required for upload responses.
    """
