from fastapi import APIRouter
from backend.database import get_db_connection

router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


@router.get("/")
def get_employees():
    connection = get_db_connection()

    if connection is None:
        return {
            "status": "failed",
            "message": "Database connection failed"
        }

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            employee_id,
            employee_code,
            first_name,
            last_name,
            designation,
            department,
            branch_id,
            joining_date,
            salary,
            employee_status,
            created_at,
            updated_at
        FROM employees
        ORDER BY employee_id
    """)

    employees = cursor.fetchall()

    cursor.close()
    connection.close()

    return {
        "status": "success",
        "count": len(employees),
        "data": employees
    }