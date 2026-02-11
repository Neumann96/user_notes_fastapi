from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import new_session
from app.db.crud.user import get_user_by_email, create_user
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.auth import RegisterBody

router = APIRouter(prefix="/auth", tags=["auth"])


async def get_db():
    async with new_session() as session:
        yield session
        
        
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    data: RegisterBody,
    db: AsyncSession = Depends(get_db),
):
    email = str(data.email)
    password = data.password
    
    existing = await get_user_by_email(db, email)
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")
    pw_bytes = password.encode("utf-8")
    print("pw chars:", len(password), "pw bytes:", len(pw_bytes))
    user = await create_user(
        db,
        email=email,
        hashed_password=hash_password(password),
    )
    return {"id": user.id, "email": user.email}


@router.post("/login")
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    user = await get_user_by_email(db, form.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    if not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    token = create_access_token(subject=user.email, expires_minutes=60)
    return {"access_token": token, "token_type": "bearer"}