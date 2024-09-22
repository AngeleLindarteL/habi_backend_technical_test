from abc import abstractmethod, ABCMeta
from typing import Generic, TypeVar, Optional, Any, Literal, Union, Sequence, Dict, List
from dataclasses import dataclass, field
from pydantic import BaseModel
from lib.enums.database import FindOperationComparator

ModelType = TypeVar("ModelType", bound=BaseModel)


@dataclass
class StatementResult:
    value_set: Sequence[Any] | Dict[str, Any]
    query: str


@dataclass
class JoinStatement:
    table: str
    local_field: str
    foreign_field: str
    type: Optional[Literal["LEFT", "INNER", "RIGHT"]] = ""


@dataclass
class FindOperation:
    field_name: str
    operator: FindOperationComparator
    value: str


@dataclass
class FindQuery:
    where: list[FindOperation]
    limit: Optional[int]
    offset: Optional[int]
    join: Optional[List[Union["JoinStatement", "FindQuery"]]] = field(
        default_factory=list
    )
    overwrite_model: Optional[ModelType] | None = None


@dataclass
class UpdateQuery:
    where: list[FindOperation]
    update: dict[str, Any]


class IDatabase(Generic[ModelType], metaclass=ABCMeta):
    @abstractmethod
    def findOne(self, query: list[FindOperation]) -> ModelType | None:
        raise NotImplementedError("Implement find by unique operation")

    @abstractmethod
    def find(self, query: FindQuery) -> list[ModelType]:
        raise NotImplementedError("Implement find operation")

    @abstractmethod
    def custom_query_find(self, query: str, values: list[Any]) -> list[dict]:
        raise NotImplementedError("Implement find operation")

    @abstractmethod
    def execute_query(self, query: str) -> None:
        raise NotImplementedError("Implement find operation")

    @abstractmethod
    def save(self, obj: ModelType) -> ModelType:
        raise NotImplementedError("Implement update operation")
