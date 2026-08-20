from backend.database import get_db_connection


def get_transaction_analytics():
    connection = get_db_connection()

    if connection is None:
        return {
            "status": "failed",
            "message": "Database connection failed"
        }

    cursor = None

    try:
        cursor = connection.cursor()

        # Overall transaction summary
        cursor.execute("""
            SELECT
                COUNT(*) AS total_transactions,

                COUNT(*) FILTER (
                    WHERE transaction_status = 'Completed'
                ) AS completed_transactions,

                COUNT(*) FILTER (
                    WHERE transaction_status <> 'Completed'
                ) AS unsuccessful_transactions,

                COALESCE(SUM(amount), 0) AS total_transaction_amount,

                COALESCE(AVG(amount), 0) AS average_transaction_amount

            FROM transactions
        """)

        summary = cursor.fetchone()

        # Transaction type distribution
        cursor.execute("""
            SELECT
                transaction_type,
                COUNT(*) AS transaction_count
            FROM transactions
            GROUP BY transaction_type
            ORDER BY transaction_count DESC
        """)

        type_rows = cursor.fetchall()

        transaction_types = [
            {
                "transaction_type": row[0],
                "transaction_count": row[1]
            }
            for row in type_rows
        ]

        return {
            "status": "success",
            "data": {
                "total_transactions": summary[0],
                "completed_transactions": summary[1],
                "unsuccessful_transactions": summary[2],
                "total_transaction_amount": float(summary[3]),
                "average_transaction_amount": float(summary[4]),
                "transaction_types": transaction_types
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