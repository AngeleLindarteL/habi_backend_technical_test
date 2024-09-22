from pydantic import BaseModel


# Pydantic usage ensures type and nullish the DTO (DataTransferObject)
class LikeDTO(BaseModel):
    userId: int
    propertyId: int
