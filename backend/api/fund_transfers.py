from fastapi import APIRouter
from backend.database import get_db_connection

router = APIRouter(
    prefix="/fund-transfers",
    tags=["Fund Transfers"]
)


@router.get("/")
def get_fund_transfers():
    connection = get_db_connection()

    if connection is None:
        return {
            "status": "failed",
            "message": "Database connection failed"
        }

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                transfer_id,
                transfer_code,
                customer_id,
                beneficiary_id,
                transfer_type,
                transfer_date,
                amount,
                transfer_status,
                remarks,
                created_at
            FROM fund_transfers
            ORDER BY transfer_date DESC
        """)

        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        data = [dict(zip(columns, row)) for row in rows]

        return {
            "status": "success",
            "count": len(data),
            "data": data
        }

    except Exception as e:
        return {
            "status": "failed",
            "message": str(e)
        }

    finally:
        cursor.close()
        connection.close()