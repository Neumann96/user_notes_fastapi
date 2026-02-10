from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError

from app.db.session import new_session
from app.db.crud.user import get_user_by_email
from app.core.security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_db():
    async with new_session() as session:
        yield session
        
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
):
    try:
        email = decode_token(token)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    user = await get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user