from typing import Generic, Optional, Union

from lib.interface.database import (
    FindQuery,
    FindOperation,
    ModelType,
    JoinStatement,
    StatementResult,
)
from lib.enums.database import TableNameEnum


class SQLDatabase:
    __table_name__: str
    __entity__: ModelType
    __position_marker__: str

    def __init__(
        self, entity: Generic[ModelType], table_name: str, position_marker: str
    ) -> None:
        """Common SQL Databases Methods/Implementations"""
        self.__table_name__ = table_name
        self.__entity__ = entity
        self.__position_marker__ = position_marker

    def __build_composed_query__(
        self,
        queries: list[FindOperation],
        join_q: Optional[list[Union["JoinStatement", "FindQuery"]]] = None,
    ) -> StatementResult:
        where_q = self.__build_where__(queries)
        vals_arr = [q.value for q in queries]
        joins = join_q if join_q is not None else []
        join_statement = ""

        for join in joins:
            built_join = self.__build_individual_join__(join)
            vals_arr.extend(built_join.value_set)

            join_statement = f"{join_statement}\n {built_join.query}"

        query_str = f"SELECT * FROM `{self.__table_name__}` {self.__table_name__} {join_statement} WHERE {where_q}"

        return StatementResult(vals_arr, query_str)

    def __build_where__(self, conditions: list[FindOperation]) -> str:
        where_arr = [
            f"{self.__table_name__}.{q.field_name} {q.operator.value} {self.__position_marker__}"
            for q in conditions
        ]
        return " AND ".join(where_arr)

    def __build_individual_join__(
        self, statement: Union["JoinStatement", "FindQuery"]
    ) -> StatementResult:
        comp_query = f"{statement.table}"
        value_set = []

        if isinstance(statement, FindQuery):
            built_res = self.__build_composed_query__(statement.where, statement.join)
            value_set = built_res.value_set
            comp_query = f"({built_res.query})"

        return StatementResult(
            value_set,
            f"""
                {statement.type} JOIN {comp_query} {statement.table}
                ON {statement.table}.{statement.foreign_field} = {self.__table_name__}.{statement.local_field}
            """,
        )
