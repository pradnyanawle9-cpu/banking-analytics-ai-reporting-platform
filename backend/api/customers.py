from fastapi import APIRouter, HTTPException
from backend.database import get_db_connection

router = APIRouter(
    prefix="/api/customers",
    tags=["Customers"]
)


@router.get("/")
def get_customers():
    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                customer_id,
                customer_code,
                first_name,
                last_name,
                date_of_birth,
                gender,
                email,
                phone,
                occupation,
                annual_income,
                customer_status,
                created_at,
                updated_at
            FROM customers
            ORDER BY customer_id;
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
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()