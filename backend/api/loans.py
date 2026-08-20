from fastapi import APIRouter
from backend.database import get_db_connection

router = APIRouter(prefix="/loans", tags=["Loans"])


@router.get("/")
def get_loans():
    connection = get_db_connection()

    if connection is None:
        return {
            "status": "failed",
            "message": "Database connection failed"
        }

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            loan_id,
            loan_number,
            customer_id,
            loan_type,
            loan_amount,
            interest_rate,
            tenure_months,
            loan_status,
            application_date,
            approval_date,
            disbursement_date,
            outstanding_amount,
            created_at,
            updated_at
        FROM loans
        ORDER BY loan_id
    """)

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return {
        "status": "success",
        "count": len(rows),
        "data": rows
    }