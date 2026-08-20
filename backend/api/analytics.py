from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel


from backend.analytics.branch_analytics import get_branch_transaction_analytics
from backend.analytics.customer_analytics import get_customer_analytics
from backend.analytics.account_analytics import get_account_summary
from backend.analytics.loan_analytics import get_loan_summary
from backend.analytics.transaction_analytics import get_transaction_analytics
from backend.analytics.card_analytics import get_card_analytics
from backend.analytics.fund_transfer_analytics import get_fund_transfer_analytics
from backend.analytics.complaint_analytics import get_complaint_analytics
from backend.analytics.credit_score_analytics import get_credit_score_analytics
from backend.analytics.card_transaction_analytics import get_card_transaction_analytics
from backend.analytics.loan_payment_analytics import get_loan_payment_analytics

from backend.services.gemini_service import generate_report,generate_structured_report
from backend.services.pdf_service import generate_ai_report_pdf

class ReportRequest(BaseModel):
    query: str


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/customers")
def customer_analytics():
    return get_customer_analytics()


@router.get("/accounts")
def account_analytics():
    return get_account_summary()


@router.get("/loans")
def loan_analytics():
    return get_loan_summary()


@router.get("/transactions")
def transaction_analytics():
    return get_transaction_analytics()


@router.get("/cards")
def card_analytics():
    return get_card_analytics()


@router.get("/fund-transfers")
def fund_transfer_analytics():
    return get_fund_transfer_analytics()


@router.get("/complaints")
def complaint_analytics():
    return get_complaint_analytics()


@router.get("/credit-scores")
def credit_score_analytics():
    return get_credit_score_analytics()


@router.get("/card-transactions")
def card_transaction_analytics():
    return get_card_transaction_analytics()


@router.get("/loan-payments")
def loan_payment_analytics():
    return get_loan_payment_analytics()

@router.get("/branches/transactions")
def branch_transaction_analytics():
    return get_branch_transaction_analytics()

@router.get("/ai-report")
def ai_report():

    customer_data = get_customer_analytics()
    account_data = get_account_summary()
    loan_data = get_loan_summary()
    transaction_data = get_transaction_analytics()
    card_data = get_card_analytics()
    fund_transfer_data = get_fund_transfer_analytics()
    complaint_data = get_complaint_analytics()
    credit_score_data = get_credit_score_analytics()
    card_transaction_data = get_card_transaction_analytics()
    loan_payment_data = get_loan_payment_analytics()
    branch_transaction_data=get_branch_transaction_analytics()

    analytics_data = {
        "customers": customer_data,
        "accounts": account_data,
        "loans": loan_data,
        "transactions": transaction_data,
        "cards": card_data,
        "fund_transfers": fund_transfer_data,
        "complaints": complaint_data,
        "credit_scores": credit_score_data,
        "card_transactions": card_transaction_data,
        "loan_payments": loan_payment_data,
        "branch_transactions": branch_transaction_data
    }

    prompt = f"""
You are a senior banking data analyst.

Analyze the following banking analytics data and generate a professional
business intelligence report.

Identify:
1. Key performance insights
2. Important trends or patterns
3. Potential business risks
4. Business opportunities
5. Actionable recommendations

Use ONLY the provided data.
Do not invent numbers or facts.

Banking Analytics Data:
{analytics_data}
"""

    report = generate_report(prompt)

    return {
        "status": "success",
        "report": report
    }
