from db_connection import get_connection
from datetime import date, timedelta
from decimal import Decimal
import random


TOTAL_ACCOUNTS = 3000


def generate_accounts():
    connection = get_connection()

    if connection is None:
        return

    cursor = connection.cursor()

    # Get existing customer IDs
    cursor.execute("""
        SELECT customer_id
        FROM customers
        ORDER BY customer_id;
    """)

    customer_ids = [row[0] for row in cursor.fetchall()]

    # Get existing branch IDs
    cursor.execute("""
        SELECT branch_id
        FROM branches
        ORDER BY branch_id;
    """)

    branch_ids = [row[0] for row in cursor.fetchall()]

    if not customer_ids:
        print("No customers found. Account generation stopped.")
        cursor.close()
        connection.close()
        return

    if not branch_ids:
        print("No branches found. Account generation stopped.")
        cursor.close()
        connection.close()
        return

    insert_query = """
        INSERT INTO accounts
        (
            account_number,
            customer_id,
            branch_id,
            account_type,
            account_status,
            opening_date,
            closing_date,
            current_balance
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    accounts = []

    account_types = [
        "Savings",
        "Current",
        "Salary",
        "Business"
    ]

    for i in range(1, TOTAL_ACCOUNTS + 1):

        # Unique 12-digit account number
        account_number = f"{100000000000 + i}"

        customer_id = random.choice(customer_ids)
        branch_id = random.choice(branch_ids)

        account_type = random.choice(account_types)

        # Most accounts are active
        account_status = random.choices(
            ["Active", "Closed"],
            weights=[95, 5],
            k=1
        )[0]

        opening_date = date.today() - timedelta(
            days=random.randint(30, 3650)
        )

        if account_status == "Closed":
            closing_date = opening_date + timedelta(
                days=random.randint(30, 1500)
            )

            # Never allow closing date in the future
            if closing_date > date.today():
                closing_date = date.today()

            current_balance = Decimal("0.00")

        else:
            closing_date = None

            current_balance = Decimal(
                str(round(random.uniform(500, 500000), 2))
            )

        accounts.append(
            (
                account_number,
                customer_id,
                branch_id,
                account_type,
                account_status,
                opening_date,
                closing_date,
                current_balance
            )
        )

    try:
        cursor.executemany(insert_query, accounts)
        connection.commit()

        print(f"{TOTAL_ACCOUNTS} accounts inserted successfully.")

    except Exception as e:
        connection.rollback()
        print("Account insertion failed!")
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    generate_accounts()