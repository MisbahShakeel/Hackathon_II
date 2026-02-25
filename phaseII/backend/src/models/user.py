from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime
import uuid

if TYPE_CHECKING:
    from .todo import Todo

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship to todos
    todos: list["Todo"] = Relationship(back_populates="owner")

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: uuid.UUID
    is_active: bool
    created_at: datetime

class UserUpdate(SQLModel):
    email: Optional[str] = None
    is_active: Optional[bool] = None