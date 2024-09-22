from pydantic import BaseModel
from typing import Optional


# Pydantic usage ensures type and nullish the DTO (DataTransferObject)
class GetPropertyListParams(BaseModel):
    pageSize: int = 10
    page: int = 1

    # Filters
    builtYearStart: int | None = None
    builtYearEnd: int | None = None
    city: str | None = None
    status: str | None = None
