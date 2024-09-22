from lib.database.my_sql import MySQLDatabase
from lib.interface.secret_manager import ISecretManager
from lib.enums.database import TableNameEnum
from lib.models.property_model import Property, ListPropertyModel
from lib.constants.properties_read import allowed_properties
from lib.dtos.property_dto import GetPropertyListParams


class PropertyRepository(MySQLDatabase):
    def __init__(self, sm: ISecretManager):
        super().__init__(sm, Property, TableNameEnum.Property)

    def get_properties_with_filters(
        self, properties: GetPropertyListParams, limit: int, skip: int
    ) -> list[ListPropertyModel]:
        args = []
        query = f"""
            SELECT property.*, statuses.status, statuses.status_label
            FROM property
            LEFT JOIN (
                SELECT t.property_id, sts.name AS status, sts.label as status_label
                FROM status_history t
                LEFT JOIN status sts ON sts.id = t.status_id
                WHERE t.update_date = (
                    SELECT MAX(t2.update_date)
                    FROM status_history t2
                    WHERE t2.property_id = t.property_id
                )
            ) statuses ON property.id = statuses.property_id
            WHERE
                property.price > 0 AND
                statuses.status IN ({",".join(allowed_properties)})
        """

        if properties.status is not None:
            query = f"{query} AND status = %s"
            args.append(properties.status)

        if properties.city is not None:
            query = f"{query} AND city = %s"
            args.append(properties.city)

        if properties.builtYearStart is not None:
            query = f"{query} AND year >= %s"
            args.append(properties.builtYearStart)

        if properties.builtYearEnd is not None:
            query = f"{query} AND year <= %s"
            args.append(properties.builtYearEnd)

        query = f"{query} LIMIT %s OFFSET %s"
        args.append(limit)
        args.append(skip)

        results = self.custom_query_find(query, args)

        return [ListPropertyModel(**result) for result in results]
