from backend.database import get_db_connection


def get_branch_transaction_analytics():
    connection = get_db_connection()

    if connection is None:
        return {
            "status": "failed",
            "message": "Database connection failed"
        }

    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                b.branch_id,
                b.branch_name,
                COUNT(t.transaction_id) AS transaction_count,
                COALESCE(SUM(t.amount), 0) AS total_transaction_amount,
                COALESCE(AVG(t.amount), 0) AS average_transaction_amount
            FROM branches b
            JOIN accounts a
                ON b.branch_id = a.branch_id
            JOIN transactions t
                ON a.account_id = t.account_id
            GROUP BY
                b.branch_id,
                b.branch_name
            ORDER BY transaction_count DESC
        """)

        rows = cursor.fetchall()

        branches = [
            {
                "branch_id": row[0],
                "branch_name": row[1],
                "transaction_count": row[2],
                "total_transaction_amount": float(row[3]),
                "average_transaction_amount": float(row[4])
            }
            for row in rows
        ]

        return {
            "status": "success",
            "data": branches
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