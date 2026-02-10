from app.db.base import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    
    notes = relationship("Note", 
                         back_populates="owner", 
                         cascade="all, delete-orphan",
                        )