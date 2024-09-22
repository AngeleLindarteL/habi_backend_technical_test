from typing import Any
from fastapi import APIRouter
from lib.dtos.like_dto import LikeDTO

from .module import LikeModule

routes = APIRouter(prefix="/like")
module = LikeModule()


@routes.post("/")
async def get_property_list(body: LikeDTO) -> Any:
    return await module.service.like_property(body)
