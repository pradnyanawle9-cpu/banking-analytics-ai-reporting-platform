import psycopg2
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


def get_connection():
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )

        print("PostgreSQL connection successful!")
        return connection

    except psycopg2.Error as e:
        print("PostgreSQL connection failed!")
        print("Error:", e)
        return None