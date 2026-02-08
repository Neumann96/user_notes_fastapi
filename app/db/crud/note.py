from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.note import Note


async def create_note(db: AsyncSession, title: str, content: str, owner_id: int):
    note = Note(title=title, content=content, owner_id=owner_id)
    db.add(note)
    await db.commit()
    await db.refresh(note)
    return note


async def get_notes_by_owner(db: AsyncSession, owner_id: id):
    result = await db.execute(
        select(Note).where(Note.owner_id == owner_id)
    )
    return result.scalars().all()


async def get_note(db: AsyncSession, note_id: int, owner_id: int):
    result = await db.execute(
        select(Note).where(Note.id == note_id, Note.owner_id == owner_id)
    )
    return result.scalar_one_or_none()