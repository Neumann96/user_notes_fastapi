from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserCreate, UserRead
from app.db.session import new_session
from app.db.crud.user import get_user_by_email, create_user

router = APIRouter(prefix="/users", tags=["users"])

async def get_db():
    async with new_session() as session:
        yield session


@router.post("/", response_model=UserRead)
async def register_user(
    data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    existing = await get_user_by_email(db, data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = await create_user(
        db,
        email=data.email,
        hashed_password=data.password,
    )
    
    return user