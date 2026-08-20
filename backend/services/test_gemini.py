from gemini_service import generate_report

prompt="""You are a banking Data Analyst
        Give me a short sample banking performance report with 3 key insights.
"""
report=generate_report(prompt)
print("\n---GEMINI REPORT---\n")
print(report)