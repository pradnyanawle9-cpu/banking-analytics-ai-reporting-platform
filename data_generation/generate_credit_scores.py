from db_connection import get_connection
from datetime import date, timedelta
import random


TOTAL_CREDIT_SCORES = 2000


def get_score_category(credit_score):
    if credit_score >= 750:
        return "Excellent"
    elif credit_score >= 700:
        return "Good"
    elif credit_score >= 650:
        return "Fair"
    elif credit_score >= 600:
        return "Poor"
    else:
        return "Very Poor"


def generate_credit_scores():
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

    if not customer_ids:
        print("No customers found. Credit score generation stopped.")
        cursor.close()
        connection.close()
        return

    # Prevent duplicate credit scores for customers
    customer_ids = customer_ids[:TOTAL_CREDIT_SCORES]

    insert_query = """
        INSERT INTO credit_scores
        (
            customer_id,
            credit_score,
            score_date,
            score_category
        )
        VALUES (%s, %s, %s, %s)
    """

    credit_scores = []

    today = date.today()

    for customer_id in customer_ids:

        credit_score = random.randint(300, 850)

        score_category = get_score_category(
            credit_score
        )

        score_date = today - timedelta(
            days=random.randint(1, 365)
        )

        credit_scores.append(
            (
                customer_id,
                credit_score,
                score_date,
                score_category
            )
        )

    try:
        cursor.executemany(
            insert_query,
            credit_scores
        )

        connection.commit()

        print(
            f"{len(credit_scores)} credit scores inserted successfully."
        )

    except Exception as e:
        connection.rollback()
        print("Credit score insertion failed!")
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    generate_credit_scores()