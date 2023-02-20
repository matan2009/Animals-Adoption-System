import mysql.connector
import hashlib
import json
import secrets

from common.database_helper import DatabaseHelper
from configurations.animals_adoption_system_configurations import AnimalsAdoptionSystemConfiguration
from configurations.connection_system_helper_configurations import ConnectionSystemHelperConfigurations
from excpetions.connection_system_helper_excpetion import ConnectionSystemHelperException


class ConnectionSystemHelper(AnimalsAdoptionSystemConfiguration):

    def __init__(self):
        super().__init__()
        helper_config = self.config["connection_system_helper"]
        self.configurations = ConnectionSystemHelperConfigurations(helper_config["table_name"])
        create_users_table_query = """CREATE TABLE users (
            username VARCHAR(255) NOT NULL PRIMARY KEY,
            password VARCHAR(255) NOT NULL,
            token VARCHAR(255))"""
        self.database_helper = DatabaseHelper(self.configurations, create_users_table_query)

    def insert_user_info_to_db(self, conn, cursor, username, password, token):
        query = 'INSERT INTO {} (username, password, token) VALUES (%s, %s, %s)'.format(self.configurations.table_name)
        values = (username, password, token)
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()

    def create_new_user_in_db(self, username, password):
        conn, cursor = self.database_helper.create_connection_to_db()
        random_bytes = secrets.token_bytes(16)
        token = hashlib.sha256(random_bytes).hexdigest()
        self.insert_user_info_to_db(conn, cursor, username, password, token)

    def verify_user(self, provided_username, provided_password):
        conn, cursor = self.database_helper.create_connection_to_db()
        query = 'SELECT * FROM {} WHERE username = %s'.format(self.configurations.table_name)
        cursor.execute(query, (provided_username,))
        user_record = cursor.fetchone()
        if not user_record:
            raise ConnectionSystemHelperException(("Unauthorized. username is not registered", 401))

        user_password = user_record[1]
        if provided_password != user_password:
            raise ConnectionSystemHelperException(("Unauthorized. password is incorrect", 401))

        token = user_record[2]
        return token

    def verify_token(self, provided_token):
        conn, cursor = self.database_helper.create_connection_to_db()
        query = 'SELECT * FROM {} WHERE token = %s'.format(self.configurations.table_name)
        cursor.execute(query, (provided_token,))
        user_record = cursor.fetchone()
        if not user_record:
            raise ConnectionSystemHelperException(("Unauthorized. token is incorrect", 401))