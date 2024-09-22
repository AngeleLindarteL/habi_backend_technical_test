import mysql.connector as mysql
from typing import Generic, Any

from lib.database.sql_db import SQLDatabase
from lib.utils.singleton import SingletonBase
from lib.interface.database import (
    IDatabase,
    FindQuery,
    FindOperation,
    ModelType,
)
from lib.interface.secret_manager import ISecretManager
from lib.enums.database import TableNameEnum


class MySQLDatabase(SingletonBase, IDatabase, SQLDatabase):
    __table_name__: str
    __entity__: ModelType

    def __init__(
        self,
        sm: ISecretManager,
        entity: Generic[ModelType],
        table_name: TableNameEnum,
    ) -> None:
        """Uses dependency injection + singleton to be resource efficient"""
        self.__table_name__ = table_name.value
        self.__entity__ = entity

        self.__connection__ = mysql.connect(
            user=sm.get(
                "sql_user",
                "",
            ),
            password=sm.get(
                "sql_password",
                "",
            ),
            host=sm.get(
                "sql_host",
                "",
            ),
            port=sm.get(
                "sql_port",
                "",
            ),
            database=sm.get(
                "sql_database",
                "",
            ),
        )

        SQLDatabase.__init__(self, self.__entity__, self.__table_name__, "%s")

    def findOne(self, queries: list[FindOperation]) -> ModelType | None:
        cursor = self.__connection__.cursor(dictionary=True)
        statement = self.__build_composed_query__(queries)

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

        cursor.execute(query_str, statement.value_set)

        results = cursor.fetchall()
        cursor.close()

        return [entity(**result) for result in results]

    def execute_query(self, query: str) -> None:
        cursor = self.__connection__.cursor()
        cursor.execute(query)
        cursor.close()

    def custom_query_find(self, query: str, values: list[Any]) -> list[dict]:
        cursor = self.__connection__.cursor(dictionary=True)
        cursor.execute(query, values)
        results = cursor.fetchall()
        cursor.close()

        return results

    def save(self, obj: ModelType) -> ModelType:
        raise NotImplementedError("Implement update operation")
