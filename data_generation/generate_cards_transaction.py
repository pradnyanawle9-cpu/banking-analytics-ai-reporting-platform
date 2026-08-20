from db_connection import get_connection
from datetime import datetime, timedelta
from decimal import Decimal
import random


TOTAL_CARD_TRANSACTIONS = 6000


def generate_card_transactions():
    connection = get_connection()

    if connection is None:
        return

    cursor = connection.cursor()

    cursor.execute("""
        SELECT card_id
        FROM cards
        ORDER BY card_id;
    """)

    card_ids = [row[0] for row in cursor.fetchall()]

    if not card_ids:
        print("No cards found. Card transaction generation stopped.")
        cursor.close()
        connection.close()
        return

    insert_query = """
        INSERT INTO card_transactions
        (
            transaction_code,
            card_id,
            transaction_date,
            transaction_type,
            amount,
            merchant_name,
            transaction_status,
            description
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    transactions = []

    transaction_types = [
        "Purchase",
        "Online Payment",
        "ATM Withdrawal",
        "POS Payment",
        "Cash Withdrawal"
    ]

    statuses = [
        "Completed",
        "Pending",
        "Failed"
    ]

    merchants = [
        "Amazon",
        "Flipkart",
        "Reliance Retail",
        "DMart",
        "Swiggy",
        "Zomato",
        "Myntra",
        "Uber",
        "IRCTC",
        "BookMyShow",
        "BigBasket",
        "Airtel"
    ]

    start_date = datetime.now() - timedelta(days=730)
    end_date = datetime.now()

    for i in range(1, TOTAL_CARD_TRANSACTIONS + 1):

        transaction_code = f"CTXN{i:06d}"

        card_id = random.choice(card_ids)

        transaction_date = start_date + (
            end_date - start_date
        ) * random.random()

        transaction_type = random.choice(transaction_types)

        amount = Decimal(
            str(round(random.uniform(100, 100000), 2))
        )

        merchant_name = random.choice(merchants)

        transaction_status = random.choices(
            statuses,
            weights=[92, 5, 3],
            k=1
        )[0]

        description = f"{transaction_type} transaction"

        transactions.append(
            (
                transaction_code,
                card_id,
                transaction_date,
                transaction_type,
                amount,
                merchant_name,
                transaction_status,
                description
            )
        )

    try:
        cursor.executemany(insert_query, transactions)
        connection.commit()

        print(
            f"{TOTAL_CARD_TRANSACTIONS} card transactions inserted successfully."
        )

    except Exception as e:
        connection.rollback()
        print("Card transaction insertion failed!")
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    generate_card_transactions()