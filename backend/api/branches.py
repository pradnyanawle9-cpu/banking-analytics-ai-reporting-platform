from fastapi import APIRouter
from backend.database import get_db_connection

router = APIRouter(
    prefix="/api/branches",
    tags=["Branches"]
)


@router.get("/")
def get_branches():
    connection = get_db_connection()

    if connection is None:
        return {
            "status": "failed",
            "message": "Database connection failed"
        }

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            branch_id,
            branch_code,
            branch_name,
            city,
            state,
            branch_status
        FROM branches
        ORDER BY branch_id
    """)

    branches = cursor.fetchall()

    cursor.close()
    connection.close()

    return {
        "status": "success",
        "count": len(branches),
        "data": [
            {
                "branch_id": row[0],
                "branch_code": row[1],
                "branch_name": row[2],
                "city": row[3],
                "state": row[4],
                "branch_status": row[5]
            }
            for row in branches
        ]
    }