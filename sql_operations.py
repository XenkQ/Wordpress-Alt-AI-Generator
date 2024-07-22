import json
import mysql.connector

import sql_structure_queries
from sql_table_data_queries import SQL_Table_Data_Queries
from enum import Enum


class GetDataOperations(Enum):
    IMAGE_IDS_LINKS_WITHOUT_ALT = 0,
    IMAGE_IDS_LINKS_WITH_EXISTING_EMPTY_ALT_ROW = 1,
    WORDPRESS_TABLES_PREFIX = 2


class ChangeDataOperations(Enum):
    INSERT_ROW_WITH_IMAGE_ALT_DATA = 0,
    UPDATE_EXISTING_IMAGE_ALT_DATA = 1


class DataBaseOperations(Enum):
    GET_WORDPRESS_TABLES_PREFIX = 0


class SQL_Operations:
    with open('credentials.json', 'r') as file:
        data = json.loads(file.read())
        __sql_server_params = data['database_mode_credentials']

    def __init__(self):
        self.queries = SQL_Table_Data_Queries(self.get_tables_prefix())

    def get_tables_prefix(self) -> str:
        if self.can_database_user_insert_and_update():
            return self.get_data(GetDataOperations.WORDPRESS_TABLES_PREFIX)[0][0] + "_"

        return ''

    @classmethod
    def can_connect_to_database(cls) -> bool:
        result = False

        try:
            connection = mysql.connector.connect(**cls.__sql_server_params)
            result = connection.is_connected()
            connection.close()
        except Exception:
            pass

        return result

    @classmethod
    def can_database_user_insert_and_update(cls) -> bool:
        if not cls.can_connect_to_database():
            return False

        connection = mysql.connector.connect(**cls.__sql_server_params)
        cursor = connection.cursor()

        query = sql_structure_queries.SELECT_CURRENT_USER_PRIVILEGES
        cursor.execute(query)

        result = cursor.fetchall()[1]

        if 'INSERT' in result[0] and 'UPDATE' in result[0]:
            return True

        return False

    def get_data(self, operation: GetDataOperations) -> list:
        connection = mysql.connector.connect(**self.__sql_server_params)
        cursor = connection.cursor()

        query = None
        result = None

        if operation == GetDataOperations.IMAGE_IDS_LINKS_WITHOUT_ALT:
            query = self.queries.SELECT_IMAGE_IDS_LINKS_WITHOUT_ALT
        elif operation == GetDataOperations.IMAGE_IDS_LINKS_WITH_EXISTING_EMPTY_ALT_ROW:
            query = self.queries.SELECT_IMAGE_IDS_LINKS_WITH_EXISTING_EMPTY_ALT_ROW
        elif operation == GetDataOperations.WORDPRESS_TABLES_PREFIX:
            query = sql_structure_queries.SELECT_TABLE_PREFIX

        if query:
            cursor.execute(query)
            result = cursor.fetchall()

        cursor.close()
        connection.close()

        if result:
            return result
        else:
            return []

    def change_data(self, post_id: int, alt_text: str, operation: ChangeDataOperations):
        connection = mysql.connector.connect(**self.__sql_server_params)
        cursor = connection.cursor()

        if operation == ChangeDataOperations.INSERT_ROW_WITH_IMAGE_ALT_DATA:
            cursor.execute(self.queries.INSERT_IMAGE_ALT_DATA, (post_id, alt_text))
        elif operation == ChangeDataOperations.UPDATE_EXISTING_IMAGE_ALT_DATA:
            cursor.execute(self.queries.UPDATE_IMAGE_ALT_DATA, (alt_text, post_id))

        connection.commit()

        cursor.close()
        connection.close()
