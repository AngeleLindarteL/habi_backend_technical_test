from typing import Generic, Any
import sqlite3

from lib.utils.singleton import SingletonBase
from lib.interface.database import (
    IDatabase,
    FindQuery,
    FindOperation,
    ModelType,
)
from lib.enums.database import TableNameEnum
from .sql_db import SQLDatabase


class SQLiteDatabase(SingletonBase, IDatabase, SQLDatabase):
    __table_name__: str
    __entity__: ModelType

    def __init__(
        self,
        entity: Generic[ModelType],
        table_name: TableNameEnum,
    ) -> None:
        """Uses dependency injection + singleton to be resource efficient"""
        self.__table_name__ = table_name.value
        self.__entity__ = entity

        self.__connection__ = sqlite3.connect("./likes.db")

        SQLDatabase.__init__(self, self.__entity__, self.__table_name__, "?")

    def findOne(self, queries: list[FindOperation]) -> ModelType | None:
        cursor = self.__connection__.cursor(dictionary=True)
        statement = self.__build_composed_query__(queries, None)

        cursor.execute(statement.query, statement.value_set)

        result = cursor.fetchone()
        cursor.close()

        return self.__entity__(**result)

    def find(self, query: FindQuery) -> list[ModelType]:
        cursor = self.__connection__.cursor(dictionary=True)
        entity = (
            query.overwrite_model
            if query.overwrite_model is not None
            else self.__entity__
        )

        statement = self.__build_composed_query__(query.where, query.join)
        query_str = statement.query

        if query.limit is not None:
            query_str = f"{query_str} LIMIT {query.limit}"

        if query.limit is not None:
            query_str = f"{query_str} OFFSET {query.limit}"

        print(f"query is {query_str}")

        cursor.execute(query_str, statement.value_set)

        results = cursor.fetchall()
        cursor.close()

        return [entity(**result) for result in results]

    def custom_query_find(self, query: str, values: list[Any]) -> list[dict]:
        cursor = self.__connection__.cursor(dictionary=True)
        cursor.execute(query, values)
        results = cursor.fetchall()
        cursor.close()

        return results

    def execute_query(self, query: str) -> None:
        cursor = self.__connection__.cursor()
        cursor.execute(query)
        result = cursor.fetchall()

        print(f"Query result {result}")

        cursor.close()

    def save(self, obj: ModelType) -> ModelType:
        dict_obj = obj.model_dump(exclude_none=True)
        print(f"dict is {dict_obj}")
        model_keys = dict_obj.keys()

        keys = ", ".join(model_keys)
        values = ", ".join(["?" for _ in range(len(dict_obj))])

        query = f"""
            INSERT INTO `{self.__table_name__}` ({keys})
            VALUES ({values})
        """

        cursor = self.__connection__.cursor()
        cursor.execute(query, tuple(dict_obj.values()))
        self.__connection__.commit()
        inserted_row_id = cursor.lastrowid

        print(f"{cursor.rowcount} Rows affected (Inserted) | Row ID: {inserted_row_id}")
        cursor.close()

        return self.__entity__(**dict_obj, id=inserted_row_id)
