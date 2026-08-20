from fastapi import APIRouter
from backend.database import get_db_connection

router = APIRouter(prefix="/loan-payments", tags=["Loan Payments"])


@router.get("/")
def get_loan_payments():
    connection = get_db_connection()

    if connection is None:
        return {
            "status": "failed",
            "message": "Database connection failed"
        }

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            payment_id,
            payment_code,
            loan_id,
            payment_date,
            payment_amount,
            principal_amount,
            interest_amount,
            payment_status,
            payment_method,
            created_at
        FROM loan_payments
        ORDER BY payment_id
    """)

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return {
        "status": "success",
        "count": len(rows),
        "data": rows
    }