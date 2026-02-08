from fastapi import FastAPI
from app.db.session import new_session, engine
from app.db.base import Base
from app.routers import user_router, note_router

from app.models import user, note

app = FastAPI()
app.include_router(user_router.router)
app.include_router(note_router.router)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)