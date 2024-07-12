import json
import mysql.connector
import sql_queries
from enum import Enum

class GetDataOperations(Enum):
    IMAGE_IDS_LINKS_WITHOUT_ALT = 0,
    IMAGE_IDS_LINKS_WITH_EXISTING_EMPTY_ALT_ROW = 1

class ChangeDataOperations(Enum):
    INSERT_ROW_WITH_IMAGE_ALT_DATA = 0,
    UPDATE_EXISTING_IMAGE_ALT_DATA = 1


sql_server_params: dict

with open('credentials.json', 'r') as file:
    data = json.loads(file.read())
    sql_server_params = data['database_mode_credentials']

def get_data(operation: GetDataOperations) -> list:
    connection = mysql.connector.connect(**sql_server_params)
    cursor = connection.cursor()

    query: str
    if operation == GetDataOperations.IMAGE_IDS_LINKS_WITHOUT_ALT:
        query = sql_queries.SELECT_IMAGE_IDS_LINKS_WITHOUT_ALT
    elif operation == GetDataOperations.IMAGE_IDS_LINKS_WITH_EXISTING_EMPTY_ALT_ROW:
        query = sql_queries.SELECT_IMAGE_IDS_LINKS_WITH_EXISTING_EMPTY_ALT_ROW

    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result

def change_data(post_id: int, alt_text: str, operation: ChangeDataOperations):
    connection = mysql.connector.connect(**sql_server_params)
    cursor = connection.cursor()

    if operation == ChangeDataOperations.INSERT_ROW_WITH_IMAGE_ALT_DATA:
        cursor.execute(sql_queries.INSERT_IMAGE_ALT_DATA, (post_id, alt_text))
    elif operation == ChangeDataOperations.UPDATE_EXISTING_IMAGE_ALT_DATA:
        cursor.execute(sql_queries.UPDATE_IMAGE_ALT_DATA, (alt_text, post_id))

    connection.commit()

    cursor.close()
    connection.close()

def can_connect_to_database() -> bool:
    connection = mysql.connector.connect(**sql_server_params)
    status = connection.is_connected()
    connection.close()

    return status

#TODO: Fix error rise
def can_login_with_credentials() -> bool:
    if not can_connect_to_database():
        return False

    try:
        connection = mysql.connector.connect(**sql_server_params)
        cursor = connection.cursor()

        query = "SELECT CURRENT_TIMESTAMP;" #test query
        cursor.execute(query, (sql_server_params['user'], sql_server_params['password']))

        result = cursor.fetchone()

        if not result:
            return False

    except Exception:
        return False

    return True
