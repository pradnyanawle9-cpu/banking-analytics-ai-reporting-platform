from db_connection import get_connection
from datetime import datetime, timedelta
from decimal import Decimal
import random


TOTAL_TRANSACTIONS = 15000


def generate_transactions():
    connection = get_connection()

    if connection is None:
        return

    cursor = connection.cursor()

    # Get existing account IDs
    cursor.execute("""
        SELECT account_id
        FROM accounts
        ORDER BY account_id;
    """)

    account_ids = [row[0] for row in cursor.fetchall()]

    if not account_ids:
        print("No accounts found. Transaction generation stopped.")
        cursor.close()
        connection.close()
        return

    insert_query = """
        INSERT INTO transactions
        (
            transaction_code,
            account_id,
            transaction_type,
            transaction_date,
            amount,
            transaction_status,
            description
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    transactions = []

    transaction_types = [
        "Deposit",
        "Withdrawal",
        "Transfer",
        "Payment",
        "ATM Withdrawal",
        "Online Payment"
    ]

    transaction_statuses = [
        "Completed",
        "Pending",
        "Failed"
    ]

    descriptions = {
        "Deposit": "Cash deposit",
        "Withdrawal": "Cash withdrawal",
        "Transfer": "Account transfer",
        "Payment": "Bill or merchant payment",
        "ATM Withdrawal": "ATM cash withdrawal",
        "Online Payment": "Online merchant payment"
    }

    start_date = datetime.now() - timedelta(days=730)
    end_date = datetime.now()

    for i in range(1, TOTAL_TRANSACTIONS + 1):

        transaction_code = f"TXN{i:06d}"

        account_id = random.choice(account_ids)

        transaction_type = random.choice(transaction_types)

        transaction_date = start_date + (
            end_date - start_date
        ) * random.random()

        amount = Decimal(
            str(round(random.uniform(100, 250000), 2))
        )

        transaction_status = random.choices(
            transaction_statuses,
            weights=[92, 5, 3],
            k=1
        )[0]

        description = descriptions[transaction_type]

        transactions.append(
            (
                transaction_code,
                account_id,
                transaction_type,
                transaction_date,
                amount,
                transaction_status,
                description
            )
        )

    try:
        cursor.executemany(insert_query, transactions)
        connection.commit()

        print(
            f"{TOTAL_TRANSACTIONS} transactions inserted successfully."
        )

    except Exception as e:
        connection.rollback()
        print("Transaction insertion failed!")
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    generate_transactions()