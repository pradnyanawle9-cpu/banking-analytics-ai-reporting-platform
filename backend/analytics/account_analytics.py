from backend.database import get_db_connection


def get_account_summary():
    connection = get_db_connection()

    if connection is None:
        return {
            "status": "failed",
            "message": "Database connection failed"
        }

    try:
        cursor = connection.cursor()

        query = """
            SELECT
                COUNT(*) AS total_accounts,
                COUNT(*) FILTER (WHERE account_status = 'Active') AS active_accounts,
                COUNT(*) FILTER (WHERE account_status = 'Closed') AS closed_accounts,
                COALESCE(SUM(current_balance), 0) AS total_balance,
                COALESCE(AVG(current_balance), 0) AS average_balance
            FROM accounts;
        """

        cursor.execute(query)
        result = cursor.fetchone()

        return {
            "status": "success",
            "data": {
                "total_accounts": result[0],
                "active_accounts": result[1],
                "closed_accounts": result[2],
                "total_balance": float(result[3]),
                "average_balance": float(result[4])
            }
        }

    except Exception as e:
        return {
            "status": "failed",
            "message": str(e)
        }

    finally:
        cursor.close()
        connection.close()