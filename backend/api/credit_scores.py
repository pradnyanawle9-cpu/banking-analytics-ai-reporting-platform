from fastapi import APIRouter
from backend.database import get_db_connection

router = APIRouter(
    prefix="/credit-scores",
    tags=["Credit Scores"]
)


@router.get("/")
def get_credit_scores():
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
                credit_score_id,
                customer_id,
                credit_score,
                score_date,
                score_category,
                created_at,
                updated_at
            FROM credit_scores
            ORDER BY score_date DESC
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