from db_connection import get_connection
import random


TOTAL_BENEFICIARIES = 2000


def generate_beneficiaries():
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
        print("No customers found. Beneficiary generation stopped.")
        cursor.close()
        connection.close()
        return

    insert_query = """
        INSERT INTO beneficiaries
        (
            beneficiary_code,
            customer_id,
            beneficiary_name,
            account_number,
            bank_name,
            ifsc_code,
            beneficiary_type,
            beneficiary_status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    beneficiaries = []

    first_names = [
        "Amit", "Rahul", "Priya", "Sneha", "Rohit",
        "Neha", "Pooja", "Akshay", "Kiran", "Anjali"
    ]

    last_names = [
        "Sharma", "Patil", "Deshmukh", "Kulkarni",
        "Joshi", "Pawar", "Jadhav", "More", "Shinde"
    ]

    bank_names = [
        "State Bank of India",
        "HDFC Bank",
        "ICICI Bank",
        "Axis Bank",
        "Kotak Mahindra Bank",
        "Bank of Baroda",
        "Punjab National Bank",
        "Canara Bank",
        "IndusInd Bank",
        "IDFC First Bank"
    ]

    beneficiary_types = [
        "Individual",
        "Business",
        "Family",
        "Merchant"
    ]

    statuses = [
        "Active",
        "Inactive"
    ]

    bank_codes = [
        "SBIN",
        "HDFC",
        "ICIC",
        "UTIB",
        "KKBK",
        "BARB",
        "PUNB",
        "CNRB",
        "INDB",
        "IDFB"
    ]

    for i in range(1, TOTAL_BENEFICIARIES + 1):

        beneficiary_code = f"BEN{i:06d}"

        customer_id = random.choice(customer_ids)

        first_name = random.choice(first_names)
        last_name = random.choice(last_names)

        beneficiary_name = f"{first_name} {last_name}"

        account_number = str(
            random.randint(100000000000, 999999999999)
        )

        bank_name = random.choice(bank_names)

        bank_code = random.choice(bank_codes)

        ifsc_code = f"{bank_code}0{random.randint(100000, 999999)}"

        beneficiary_type = random.choice(beneficiary_types)

        beneficiary_status = random.choices(
            statuses,
            weights=[90, 10],
            k=1
        )[0]

        beneficiaries.append(
            (
                beneficiary_code,
                customer_id,
                beneficiary_name,
                account_number,
                bank_name,
                ifsc_code,
                beneficiary_type,
                beneficiary_status
            )
        )

    try:
        cursor.executemany(insert_query, beneficiaries)
        connection.commit()

        print(
            f"{TOTAL_BENEFICIARIES} beneficiaries inserted successfully."
        )

    except Exception as e:
        connection.rollback()
        print("Beneficiary insertion failed!")
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    generate_beneficiaries()