from db_connection import get_connection
from datetime import date, timedelta
from decimal import Decimal
import random


TOTAL_PAYMENTS = 4000


def generate_loan_payments():
    connection = get_connection()

    if connection is None:
        return

    cursor = connection.cursor()

    # Get existing loans
    cursor.execute("""
        SELECT loan_id, application_date, loan_amount
        FROM loans
        ORDER BY loan_id;
    """)

    loans = cursor.fetchall()

    if not loans:
        print("No loans found. Loan payment generation stopped.")
        cursor.close()
        connection.close()
        return

    insert_query = """
        INSERT INTO loan_payments
        (
            payment_code,
            loan_id,
            payment_date,
            payment_amount,
            principal_amount,
            interest_amount,
            payment_status,
            payment_method
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    payments = []

    payment_statuses = [
        "Completed",
        "Pending",
        "Failed"
    ]

    payment_methods = [
        "Bank Transfer",
        "UPI",
        "Debit Card",
        "Cash",
        "Cheque"
    ]

    today = date.today()

    for i in range(1, TOTAL_PAYMENTS + 1):

        payment_code = f"PAY{i:06d}"

        loan_id, application_date, loan_amount = random.choice(loans)

        # ---------------------------------------------------------
        # PAYMENT DATE
        # Never generate a future payment date.
        # ---------------------------------------------------------

        max_days_after_application = (
            today - application_date
        ).days

        if max_days_after_application <= 0:
            payment_date = application_date
        elif max_days_after_application < 30:
            payment_date = application_date + timedelta(
                days=random.randint(
                    0,
                    max_days_after_application
                )
            )
        else:
            days_after_application = random.randint(
                30,
                min(1800, max_days_after_application)
            )

            payment_date = (
                application_date
                + timedelta(days=days_after_application)
            )

        # ---------------------------------------------------------
        # PAYMENT AMOUNT
        # ---------------------------------------------------------

        payment_amount = Decimal(
            str(round(random.uniform(1000, 100000), 2))
        )

        # Principal + Interest = Payment Amount
        interest_ratio = random.uniform(0.05, 0.25)

        interest_amount = Decimal(
            str(
                round(
                    float(payment_amount) * interest_ratio,
                    2
                )
            )
        )

        principal_amount = (
            payment_amount - interest_amount
        ).quantize(Decimal("0.01"))

        # ---------------------------------------------------------
        # PAYMENT STATUS
        # ---------------------------------------------------------

        payment_status = random.choices(
            payment_statuses,
            weights=[90, 7, 3],
            k=1
        )[0]

        # ---------------------------------------------------------
        # PAYMENT METHOD
        # ---------------------------------------------------------

        payment_method = random.choice(
            payment_methods
        )

        payments.append(
            (
                payment_code,
                loan_id,
                payment_date,
                payment_amount,
                principal_amount,
                interest_amount,
                payment_status,
                payment_method
            )
        )

    # -------------------------------------------------------------
    # INSERT PAYMENTS
    # -------------------------------------------------------------

    try:
        cursor.executemany(
            insert_query,
            payments
        )

        connection.commit()

        print(
            f"{TOTAL_PAYMENTS} loan payments inserted successfully."
        )

    except Exception as e:
        connection.rollback()

        print(
            "Loan payment insertion failed!"
        )

        print(
            "Error:",
            e
        )

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    generate_loan_payments()