@router.post("/ai-report/query")
def ai_report_query(request: ReportRequest):

    customer_data = get_customer_analytics()
    account_data = get_account_summary()
    loan_data = get_loan_summary()
    transaction_data = get_transaction_analytics()
    card_data = get_card_analytics()
    fund_transfer_data = get_fund_transfer_analytics()
    complaint_data = get_complaint_analytics()
    credit_score_data = get_credit_score_analytics()
    card_transaction_data = get_card_transaction_analytics()
    loan_payment_data = get_loan_payment_analytics()
    branch_transaction_data = get_branch_transaction_analytics()

    analytics_data = {
        "customers": customer_data,
        "accounts": account_data,
        "loans": loan_data,
        "transactions": transaction_data,
        "cards": card_data,
        "fund_transfers": fund_transfer_data,
        "complaints": complaint_data,
        "credit_scores": credit_score_data,
        "card_transactions": card_transaction_data,
        "loan_payments": loan_payment_data,
        "branch_transactions": branch_transaction_data,
    }

    prompt = f"""
You are the query interpretation and reporting engine of a Banking
Analytics platform.

USER QUESTION:
{request.query}

AVAILABLE REAL BANKING ANALYTICS DATA:
{analytics_data}

Your task is to answer ONLY the user's question using ONLY the
available banking analytics data.

CRITICAL:
- Never invent a number.
- Never invent a category.
- Never invent a branch/customer/account/etc.
- Never use data that is unrelated to the user's question.
- Do not return a generic banking dashboard.
- Do not return all available analytics.
- Select ONLY the data required to answer the user's question.

If the user asks about loan payments:

- use loan payment analytics only.
- If the question asks about payment activity, payment volume, payment trend, payment history, or changes over time:
  - use loan_payments.payment_trend
  - operation = trend
  - return exactly ONE line chart
  - x_axis = payment_month
  - y_axis = payment_count
  - chart data must contain payment_month and payment_count from payment_trend
  - table must contain the same payment trend data
- Do NOT use loan portfolio data.
- Do NOT use loans.loan_type_analysis.
- Do NOT use unrelated banking analytics.

REPAYMENT PRIORITY RULE:

- If the user's question contains or clearly refers to repayment, loan repayment, repayment performance, repayment risk, repayment risks, payment performance, payment failure, failed payments, unsuccessful payments, payment activity, payment history, payment volume, payment trend, principal paid, interest paid, or loan payment performance:
  - domain MUST be "loan_payments".
  - use loan_payments analytics only.
  - Do NOT use loans.data.loan_type_analysis.
  - Do NOT use loan portfolio or loan-type exposure data.
  - Do NOT answer using overall loan portfolio metrics when loan payment metrics are available.

- This rule has priority over the general loan rule.

- Only use the "loans" domain when the user specifically asks about:
  - loan types
  - loan-type exposure
  - loan portfolio
  - loan amount
  - outstanding loan amount
  - loan ranking
  - comparison between loan types
  - highest/lowest loan type

LOAN-SPECIFIC RULE:
- When the user's question asks about loan types, loan-type exposure, highest/lowest loan type, loan-type ranking, or comparison between loan types, use `loans.data.loan_type_analysis`.
- For such questions, `loan_type` is the category.
- Use `total_outstanding_amount` as the financial exposure metric when the question asks about exposure.
- For ranking/comparison questions, return a bar chart and a table using ONLY `loan_type_analysis`.
- Sort loan types from highest to lowest when the question asks for greatest/highest/top exposure.
- Never substitute overall `total_loan_amount` or overall `total_outstanding_amount` for loan-type data when `loan_type_analysis` is available.

- If the requested information does not exist in the supplied data,
  say so clearly.
- All numeric values in KPIs, charts and tables MUST exist in the
  supplied data or be a mathematically valid calculation directly
  derived from supplied values.

RETURN ONLY VALID JSON.

Use EXACTLY this structure:

{{
  "query": "{request.query}",

  "intent": {{
    "domain": "customers|accounts|transactions|cards|loans|credit_scores|complaints|fund_transfers|card_transactions|loan_payments|branches|overview",
    "operation": "summary|comparison|ranking|trend|distribution|detail|risk|opportunity",
    "requested_entities": ["string"],
    "requested_metrics": ["string"]
  }},

  "kpis": [
    {{
      "label": "string",
      "value": "string",
      "unit": "number|currency|percentage|text",
      "source_field": "string"
    }}
  ],

  "charts": [
    {{
      "type": "bar|line|pie|donut",
      "title": "string",
      "description": "string",
      "x_axis": "string",
      "y_axis": "string",
      "data": [
        {{
          "label": "string",
          "value": 0
        }}
      ]
    }}
  ],

  "table": {{
    "title": "string",
    "columns": ["string"],
    "rows": [
      {{
        "values": ["string"]
      }}
    ]
  }},

  "analysis": {{
    "summary": "string",
    "insights": ["string"],
    "risks": ["string"],
    "opportunities": ["string"],
    "recommendations": ["string"]
  }}
}}

KPI RULES:
1. Return at least 4 KPIs when the available data supports them.
2. Every KPI must directly help answer the user's question.
3. Do NOT fill KPIs with unrelated banking metrics just to reach four.
4. If fewer than four meaningful KPIs are possible, return only the
   meaningful ones.
5. KPI values must come from the supplied data or direct calculations.

CHART RULES:
1. Return ZERO charts if the question does not require a visualization.
2. Return ONE chart when one visualization answers the question.
3. Return TWO charts only when two genuinely different visualizations
   are useful.
4. Ranking/comparison -> bar chart.
5. Trend over ordered/time data -> line chart.
6. Distribution/proportion -> pie or donut.
7. Never create a chart containing unrelated categories.
8. Chart data must come only from the relevant supplied data.

TABLE RULES:
1. The table must answer the user's exact question.
2. Include ONLY relevant columns.
3. Include ONLY relevant rows.
4. Do not return the entire database analytics dataset.
5. For ranking questions, sort rows from highest to lowest unless
   the question explicitly asks otherwise.
6. For "highest", "top", "lowest", "bottom", etc., return the
   corresponding ranked records.
7. Preserve the actual names and values from the supplied data.

QUERY-SPECIFIC BEHAVIOR:

If the user asks:
"which branches have the highest transaction activity?"

Then:
- domain = branches
- operation = ranking
- use branch transaction data
- rank branches by transaction count
- KPIs must describe branch transaction performance
- chart should show branch transaction ranking
- table should contain branch name and transaction activity data
- DO NOT show customer, loan, card or generic transaction charts.

If the user asks about customers:
- use customer analytics only.

If the user asks about accounts:
- use account analytics only.

If the user asks about loans:
- use loan analytics only.

If the user asks about cards:
- use card analytics only.

If the user asks about credit scores:
- use credit score analytics only.

If the user asks about complaints:
- use complaint analytics only.

If the user asks about fund transfers:
- use fund transfer analytics only.

If the user asks about card transactions:
- use card transaction analytics only.

If the user asks about loan payments:
- use loan payment analytics only.

If the user asks about general transactions:
- use transaction analytics only.

IMPORTANT:
The frontend will render the report entirely from this JSON.
Therefore, do NOT return a fixed dashboard structure.

Return JSON only.
No markdown.
No explanation outside JSON.
"""

    structured_result = generate_structured_report(prompt)
    print("PDF STRUCTURED RESULT:")
    print(structured_result)

    print("PDF RESULT KEYS:", structured_result.keys())
    if structured_result.get("status") == "error":
      return structured_result
    return {
        "status": "success",
        "query": request.query,
        "result": structured_result,
     }
@router.post("/ai-report/pdf")
def generate_ai_report_pdf_endpoint(request: ReportRequest):

    response = ai_report_query(request)

    if response.get("status") == "error":
        return response

    structured_result = response.get("result", {})

    pdf_buffer = generate_ai_report_pdf(structured_result)

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": 'attachment; filename="banking_ai_report.pdf"'
        },
    )