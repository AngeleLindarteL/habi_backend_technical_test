from lib.repository.property_repository import PropertyRepository
from lib.dtos.property_dto import GetPropertyListParams
from lib.models.property_model import ListPropertyModel
from lib.interface.pagination import PaginatedResponse


class PropertyService:
    __repository__: PropertyRepository

    def __init__(self, repository: PropertyRepository) -> None:
        self.__repository__ = repository

    async def get_property_list(
        self, params: GetPropertyListParams
    ) -> PaginatedResponse[ListPropertyModel]:
        take = params.pageSize + 1  # Takes limit + 1 to determine hasNext response prop
        skip = (params.page - 1) * params.pageSize
        has_next = False
        take_to = params.pageSize

        results = self.__repository__.get_properties_with_filters(params, take, skip)

        if len(results) > params.pageSize:
            has_next = True
        else:
            take_to = len(results)

        return PaginatedResponse(
            page=params.page,
            page_size=params.pageSize,
            data=results[:take_to],
            has_next=has_next,
            length=len(results[:take_to]),
        )
