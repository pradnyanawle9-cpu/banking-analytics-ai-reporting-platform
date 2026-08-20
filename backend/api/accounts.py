from fastapi import APIRouter, HTTPException
from backend.database import get_db_connection

router = APIRouter(
    prefix="/api/accounts",
    tags=["Accounts"]
)


@router.get("/")
def get_accounts():
    connection = None
    cursor = None

    try:
        connection = get_db_connection()

        if connection is None:
            raise HTTPException(
                status_code=500,
                detail="Database connection failed"
            )

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                account_id,
                account_number,
                customer_id,
                branch_id,
                account_type,
                account_status,
                opening_date,
                closing_date,
                current_balance,
                created_at,
                updated_at
            FROM accounts
            ORDER BY account_id;
        """)

        rows = cursor.fetchall()

        columns = [desc[0] for desc in cursor.description]

        data = [dict(zip(columns, row)) for row in rows]

        return {
            "status": "success",
            "count": len(data),
            "data": data
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()