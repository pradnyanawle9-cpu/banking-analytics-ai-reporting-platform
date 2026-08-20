from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


def generate_ai_report_pdf(report_data: dict) -> BytesIO:
    """
    Generate a professional PDF from the existing structured AI report.

    The AI summary is intentionally excluded.
    The PDF contains:
    - Query
    - Intent
    - KPIs
    - Visualization data
    - Table
    - Insights
    - Risks
    - Opportunities
    - Recommendations
    """

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title="Banking AI Report",
        author="Banking AI Reporting Platform",
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#5B21B6"),
        spaceAfter=8,
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=10,
        textColor=colors.HexColor("#6B7280"),
        spaceAfter=18,
    )

    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#4C1D95"),
        spaceBefore=12,
        spaceAfter=8,
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#374151"),
    )

    bullet_style = ParagraphStyle(
        "Bullet",
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-7,
        spaceAfter=5,
    )

    story = []

    # ---------------------------------------------------------
    # HEADER
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "Banking AI Reporting Platform",
            title_style,
        )
    )

    story.append(
        Paragraph(
            "AI-Powered Banking Analytics Report",
            subtitle_style,
        )
    )

    query = report_data.get("query", "")

    if query:
        story.append(Paragraph("<b>Query</b>", heading_style))
        story.append(Paragraph(str(query), body_style))
        story.append(Spacer(1, 8))

    # ---------------------------------------------------------
    # INTENT
    # ---------------------------------------------------------

    intent = report_data.get("intent", {})

    if intent:
        story.append(Paragraph("Analysis Context", heading_style))

        intent_rows = []

        for key, value in intent.items():
            if isinstance(value, list):
                value = ", ".join(str(item) for item in value)

            intent_rows.append(
                [
                    str(key).replace("_", " ").title(),
                    str(value),
                ]
            )

        intent_table = Table(
            intent_rows,
            colWidths=[48 * mm, 125 * mm],
            repeatRows=0,
        )

        intent_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (0, -1),
                        colors.HexColor("#F3E8FF"),
                    ),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, -1),
                        colors.HexColor("#374151"),
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (0, -1),
                        "Helvetica-Bold",
                    ),
                    (
                        "FONTNAME",
                        (1, 0),
                        (1, -1),
                        "Helvetica",
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.4,
                        colors.HexColor("#DDD6FE"),
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP",
                    ),
                    (
                        "PADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                ]
            )
        )

        story.append(intent_table)

    # ---------------------------------------------------------
    # KPIs
    # ---------------------------------------------------------

    kpis = report_data.get("kpis", [])

    if kpis:
        story.append(Paragraph("Key Performance Indicators", heading_style))

        kpi_rows = [["Metric", "Value", "Unit"]]

        for kpi in kpis:
            kpi_rows.append(
                [
                    str(kpi.get("label", "")),
                    str(kpi.get("value", "")),
                    str(kpi.get("unit", "")),
                ]
            )

        kpi_table = Table(
            kpi_rows,
            colWidths=[75 * mm, 55 * mm, 43 * mm],
            repeatRows=1,
        )

        kpi_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#5B21B6"),
                    ),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.white,
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold",
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.4,
                        colors.HexColor("#DDD6FE"),
                    ),
                    (
                        "ROWBACKGROUNDS",
                        (0, 1),
                        (-1, -1),
                        [
                            colors.white,
                            colors.HexColor("#FAF5FF"),
                        ],
                    ),
                    (
                        "PADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),
                ]
            )
        )

        story.append(kpi_table)

    # ---------------------------------------------------------
    # VISUALIZATION DATA
    # ---------------------------------------------------------

    charts = report_data.get("charts", [])

    if charts:
        story.append(Paragraph("Visual Analytics", heading_style))

        for chart in charts:
            chart_title = chart.get("title", "Chart")

            story.append(
                Paragraph(
                    f"<b>{chart_title}</b>",
                    body_style,
                )
            )

            chart_type = chart.get("type", "")
            description = chart.get("description", "")

            if description:
                story.append(
                    Paragraph(
                        description,
                        body_style,
                    )
                )

            story.append(
                Paragraph(
                    f"Visualization type: {chart_type.title()}",
                    body_style,
                )
            )

            chart_data = chart.get("data", [])

            if chart_data:
                chart_rows = [["Category", "Value"]]

                for item in chart_data:
                    chart_rows.append(
                        [
                            str(item.get("label", "")),
                            str(item.get("value", "")),
                        ]
                    )

                chart_table = Table(
                    chart_rows,
                    colWidths=[110 * mm, 63 * mm],
                    repeatRows=1,
                )

                chart_table.setStyle(
                    TableStyle(
                        [
                            (
                                "BACKGROUND",
                                (0, 0),
                                (-1, 0),
                                colors.HexColor("#7C3AED"),
                            ),
                            (
                                "TEXTCOLOR",
                                (0, 0),
                                (-1, 0),
                                colors.white,
                            ),
                            (
                                "FONTNAME",
                                (0, 0),
                                (-1, 0),
                                "Helvetica-Bold",
                            ),
                            (
                                "GRID",
                                (0, 0),
                                (-1, -1),
                                0.4,
                                colors.HexColor("#DDD6FE"),
                            ),
                            (
                                "ROWBACKGROUNDS",
                                (0, 1),
                                (-1, -1),
                                [
                                    colors.white,
                                    colors.HexColor("#FAF5FF"),
                                ],
                            ),
                            (
                                "PADDING",
                                (0, 0),
                                (-1, -1),
                                6,
                            ),
                        ]
                    )
                )

                story.append(Spacer(1, 5))
                story.append(chart_table)

    # ---------------------------------------------------------
    # TABLE
    # ---------------------------------------------------------

    table_data = report_data.get("table", {})

    if table_data and table_data.get("rows"):
        story.append(
            Paragraph(
                table_data.get("title", "Detailed Analysis"),
                heading_style,
            )
        )

        columns = table_data.get("columns", [])
        rows = table_data.get("rows", [])

        pdf_rows = [columns]

        for row in rows:
            values = row.get("values", [])
            pdf_rows.append([str(value) for value in values])

        report_table = Table(
            pdf_rows,
            repeatRows=1,
            colWidths=None,
        )

        report_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#5B21B6"),
                    ),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.white,
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold",
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.4,
                        colors.HexColor("#DDD6FE"),
                    ),
                    (
                        "ROWBACKGROUNDS",
                        (0, 1),
                        (-1, -1),
                        [
                            colors.white,
                            colors.HexColor("#FAF5FF"),
                        ],
                    ),
                    (
                        "FONTSIZE",
                        (0, 0),
                        (-1, -1),
                        8,
                    ),
                    (
                        "PADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP",
                    ),
                ]
            )
        )

        story.append(report_table)

    # ---------------------------------------------------------
    # AI ANALYSIS
    # NOTE: summary intentionally excluded
    # ---------------------------------------------------------

    analysis = report_data.get("analysis", {})

    sections = [
        ("Insights", analysis.get("insights", [])),
        ("Risks", analysis.get("risks", [])),
        ("Opportunities", analysis.get("opportunities", [])),
        ("Recommendations", analysis.get("recommendations", [])),
    ]

    for title, items in sections:
        if items:
            story.append(
                Paragraph(
                    title,
                    heading_style,
                )
            )

            for item in items:
                story.append(
                    Paragraph(
                        f"• {item}",
                        bullet_style,
                    )
                )

    # ---------------------------------------------------------
    # FOOTER
    # ---------------------------------------------------------

    story.append(Spacer(1, 18))

    story.append(
        Paragraph(
            "Generated by Banking AI Reporting Platform",
            subtitle_style,
        )
    )

    doc.build(story)

    buffer.seek(0)

    return buffer