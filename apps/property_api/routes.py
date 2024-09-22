from typing import Any
from fastapi import APIRouter, Query
from typing import Annotated, Literal
from lib.dtos.property_dto import GetPropertyListParams

from .module import PropertyModule

routes = APIRouter(prefix="/property")
module = PropertyModule()


@routes.get("/list")
async def get_property_list(params: Annotated[GetPropertyListParams, Query()]) -> Any:
    return await module.service.get_property_list(params)
