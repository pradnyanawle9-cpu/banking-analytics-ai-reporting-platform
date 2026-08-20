from backend.database import get_db_connection


def get_card_analytics():
    connection = get_db_connection()

    if connection is None:
        return {
            "status": "failed",
            "message": "Database connection failed"
        }

    cursor = None

    try:
        cursor = connection.cursor()

        # ---------------------------------------------------------
        # 1. Overall card summary
        # ---------------------------------------------------------
        cursor.execute("""
            SELECT
                COUNT(*) AS total_cards,

                COUNT(*) FILTER (
                    WHERE card_status = 'Active'
                ) AS active_cards,

                COUNT(*) FILTER (
                    WHERE card_status <> 'Active'
                ) AS inactive_cards,

                COUNT(*) FILTER (
                    WHERE card_type = 'Credit'
                ) AS credit_cards,

                COUNT(*) FILTER (
                    WHERE card_type = 'Debit'
                ) AS debit_cards,

                COALESCE(SUM(credit_limit), 0) AS total_credit_limit,

                COALESCE(SUM(available_limit), 0) AS total_available_limit

            FROM cards
        """)

        summary = cursor.fetchone()

        # ---------------------------------------------------------
        # 2. Card status distribution
        # ---------------------------------------------------------
        cursor.execute("""
            SELECT
                card_status,
                COUNT(*) AS card_count
            FROM cards
            GROUP BY card_status
            ORDER BY card_count DESC
        """)

        status_rows = cursor.fetchall()

        card_status_distribution = [
            {
                "status": row[0],
                "count": row[1]
            }
            for row in status_rows
        ]

        # ---------------------------------------------------------
        # 3. Card type distribution
        # ---------------------------------------------------------
        cursor.execute("""
            SELECT
                card_type,
                COUNT(*) AS card_count
            FROM cards
            GROUP BY card_type
            ORDER BY card_count DESC
        """)

        type_rows = cursor.fetchall()

        card_type_distribution = [
            {
                "card_type": row[0],
                "count": row[1]
            }
            for row in type_rows
        ]

        # ---------------------------------------------------------
        # 4. Credit utilization
        # ---------------------------------------------------------
        total_credit_limit = float(summary[5])
        total_available_limit = float(summary[6])

        utilized_credit_limit = (
            total_credit_limit - total_available_limit
        )

        utilization_percentage = (
            (utilized_credit_limit / total_credit_limit) * 100
            if total_credit_limit > 0
            else 0
        )

        # ---------------------------------------------------------
        # 5. Credit limit comparison data
        # ---------------------------------------------------------
        credit_limit_metrics = [
            {
                "metric": "Total Credit Limit",
                "value": total_credit_limit
            },
            {
                "metric": "Available Credit",
                "value": total_available_limit
            },
            {
                "metric": "Utilized Credit",
                "value": utilized_credit_limit
            }
        ]

        # ---------------------------------------------------------
        # Final response
        # ---------------------------------------------------------
        return {
            "status": "success",

            "data": {
                # KPI values
                "total_cards": summary[0],
                "active_cards": summary[1],
                "inactive_cards": summary[2],
                "credit_cards": summary[3],
                "debit_cards": summary[4],

                "total_credit_limit": total_credit_limit,
                "total_available_limit": total_available_limit,

                "utilized_credit_limit": utilized_credit_limit,
                "utilization_percentage": round(
                    utilization_percentage,
                    2
                ),

                # Chart data
                "card_status_distribution":
                    card_status_distribution,

                "card_type_distribution":
                    card_type_distribution,

                "credit_limit_metrics":
                    credit_limit_metrics
            }
        }

    except Exception as e:

        return {
            "status": "failed",
            "message": str(e)
        }

    finally:

        if cursor is not None:
            cursor.close()

        connection.close()