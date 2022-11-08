from typing import Optional
from pydantic import BaseModel, Field

from uuid import UUID, uuid4

class User(BaseModel):
    id: UUID = Field(default_factory=uuid4, alias="_id")
    name: str

class UserCreate(BaseModel):
    name: str

class UserUpdate(BaseModel):
    name: Optional[str]

class UserRead(BaseModel):
    id: UUID = Field(alias="_id")
    name: str
