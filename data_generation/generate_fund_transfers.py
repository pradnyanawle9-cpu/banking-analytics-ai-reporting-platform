from db_connection import get_connection
from datetime import datetime, timedelta
from decimal import Decimal
import random


TOTAL_TRANSFERS = 8000


def generate_fund_transfers():
    connection = get_connection()

    if connection is None:
        return

    cursor = connection.cursor()

    # Get beneficiary and its customer
    cursor.execute("""
        SELECT beneficiary_id, customer_id
        FROM beneficiaries
        ORDER BY beneficiary_id;
    """)

    beneficiaries = cursor.fetchall()

    if not beneficiaries:
        print("No beneficiaries found. Fund transfer generation stopped.")
        cursor.close()
        connection.close()
        return

    insert_query = """
        INSERT INTO fund_transfers
        (
            transfer_code,
            customer_id,
            beneficiary_id,
            transfer_type,
            transfer_date,
            amount,
            transfer_status,
            remarks
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    transfers = []

    transfer_types = [
        "NEFT",
        "RTGS",
        "IMPS",
        "UPI"
    ]

    transfer_statuses = [
        "Completed",
        "Pending",
        "Failed"
    ]

    start_date = datetime.now() - timedelta(days=730)
    end_date = datetime.now()

    for i in range(1, TOTAL_TRANSFERS + 1):

        transfer_code = f"FT{i:06d}"

        beneficiary_id, customer_id = random.choice(beneficiaries)

        transfer_type = random.choice(transfer_types)

        transfer_date = start_date + (
            end_date - start_date
        ) * random.random()

        amount = Decimal(
            str(round(random.uniform(500, 500000), 2))
        )

        transfer_status = random.choices(
            transfer_statuses,
            weights=[92, 5, 3],
            k=1
        )[0]

        remarks = f"{transfer_type} fund transfer"

        transfers.append(
            (
                transfer_code,
                customer_id,
                beneficiary_id,
                transfer_type,
                transfer_date,
                amount,
                transfer_status,
                remarks
            )
        )

    try:
        cursor.executemany(insert_query, transfers)
        connection.commit()

        print(
            f"{TOTAL_TRANSFERS} fund transfers inserted successfully."
        )

    except Exception as e:
        connection.rollback()
        print("Fund transfer insertion failed!")
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    generate_fund_transfers()