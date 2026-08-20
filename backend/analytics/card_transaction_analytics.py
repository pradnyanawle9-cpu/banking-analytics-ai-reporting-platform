from backend.database import get_db_connection


def get_card_transaction_analytics():
    connection = get_db_connection()

    if connection is None:
        return {
            "status": "failed",
            "message": "Database connection failed"
        }

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
            SELECT
                COUNT(*) AS total_card_transactions,

                COUNT(*) FILTER (
                    WHERE transaction_status = 'Completed'
                ) AS completed_transactions,

                COUNT(*) FILTER (
                    WHERE transaction_status <> 'Completed'
                ) AS unsuccessful_transactions,

                COALESCE(SUM(amount), 0) AS total_transaction_amount,

                COALESCE(AVG(amount), 0) AS average_transaction_amount,

                COUNT(DISTINCT merchant_name) AS total_merchants,

                COUNT(DISTINCT transaction_type) AS total_transaction_types

            FROM card_transactions
        """

        cursor.execute(query)

        row = cursor.fetchone()

        return {
            "status": "success",
            "data": {
                "total_card_transactions": row[0],
                "completed_transactions": row[1],
                "unsuccessful_transactions": row[2],
                "total_transaction_amount": float(row[3]),
                "average_transaction_amount": float(row[4]),
                "total_merchants": row[5],
                "total_transaction_types": row[6]
            }
        }

    except Exception as e:
        return {
            "status": "failed",
            "message": str(e)
        }

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()