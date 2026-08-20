from faker import Faker
from db_connection import get_connection
import random


fake = Faker("en_IN")

TOTAL_EMPLOYEES = 200


def generate_employees():
    connection = get_connection()

    if connection is None:
        return

    cursor = connection.cursor()

    # Get existing branch IDs
    cursor.execute("""
        SELECT branch_id
        FROM branches
        ORDER BY branch_id;
    """)

    branch_ids = [row[0] for row in cursor.fetchall()]

    if not branch_ids:
        print("No branches found. Employee generation stopped.")
        cursor.close()
        connection.close()
        return

    insert_query = """
        INSERT INTO employees
        (
            employee_code,
            first_name,
            last_name,
            designation,
            department,
            branch_id,
            joining_date,
            salary,
            employee_status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    employees = []

    designations = [
        "Branch Manager",
        "Assistant Branch Manager",
        "Bank Officer",
        "Senior Bank Officer",
        "Relationship Manager",
        "Customer Service Executive",
        "Loan Officer",
        "Credit Analyst",
        "Cashier",
        "Operations Executive"
    ]

    departments = [
        "Operations",
        "Retail Banking",
        "Loans",
        "Credit",
        "Customer Service",
        "Finance",
        "Human Resources",
        "IT"
    ]

    statuses = ["Active", "Inactive"]

    for i in range(1, TOTAL_EMPLOYEES + 1):

        employee_code = f"EMP{i:04d}"

        first_name = fake.first_name()
        last_name = fake.last_name()

        designation = random.choice(designations)
        department = random.choice(departments)

        # Always use an existing branch_id
        branch_id = random.choice(branch_ids)

        joining_date = fake.date_between(
            start_date="-12y",
            end_date="today"
        )

        salary = round(
            random.uniform(25000, 150000),
            2
        )

        employee_status = random.choices(
            statuses,
            weights=[90, 10],
            k=1
        )[0]

        employees.append(
            (
                employee_code,
                first_name,
                last_name,
                designation,
                department,
                branch_id,
                joining_date,
                salary,
                employee_status
            )
        )

    try:
        cursor.executemany(insert_query, employees)
        connection.commit()

        print(f"{TOTAL_EMPLOYEES} employees inserted successfully.")

    except Exception as e:
        connection.rollback()
        print("Employee insertion failed!")
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    generate_employees()