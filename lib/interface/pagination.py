from abc import ABCMeta
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("Any")


@dataclass
class PaginatedResponse(Generic[T], metaclass=ABCMeta):
    page: int
    data: list[T]
    page_size: int
    has_next: bool
    length: int
