from db_connection import get_connection
from datetime import date, timedelta
import random


TOTAL_COMPLAINTS = 1000


def generate_complaints():
    connection = get_connection()

    if connection is None:
        return

    cursor = connection.cursor()

    cursor.execute("""
        SELECT customer_id
        FROM customers
        ORDER BY customer_id;
    """)

    customer_ids = [row[0] for row in cursor.fetchall()]

    if not customer_ids:
        print("No customers found. Complaint generation stopped.")
        cursor.close()
        connection.close()
        return

    insert_query = """
        INSERT INTO complaints
        (
            complaint_code,
            customer_id,
            complaint_type,
            complaint_date,
            complaint_status,
            priority,
            resolution_date,
            resolution_description
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    complaints = []

    complaint_types = [
        "Transaction Issue",
        "Account Issue",
        "Card Issue",
        "Loan Issue",
        "Fund Transfer Issue",
        "ATM Issue",
        "Online Banking Issue",
        "Service Issue"
    ]

    priorities = [
        "Low",
        "Medium",
        "High",
        "Critical"
    ]

    statuses = [
        "Open",
        "In Progress",
        "Resolved",
        "Closed"
    ]

    resolution_descriptions = [
        "Issue resolved successfully.",
        "Customer request completed.",
        "Transaction issue resolved.",
        "Account issue corrected.",
        "Card issue resolved.",
        "Customer was contacted and issue resolved."
    ]

    today = date.today()

    for i in range(1, TOTAL_COMPLAINTS + 1):

        complaint_code = f"CMP{i:06d}"

        customer_id = random.choice(customer_ids)

        complaint_type = random.choice(complaint_types)

        complaint_date = today - timedelta(
            days=random.randint(1, 730)
        )

        complaint_status = random.choices(
            statuses,
            weights=[15, 15, 50, 20],
            k=1
        )[0]

        priority = random.choices(
            priorities,
            weights=[30, 45, 20, 5],
            k=1
        )[0]

        resolution_date = None
        resolution_description = None

        if complaint_status in ["Resolved", "Closed"]:

            resolution_date = complaint_date + timedelta(
                days=random.randint(1, 30)
            )

            if resolution_date > today:
                resolution_date = today

            resolution_description = random.choice(
                resolution_descriptions
            )

        complaints.append(
            (
                complaint_code,
                customer_id,
                complaint_type,
                complaint_date,
                complaint_status,
                priority,
                resolution_date,
                resolution_description
            )
        )

    try:
        cursor.executemany(insert_query, complaints)
        connection.commit()

        print(
            f"{TOTAL_COMPLAINTS} complaints inserted successfully."
        )

    except Exception as e:
        connection.rollback()
        print("Complaint insertion failed!")
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    generate_complaints()