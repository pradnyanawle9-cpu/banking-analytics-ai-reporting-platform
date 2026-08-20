from backend.database import get_db_connection


def get_complaint_analytics():
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
                COUNT(*) AS total_complaints,

                COUNT(*) FILTER (
                    WHERE complaint_status = 'Open'
                ) AS open_complaints,

                COUNT(*) FILTER (
                    WHERE complaint_status = 'Resolved'
                ) AS resolved_complaints,

                COUNT(*) FILTER (
                    WHERE priority = 'High'
                ) AS high_priority_complaints,

                COUNT(*) FILTER (
                    WHERE priority = 'Medium'
                ) AS medium_priority_complaints,

                COUNT(*) FILTER (
                    WHERE priority = 'Low'
                ) AS low_priority_complaints,

                COUNT(DISTINCT complaint_type) AS total_complaint_types

            FROM complaints
        """

        cursor.execute(query)

        row = cursor.fetchone()

        return {
            "status": "success",
            "data": {
                "total_complaints": row[0],
                "open_complaints": row[1],
                "resolved_complaints": row[2],
                "high_priority_complaints": row[3],
                "medium_priority_complaints": row[4],
                "low_priority_complaints": row[5],
                "total_complaint_types": row[6]
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