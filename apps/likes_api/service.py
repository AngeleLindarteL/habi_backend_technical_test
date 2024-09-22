from datetime import datetime
from lib.repository.like_repository import LikeRepository
from lib.dtos.like_dto import LikeDTO
from lib.models.like_model import Like


class LikeService:
    __repository__: LikeRepository

    def __init__(self, repository: LikeRepository) -> None:
        self.__repository__ = repository

    async def like_property(self, params: LikeDTO) -> Like:
        return self.__repository__.save(
            Like(
                created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
                property_id=params.propertyId,
                user_id=params.userId,
            )
        )
