from fastapi import FastAPI
from app.db.session import new_session, engine
from app.db.base import Base

from app.models import user, note

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)