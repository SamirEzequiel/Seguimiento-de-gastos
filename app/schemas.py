from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime
from .models import Category

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ExpenseBase(BaseModel):
    amount: float = Field(gt=0)
    category: Category
    description: Optional[str] = None
    date: datetime

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseUpdate(BaseModel):
    amount: Optional[float] = Field(default=None, gt=0)
    category: Optional[Category] = None
    description: Optional[str] = None
    date: Optional[datetime] = None

class ExpenseOut(ExpenseBase):
    id: str
    user_id: str

    model_config = ConfigDict(from_attributes=True)