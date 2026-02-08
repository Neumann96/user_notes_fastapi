from pydantic import BaseModel
from typing import Optional


class NoteCreate(BaseModel):
    title: str
    content: str
    
    
class NoteRead(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int
    
    model_config = {
        "from_attributes": True  
    }
        
        
class NoteUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]