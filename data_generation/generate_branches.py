from faker import Faker
from db_connection import get_connection


fake = Faker("en_IN")

TOTAL_BRANCHES = 25


def generate_branches():
    connection = get_connection()

    if connection is None:
        return

    cursor = connection.cursor()

    insert_query = """
        INSERT INTO branches
        (
            branch_code,
            branch_name,
            city,
            state,
            contact_number,
            branch_status,
            opened_date
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    branches = []

    for i in range(1, TOTAL_BRANCHES + 1):
        branch_code = f"BR{i:03d}"

        branch_name = f"{fake.city()} Branch"

        city = fake.city()
        state = fake.state()

        contact_number = fake.numerify(
            text="+91-9#########"
        )

        branch_status = "Active"

        opened_date = fake.date_between(
            start_date="-15y",
            end_date="today"
        )

        branches.append(
            (
                branch_code,
                branch_name,
                city,
                state,
                contact_number,
                branch_status,
                opened_date
            )
        )

    try:
        cursor.executemany(insert_query, branches)
        connection.commit()

        print(f"{TOTAL_BRANCHES} branches inserted successfully.")

    except Exception as e:
        connection.rollback()
        print("Branch insertion failed!")
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    generate_branches()