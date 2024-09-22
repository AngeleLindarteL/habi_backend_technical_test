from enum import Enum


class FindOperationComparator(Enum):
    Equal = "="
    NotEqual = "!="
    GreaterThan = ">"
    GreaterThanOrEqual = ">="
    LessThan = "<"
    LessThanOrEqual = "<="
    In = "IN"
    NotIn = "NOT IN"


class TableNameEnum(Enum):
    StatusHistory = "status_history"
    Status = "status"
    Property = "property"
    Like = "like_history"
