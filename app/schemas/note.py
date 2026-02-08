from pydantic import BaseModel


class NoteCreate(BaseModel):
    title: str
    content: str
    
    
class NoteRead(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int
    
    class Config(BaseModel):
        from_attributes = True