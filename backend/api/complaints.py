from fastapi import APIRouter
from backend.database import get_db_connection

router = APIRouter(
    prefix="/complaints",
    tags=["Complaints"]
)


@router.get("/")
def get_complaints():
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
                complaint_id,
                complaint_code,
                customer_id,
                complaint_type,
                complaint_date,
                complaint_status,
                priority,
                resolution_date,
                resolution_description,
                created_at,
                updated_at
            FROM complaints
            ORDER BY complaint_date DESC
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