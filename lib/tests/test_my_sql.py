from lib.interface.database import FindQuery, FindOperation
from lib.enums.database import TableNameEnum, FindOperationComparator
from lib.secrets.dot_secret_manager import DotEnvSecretManager
from lib.models.property_model import Property
from lib.database.my_sql import MySQLDatabase


sm = DotEnvSecretManager()


def test_singleton_connection() -> None:
    """Test that connection with same params is a real singleton"""

    db1 = MySQLDatabase(sm, Property, TableNameEnum.Property)
    db2 = MySQLDatabase(sm, Property, TableNameEnum.Property)

    assert db1 is db2


def find_ten_registries() -> None:
    """Find 10 registries with a simple query to properties table"""
    db = MySQLDatabase(sm, Property, TableNameEnum.Property)

    result = db.find(
        FindQuery(
            limit=10,
            offset=0,
            where=[
                FindOperation(
                    field_name="price",
                    operator=FindOperationComparator.GreaterThan,
                    value=0,
                )
            ],
        )
    )

    assert len(result) == 10
    assert isinstance(result[0], Property)
