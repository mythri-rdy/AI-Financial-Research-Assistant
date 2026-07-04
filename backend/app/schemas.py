from datetime import datetime
from pydantic import BaseModel, EmailStr
class UserCreate(BaseModel):#user request
    email: EmailStr
    password: str
class UserOut(BaseModel):#user response
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        from_attributes = True
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
class DocumentOut(BaseModel):
    id: int
    filename: str
    upload_date: datetime
    status: str
    class Config:
        from_attributes = True
class ChatRequest(BaseModel):
    document_id: int
    question: str
class ChatResponse(BaseModel):
    answer: str
    sources: list[str]
