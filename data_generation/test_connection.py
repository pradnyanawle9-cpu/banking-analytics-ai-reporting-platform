from db_connection import get_connection


connection = get_connection()

if connection:
    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)

        tables = cursor.fetchall()

        print("\n--- BANKING DATABASE TABLES ---")

        for table in tables:
            print(table[0])

       

        print("\n--- TABLE STRUCTURES ---")

        for table in tables:
            table_name = table[0]

            cursor.execute("""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_schema = 'public'
                AND table_name = %s
                ORDER BY ordinal_position;
            """, (table_name,))

            columns = cursor.fetchall()

            print(f"\n[{table_name}]")

            for column in columns:
                print(f"  {column[0]} : {column[1]}")



        cursor.close()

    finally:
        connection.close()