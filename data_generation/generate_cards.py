from db_connection import get_connection
from datetime import date, timedelta
from decimal import Decimal
import random


TOTAL_CARDS = 1500


def generate_cards():
    connection = get_connection()

    if connection is None:
        return

    cursor = connection.cursor()

    # Get existing customers
    cursor.execute("""
        SELECT customer_id
        FROM customers
        ORDER BY customer_id;
    """)

    customer_ids = [row[0] for row in cursor.fetchall()]

    if not customer_ids:
        print("No customers found. Card generation stopped.")
        cursor.close()
        connection.close()
        return

    insert_query = """
        INSERT INTO cards
        (
            card_number,
            customer_id,
            card_type,
            card_status,
            issue_date,
            expiry_date,
            credit_limit,
            available_limit
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    cards = []

    card_types = [
        "Debit",
        "Credit"
    ]

    card_statuses = [
        "Active",
        "Blocked",
        "Expired"
    ]

    today = date.today()

    for i in range(1, TOTAL_CARDS + 1):

        # Unique 16-digit card number
        card_number = f"{4000000000000000 + i}"

        customer_id = random.choice(customer_ids)

        card_type = random.choice(card_types)

        issue_date = today - timedelta(
            days=random.randint(30, 1460)
        )

        # 3-year validity
        expiry_date = issue_date + timedelta(days=1095)

        if expiry_date < today:
            card_status = "Expired"
        else:
            card_status = random.choices(
                ["Active", "Blocked"],
                weights=[95, 5],
                k=1
            )[0]

        if card_type == "Credit":
            credit_limit = Decimal(
                str(
                    random.choice(
                        [
                            25000,
                            50000,
                            75000,
                            100000,
                            150000,
                            250000,
                            500000
                        ]
                    )
                )
            )

            available_limit = Decimal(
                str(
                    round(
                        random.uniform(
                            0,
                            float(credit_limit)
                        ),
                        2
                    )
                )
            )

        else:
            credit_limit = None
            available_limit = None

        cards.append(
            (
                card_number,
                customer_id,
                card_type,
                card_status,
                issue_date,
                expiry_date,
                credit_limit,
                available_limit
            )
        )

    try:
        cursor.executemany(insert_query, cards)
        connection.commit()

        print(f"{TOTAL_CARDS} cards inserted successfully.")

    except Exception as e:
        connection.rollback()
        print("Card insertion failed!")
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    generate_cards()