from fastapi import APIRouter
from backend.database import get_db_connection

router = APIRouter(
    prefix="/card-transactions",
    tags=["Card Transactions"]
)


@router.get("/")
def get_card_transactions():
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
                card_transaction_id,
                transaction_code,
                card_id,
                transaction_date,
                transaction_type,
                amount,
                merchant_name,
                transaction_status,
                description,
                created_at
            FROM card_transactions
            ORDER BY transaction_date DESC
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