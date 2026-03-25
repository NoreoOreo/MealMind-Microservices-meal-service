from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class MealBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    calories: Optional[int] = Field(default=0, ge=0)


class MealCreate(MealBase):
    pass


class MealUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    calories: Optional[int] = Field(None, ge=0)


class MealOut(MealBase):
    id: str
    served_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True
