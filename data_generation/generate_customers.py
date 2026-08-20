from faker import Faker
from db_connection import get_connection
import random


fake = Faker("en_IN")

TOTAL_CUSTOMERS = 2000


def generate_customers():
    connection = get_connection()

    if connection is None:
        return

    cursor = connection.cursor()

    insert_query = """
        INSERT INTO customers
        (
            customer_code,
            first_name,
            last_name,
            date_of_birth,
            gender,
            email,
            phone,
            occupation,
            annual_income,
            customer_status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    customers = []

    for i in range(1, TOTAL_CUSTOMERS + 1):

        customer_code = f"CUST{i:05d}"

        first_name = fake.first_name()
        last_name = fake.last_name()

        date_of_birth = fake.date_of_birth(
            minimum_age=18,
            maximum_age=70
        )

        gender = random.choice(
            ["Male", "Female", "Other"]
        )

        email = f"{first_name.lower()}.{last_name.lower()}{i}@example.com"

        phone = f"+91{random.randint(7000000000, 9999999999)}"

        occupation = fake.job()

        annual_income = round(
            random.uniform(180000, 2500000),
            2
        )

        customer_status = random.choices(
            ["Active", "Inactive"],
            weights=[90, 10],
            k=1
        )[0]

        customers.append(
            (
                customer_code,
                first_name,
                last_name,
                date_of_birth,
                gender,
                email,
                phone,
                occupation,
                annual_income,
                customer_status
            )
        )

    try:
        cursor.executemany(insert_query, customers)
        connection.commit()

        print(f"{TOTAL_CUSTOMERS} customers inserted successfully.")

    except Exception as e:
        connection.rollback()
        print("Customer insertion failed!")
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    generate_customers()