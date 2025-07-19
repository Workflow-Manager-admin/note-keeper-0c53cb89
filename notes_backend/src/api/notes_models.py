from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# PUBLIC_INTERFACE
class NoteBase(BaseModel):
    """Base model for a note."""
    title: str = Field(..., description="Title of the note")
    content: str = Field(..., description="Content of the note")

# PUBLIC_INTERFACE
class NoteCreate(NoteBase):
    """Model for creating a note."""
    pass

# PUBLIC_INTERFACE
class NoteUpdate(BaseModel):
    """Model for updating a note."""
    title: Optional[str] = Field(None, description="Updated title of the note")
    content: Optional[str] = Field(None, description="Updated content of the note")

# PUBLIC_INTERFACE
class Note(NoteBase):
    """Model representing a note with ID and creation time."""
    id: int = Field(..., description="Unique identifier for the note")
    created_at: datetime = Field(..., description="Timestamp for when the note was created")
