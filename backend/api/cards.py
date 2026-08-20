from fastapi import APIRouter
from backend.database import get_db_connection

router = APIRouter(
    prefix="/cards",
    tags=["Cards"]
)


@router.get("/")
def get_cards():
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
                card_id,
                card_number,
                customer_id,
                card_type,
                card_status,
                issue_date,
                expiry_date,
                credit_limit,
                available_limit,
                created_at,
                updated_at
            FROM cards
            ORDER BY card_id
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