from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.schemas.note import NoteCreate, NoteRead
from app.db.session import new_session
from app.models.user import User
from app.auth.auth import get_current_user
from app.db.crud.note import create_note, get_notes_by_owner


router = APIRouter(prefix="/notes", tags=["notes"])

OWNER_ID = 1


async def get_db():
    async with new_session() as session:
        yield session
        
        
@router.post("/", response_model=NoteRead)
async def create_new_note(note: NoteCreate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    new_note = await create_note(db, note.title, note.content, user.id)
    return new_note


@router.get("/", response_model=List[NoteRead])
async def read_notes(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    notes = await get_notes_by_owner(db, user.id)
    return notes