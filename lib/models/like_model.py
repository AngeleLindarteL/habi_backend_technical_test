from pydantic import BaseModel
from typing import Optional


class Like(BaseModel):
    id: Optional[int] = None
    property_id: int
    user_id: int
    created_at: str
