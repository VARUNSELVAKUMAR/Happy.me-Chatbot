from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint

class ORMBase(BaseModel):
    """ Base for ORM models"""

    class Config:
        from_attributes = True

class UserOut(ORMBase):
    
    id: int
    fullname: str
    username:str
    created_at: datetime
    is_superuser: bool

    class Config:
        from_attributes = True
        orm_mode = True

class UserCreate(BaseModel):

    fullname: str
    username: str
    password: str
    is_superuser: Optional[bool] = False

class UserUpdate(BaseModel):

    fullname: Optional[str]
    username: Optional[str]
    password: Optional[str]

class Token(BaseModel):

    access_token: str
    token_type: str

class TokenData(BaseModel):

    id: Optional[int] = None

class ChatOut(ORMBase):

    id: int
    user_id: int
    message: str
    created_at: datetime

class ChatResponse(BaseModel):
    message: str
    chat_history: list[str]

class ChatMessage(BaseModel):

    message: str
    emotion: str
