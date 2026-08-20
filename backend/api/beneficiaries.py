from fastapi import APIRouter
from backend.database import get_db_connection

router = APIRouter(
    prefix="/beneficiaries",
    tags=["Beneficiaries"]
)


@router.get("/")
def get_beneficiaries():
    connection = get_db_connection()

    if connection is None:
        return {
            "status": "failed",
            "message": "Database connection failed"
        }

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            beneficiary_id,
            beneficiary_code,
            customer_id,
            beneficiary_name,
            account_number,
            bank_name,
            ifsc_code,
            beneficiary_type,
            beneficiary_status,
            created_at,
            updated_at
        FROM beneficiaries
        ORDER BY beneficiary_id
    """)

    beneficiaries = cursor.fetchall()

    cursor.close()
    connection.close()

    return {
        "status": "success",
        "count": len(beneficiaries),
        "data": beneficiaries
    }