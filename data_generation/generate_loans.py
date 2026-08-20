from db_connection import get_connection
from datetime import date, timedelta
from decimal import Decimal
import random


TOTAL_LOANS = 800


def generate_loans():
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
        print("No customers found. Loan generation stopped.")
        cursor.close()
        connection.close()
        return

    insert_query = """
        INSERT INTO loans
        (
            loan_number,
            customer_id,
            loan_type,
            loan_amount,
            interest_rate,
            tenure_months,
            loan_status,
            application_date,
            approval_date,
            disbursement_date,
            outstanding_amount
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    loans = []

    loan_types = [
        "Personal",
        "Home",
        "Vehicle",
        "Education",
        "Business"
    ]

    loan_statuses = [
        "Active",
        "Closed",
        "Pending",
        "Rejected"
    ]

    today = date.today()

    for i in range(1, TOTAL_LOANS + 1):

        loan_number = f"LN{i:06d}"

        customer_id = random.choice(customer_ids)

        loan_type = random.choice(loan_types)

        loan_amount = Decimal(
            str(round(random.uniform(100000, 5000000), 2))
        )

        interest_rate = Decimal(
            str(round(random.uniform(7.0, 16.0), 2))
        )

        tenure_months = random.choice(
            [12, 24, 36, 48, 60, 84, 120, 180]
        )

        loan_status = random.choices(
            loan_statuses,
            weights=[65, 15, 10, 10],
            k=1
        )[0]

        application_date = today - timedelta(
            days=random.randint(30, 1825)
        )

        # Default nullable dates
        approval_date = None
        disbursement_date = None

        if loan_status in ["Active", "Closed"]:

            approval_date = application_date + timedelta(
                days=random.randint(3, 30)
            )

            disbursement_date = approval_date + timedelta(
                days=random.randint(1, 15)
            )

            if loan_status == "Closed":
                outstanding_amount = Decimal("0.00")
            else:
                outstanding_amount = Decimal(
                    str(
                        round(
                            random.uniform(
                                float(loan_amount * Decimal("0.10")),
                                float(loan_amount * Decimal("0.90"))
                            ),
                            2
                        )
                    )
                )

        elif loan_status == "Pending":

            outstanding_amount = Decimal("0.00")

        else:  # Rejected

            outstanding_amount = Decimal("0.00")

        loans.append(
            (
                loan_number,
                customer_id,
                loan_type,
                loan_amount,
                interest_rate,
                tenure_months,
                loan_status,
                application_date,
                approval_date,
                disbursement_date,
                outstanding_amount
            )
        )

    try:
        cursor.executemany(insert_query, loans)
        connection.commit()

        print(f"{TOTAL_LOANS} loans inserted successfully.")

    except Exception as e:
        connection.rollback()
        print("Loan insertion failed!")
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    generate_loans()