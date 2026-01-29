"""Test Attachment Schema"""
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AttachmentBase(BaseModel):
    """Test Attachment Base schema."""

    name: Optional[str] = None
    filepath: Optional[str] = None


class AttachmentCreate(AttachmentBase):
    """Test Attachment Create schema."""

    name: str
    filepath: str


class AttachmentUpdate(AttachmentBase):
    """Test Attachment Update schema."""

    pass


class AttachmentInDBBase(AttachmentBase):
    """Test Attachment Database base schema."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    run_id: int


class Attachment(AttachmentInDBBase):
    """Test Attachment schema."""

    pass


class AttachmentInDB(AttachmentInDBBase):
    pass
