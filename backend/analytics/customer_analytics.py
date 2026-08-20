from backend.database import get_db_connection


def get_customer_analytics():
    connection = get_db_connection()

    if connection is None:
        return {
            "status": "failed",
            "message": "Database connection failed"
        }

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COUNT(*) AS total_customers,

            COUNT(*) FILTER (
                WHERE customer_status = 'Active'
            ) AS active_customers,

            COUNT(*) FILTER (
                WHERE customer_status <> 'Active'
            ) AS inactive_customers,

            COUNT(*) FILTER (
                WHERE gender = 'Male'
            ) AS male_customers,

            COUNT(*) FILTER (
                WHERE gender = 'Female'
            ) AS female_customers,

            COUNT(*) FILTER (
                WHERE gender = 'Other'
            ) AS other_customers,

            ROUND(AVG(annual_income), 2) AS average_annual_income,

            COUNT(DISTINCT occupation) AS total_occupations

        FROM customers
    """)

    row = cursor.fetchone()

    cursor.close()
    connection.close()

    return {
        "status": "success",
        "data": {
            "total_customers": row[0],
            "active_customers": row[1],
            "inactive_customers": row[2],
            "male_customers": row[3],
            "female_customers": row[4],
            "other_customers": row[5],
            "average_annual_income": float(row[6]) if row[6] is not None else 0,
            "total_occupations": row[7]
        }
    }