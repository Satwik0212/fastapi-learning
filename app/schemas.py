from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime



class PostBase(BaseModel) :
    title: str 
    content: str 
    published: bool = True # if no value is given in the JSON it automatically makes it true.

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
   pass

class Post(BaseModel):
    title: str 
    content: str 
    published: bool 
    created_at: datetime

class Config:
    from_attributes = True

                                # USERS

class UserCreate(BaseModel):
    email: EmailStr
    password: int | str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True