import json
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from .notes_models import Note

NOTES_FILE = Path(__file__).parent.parent / "notes_data.json"

def _serialize_note(note: Note) -> dict:
    return {
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "created_at": note.created_at.isoformat(),
    }

def _deserialize_note(data: dict) -> Note:
    return Note(
        id=data["id"],
        title=data["title"],
        content=data["content"],
        created_at=datetime.fromisoformat(data["created_at"]),
    )

# PUBLIC_INTERFACE
def load_notes() -> List[Note]:
    """Load all notes from the storage file."""
    if not NOTES_FILE.exists():
        return []
    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        raw = json.load(f)
        return [_deserialize_note(obj) for obj in raw]

# PUBLIC_INTERFACE
def save_notes(notes: List[Note]) -> None:
    """Save all notes to the storage file."""
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump([_serialize_note(note) for note in notes], f, indent=2)

# PUBLIC_INTERFACE
def get_next_id(notes: List[Note]) -> int:
    """Determine the next available note ID."""
    if not notes:
        return 1
    return max(note.id for note in notes) + 1

# PUBLIC_INTERFACE
def get_note_by_id(notes: List[Note], note_id: int) -> Optional[Note]:
    """Find a note by its ID."""
    for note in notes:
        if note.id == note_id:
            return note
    return None
