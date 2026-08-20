from backend.database import get_db_connection


def get_credit_score_analytics():
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
                COUNT(*) AS total_credit_scores,

                COALESCE(AVG(credit_score), 0) AS average_credit_score,

                MAX(credit_score) AS highest_credit_score,

                MIN(credit_score) AS lowest_credit_score,

                COUNT(*) FILTER (
                    WHERE score_category = 'Excellent'
                ) AS excellent_scores,

                COUNT(*) FILTER (
                    WHERE score_category = 'Good'
                ) AS good_scores,

                COUNT(*) FILTER (
                    WHERE score_category = 'Fair'
                ) AS fair_scores,

                COUNT(*) FILTER (
                    WHERE score_category = 'Poor'
                ) AS poor_scores,

                COUNT(DISTINCT customer_id) AS customers_with_credit_score

            FROM credit_scores
        """

        cursor.execute(query)

        row = cursor.fetchone()

        return {
            "status": "success",
            "data": {
                "total_credit_scores": row[0],
                "average_credit_score": float(row[1]),
                "highest_credit_score": row[2],
                "lowest_credit_score": row[3],
                "excellent_scores": row[4],
                "good_scores": row[5],
                "fair_scores": row[6],
                "poor_scores": row[7],
                "customers_with_credit_score": row[8]
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