from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import get_db_connection
from backend.api.branches import router as branches_router
from backend.api.customers import router as customers_router
from backend.api.accounts import router as accounts_router
from backend.api.employees import router as employees_router
from backend.api.beneficiaries import router as beneficiaries_router
from backend.api.card_transactions import router as card_transactions_router
from backend.api.cards import router as cards_router
from backend.api.complaints import router as complaints_router
from backend.api.credit_scores import router as credit_scores_router
from backend.api.fund_transfers import router as fund_transfers_router
from backend.api.loan_payments import router as loan_payments_router
from backend.api.loans import router as loans_router
from backend.api.transactions import router as transactions_router
from backend.api.analytics import router as analytics_router

app = FastAPI(
    title="Banking AI Reporting Platform",
    description="AI-powered banking analytics and reporting backend",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(branches_router)
app.include_router(customers_router)
app.include_router(accounts_router)
app.include_router(employees_router)
app.include_router(beneficiaries_router)
app.include_router(card_transactions_router)
app.include_router(cards_router)
app.include_router(complaints_router)
app.include_router(credit_scores_router)
app.include_router(fund_transfers_router)
app.include_router(loan_payments_router)
app.include_router(loans_router)
app.include_router(transactions_router)
app.include_router(analytics_router)

@app.get("/")
def root():
    return {
        "message": "Banking AI Reporting Platform API is running!"
    }


@app.get("/db-test")
def db_test():
    connection = get_db_connection()

    if connection is None:
        return {
            "status": "failed",
            "message": "Database connection failed"
        }

    connection.close()

    return {
        "status": "success",
        "message": "PostgreSQL database connected successfully"
    }