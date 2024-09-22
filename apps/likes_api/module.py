from .service import LikeService

from lib.secrets.dot_secret_manager import DotEnvSecretManager
from lib.repository.like_repository import LikeRepository


class LikeModule:
    service: LikeService

    def __init__(self) -> None:
        like_repository = LikeRepository()
        self.service = LikeService(like_repository)
