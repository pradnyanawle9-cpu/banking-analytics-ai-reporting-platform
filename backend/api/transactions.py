from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from backend.database import get_db_connection

router = APIRouter(prefix="/transactions", tags=["Transactions"])


class Transaction(BaseModel):
    transaction_id: int
    transaction_code: str
    account_id: int
    transaction_type: str
    transaction_date: Optional[str]
    amount: float
    transaction_status: str
    description: Optional[str]
    created_at: Optional[str]


class TransactionResponse(BaseModel):
    status: str
    count: int
    data: List[Transaction]


@router.get("/", response_model=TransactionResponse)
def get_transactions():
    connection = get_db_connection()

    if connection is None:
        return {
            "status": "failed",
            "count": 0,
            "data": []
        }

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            transaction_id,
            transaction_code,
            account_id,
            transaction_type,
            transaction_date,
            amount,
            transaction_status,
            description,
            created_at
        FROM transactions
        ORDER BY transaction_id
    """)

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    data = []

    for row in rows:
        data.append({
            "transaction_id": row[0],
            "transaction_code": row[1],
            "account_id": row[2],
            "transaction_type": row[3],
            "transaction_date": row[4].isoformat() if row[4] else None,
            "amount": float(row[5]) if row[5] is not None else 0.0,
            "transaction_status": row[6],
            "description": row[7],
            "created_at": row[8].isoformat() if row[8] else None
        })

    return {
        "status": "success",
        "count": len(data),
        "data": data
    }