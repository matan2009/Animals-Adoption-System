import mysql.connector


class DatabaseHelper:

    def __init__(self, configurations, create_table_query):
        self.configurations = configurations
        self.create_table_query = create_table_query

    @staticmethod
    def create_connection_to_db():
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Nnn010203!",
            database="animals_adoption_schema"
        )
        cursor = conn.cursor()
        return conn, cursor

    def verify_db(self):
        conn, cursor = self.create_connection_to_db()
        # Check if the table exists
        query = "SHOW TABLES LIKE '{}'".format(self.configurations.table_name)
        cursor.execute(query)
        if not cursor.fetchone():
            # create new table
            cursor.execute(self.create_table_query)
            conn.commit()
        cursor.close()
        conn.close()

    def insert_to_db(self, row_info):
        conn, cursor = self.create_connection_to_db()
        keys = ', '.join(row_info.keys())
        values = ', '.join(['%s'] * len(row_info))
        query = f"INSERT INTO {self.configurations.table_name} ({keys}) VALUES ({values})"
        cursor.execute(query, tuple(row_info.values()))
        conn.commit()
        cursor.close()
        conn.close()
