import psycopg2


def get_db_connection():
    try:
        connection = psycopg2.connect(
            host="localhost",
            port="5432",
            database="banking_analytics_db",
            user="postgres",
            password="114"
        )

        print("PostgreSQL connection successful!")
        return connection

    except Exception as e:
        print("PostgreSQL connection failed!")
        print("Error:", e)
        return None