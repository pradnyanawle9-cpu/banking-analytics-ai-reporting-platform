from backend.database import get_db_connection


def get_loan_payment_analytics():
    connection = get_db_connection()

    if connection is None:
        return {
            "status": "failed",
            "message": "Database connection failed"
        }

    cursor = None

    try:
        cursor = connection.cursor()

        # Overall loan payment summary
        summary_query = """
            SELECT
                COUNT(*) AS total_payments,

                COUNT(*) FILTER (
                    WHERE payment_status = 'Completed'
                ) AS completed_payments,

                COUNT(*) FILTER (
                    WHERE payment_status <> 'Completed'
                ) AS unsuccessful_payments,

                COALESCE(SUM(payment_amount), 0) AS total_payment_amount,

                COALESCE(SUM(principal_amount), 0) AS total_principal_paid,

                COALESCE(SUM(interest_amount), 0) AS total_interest_paid,

                COALESCE(AVG(payment_amount), 0) AS average_payment_amount,

                COUNT(DISTINCT payment_method) AS total_payment_methods

            FROM loan_payments
        """

        cursor.execute(summary_query)
        row = cursor.fetchone()

        # Monthly loan payment trend
        payment_trend_query = """
            SELECT
                DATE_TRUNC('month', payment_date) AS payment_month,
                COUNT(*) AS payment_count
            FROM loan_payments
            WHERE payment_date IS NOT NULL
            GROUP BY DATE_TRUNC('month', payment_date)
            ORDER BY payment_month
        """

        cursor.execute(payment_trend_query)
        payment_trend_rows = cursor.fetchall()

        payment_trend = []

        for trend_row in payment_trend_rows:
            payment_trend.append({
                "payment_month": trend_row[0].strftime("%Y-%m"),
                "payment_count": trend_row[1]
            })

        return {
            "status": "success",
            "data": {
                "total_payments": row[0],
                "completed_payments": row[1],
                "unsuccessful_payments": row[2],
                "total_payment_amount": float(row[3]),
                "total_principal_paid": float(row[4]),
                "total_interest_paid": float(row[5]),
                "average_payment_amount": float(row[6]),
                "total_payment_methods": row[7],
                "payment_trend": payment_trend
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