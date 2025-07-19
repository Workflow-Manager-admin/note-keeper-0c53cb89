from fastapi import FastAPI, HTTPException, Path, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from dotenv import load_dotenv
import os

from .notes_models import Note, NoteCreate, NoteUpdate
from .notes_storage import (
    load_notes,
    save_notes,
    get_next_id,
    get_note_by_id
)

# Load environment settings from .env on startup (best practice)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))

app = FastAPI(
    title="Notes Backend API",
    description="A FastAPI backend for CRUD notes with file-based persistence.",
    version="1.0.0",
    openapi_tags=[
        {"name": "Notes", "description": "Operations on notes"}
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Health"])
def health_check():
    """Health Check endpoint."""
    return {"message": "Healthy"}


# PUBLIC_INTERFACE
@app.get("/notes", response_model=List[Note], tags=["Notes"], summary="List all notes")
def list_notes():
    """Return a list of all notes."""
    return load_notes()


# PUBLIC_INTERFACE
@app.get("/notes/{note_id}", response_model=Note, tags=["Notes"], summary="Get a note by ID")
def get_note(
    note_id: int = Path(..., description="The ID of the note to retrieve")
):
    """Retrieve a single note by its ID."""
    notes = load_notes()
    note = get_note_by_id(notes, note_id)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note


# PUBLIC_INTERFACE
@app.post("/notes", response_model=Note, status_code=status.HTTP_201_CREATED, tags=["Notes"], summary="Create a new note")
def create_note(note_in: NoteCreate):
    """Create a new note."""
    notes = load_notes()
    note_id = get_next_id(notes)
    from datetime import datetime
    note = Note(
        id=note_id,
        title=note_in.title,
        content=note_in.content,
        created_at=datetime.utcnow()
    )
    notes.append(note)
    save_notes(notes)
    return note


# PUBLIC_INTERFACE
@app.put("/notes/{note_id}", response_model=Note, tags=["Notes"], summary="Update an existing note")
def update_note(
    note_id: int = Path(..., description="The ID of the note to update"),
    note_in: NoteUpdate = ...,
):
    """Update a note by its ID."""
    notes = load_notes()
    note = get_note_by_id(notes, note_id)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    # Update values
    if note_in.title is not None:
        note.title = note_in.title
    if note_in.content is not None:
        note.content = note_in.content
    save_notes(notes)
    return note


# PUBLIC_INTERFACE
@app.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Notes"], summary="Delete a note")
def delete_note(
    note_id: int = Path(..., description="The ID of the note to delete")
):
    """Delete a note by its ID."""
    notes = load_notes()
    note = get_note_by_id(notes, note_id)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    notes = [n for n in notes if n.id != note_id]
    save_notes(notes)
    return None  # 204 No Content
