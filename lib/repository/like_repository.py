from lib.database.sqlite import SQLiteDatabase
from lib.interface.secret_manager import ISecretManager
from lib.enums.database import TableNameEnum
from lib.models.like_model import Like
from pathlib import Path


class LikeRepository(SQLiteDatabase):
    def __init__(self):
        super().__init__(Like, TableNameEnum.Like)

        self.__execute_create_table__()

    def __execute_create_table__(self) -> None:
        q = ""

        with open(Path("./sql/create_like_table.sql"), "r") as f:
            q = f.read()

        self.execute_query(q)
        self.execute_query("SELECT name FROM sqlite_master WHERE type='table';")
