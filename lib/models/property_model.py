from pydantic import BaseModel
from datetime import datetime


class Property(BaseModel):
    id: int
    address: str
    city: str
    price: int
    description: str | None
    year: int | None


class ListPropertyModel(BaseModel):
    address: str
    city: str
    status: str
    price: int
    description: str | None
    year: int | None
