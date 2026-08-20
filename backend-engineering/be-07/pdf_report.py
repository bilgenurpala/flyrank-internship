from datetime import datetime, timezone
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


REPORTS_DIRECTORY = Path(__file__).with_name("generated-reports")


def generate_report(job_id, rows, title):
    REPORTS_DIRECTORY.mkdir(parents=True, exist_ok=True)
    path = REPORTS_DIRECTORY / f"task-summary-{job_id}.pdf"
    styles = getSampleStyleSheet()
    document = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title=title,
        author="Bilgenur Pala",
    )
    total = sum(row["total"] for row in rows)
    completed = sum(row["completed"] for row in rows)
    table_data = [["Category", "Total", "Completed", "Open"]]
    table_data.extend([[row["category"], row["total"], row["completed"], row["open"]] for row in rows])
    table = Table(table_data, colWidths=[70 * mm, 28 * mm, 32 * mm, 28 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#14524A")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#AEB4B2")),
        ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EAF2F0")]),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
    ]))
    story = [
        Paragraph(title, styles["Title"]),
        Paragraph(f"Generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}", styles["Normal"]),
        Spacer(1, 8 * mm),
        Paragraph(f"{completed} of {total} tasks are complete.", styles["Heading2"]),
        Spacer(1, 4 * mm),
        table,
    ]
    document.build(story)
    return path
