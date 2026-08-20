from backend.database import get_db_connection


def get_loan_summary():
    connection = get_db_connection()

    if connection is None:
        return {
            "status": "failed",
            "message": "Database connection failed"
        }

    cursor = None

    try:
        cursor = connection.cursor()

        # Overall loan summary
        summary_query = """
            SELECT
                COUNT(*) AS total_loans,
                COUNT(*) FILTER (
                    WHERE loan_status = 'Active'
                ) AS active_loans,
                COUNT(*) FILTER (
                    WHERE loan_status <> 'Active'
                ) AS inactive_loans,
                COALESCE(SUM(loan_amount), 0) AS total_loan_amount,
                COALESCE(SUM(outstanding_amount), 0) AS total_outstanding_amount,
                COALESCE(AVG(interest_rate), 0) AS average_interest_rate
            FROM loans
        """

        cursor.execute(summary_query)
        row = cursor.fetchone()

        # Loan-type financial exposure
        loan_type_query = """
            SELECT
                loan_type,
                COUNT(*) AS loan_count,
                COALESCE(SUM(loan_amount), 0) AS total_loan_amount,
                COALESCE(SUM(outstanding_amount), 0) AS total_outstanding_amount
            FROM loans
            GROUP BY loan_type
            ORDER BY total_outstanding_amount DESC
        """

        cursor.execute(loan_type_query)
        loan_type_rows = cursor.fetchall()

        loan_type_analysis = []

        for loan_type_row in loan_type_rows:
            loan_type_analysis.append({
                "loan_type": str(loan_type_row[0]),
                "loan_count": loan_type_row[1],
                "total_loan_amount": float(loan_type_row[2]),
                "total_outstanding_amount": float(loan_type_row[3])
            })

        return {
            "status": "success",
            "data": {
                "total_loans": row[0],
                "active_loans": row[1],
                "inactive_loans": row[2],
                "total_loan_amount": float(row[3]),
                "total_outstanding_amount": float(row[4]),
                "average_interest_rate": float(row[5]),
                "loan_type_analysis": loan_type_analysis
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