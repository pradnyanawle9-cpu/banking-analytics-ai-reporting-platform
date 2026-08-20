from backend.database import get_db_connection


def get_fund_transfer_analytics():
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
                COUNT(*) AS total_transfers,

                COUNT(*) FILTER (
                    WHERE transfer_status = 'Completed'
                ) AS completed_transfers,

                COUNT(*) FILTER (
                    WHERE transfer_status <> 'Completed'
                ) AS unsuccessful_transfers,

                COALESCE(SUM(amount), 0) AS total_transfer_amount,

                COALESCE(AVG(amount), 0) AS average_transfer_amount,

                COUNT(DISTINCT transfer_type) AS total_transfer_types

            FROM fund_transfers
        """

        cursor.execute(query)

        row = cursor.fetchone()

        return {
            "status": "success",
            "data": {
                "total_transfers": row[0],
                "completed_transfers": row[1],
                "unsuccessful_transfers": row[2],
                "total_transfer_amount": float(row[3]),
                "average_transfer_amount": float(row[4]),
                "total_transfer_types": row[5]
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