from pathlib import Path

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet


class PdfService:

    def export_minutes(
        self,
        meeting_title,
        minutes
    ):

        safe_title = (
            meeting_title
            .replace("/", "_")
            .replace("\\", "_")
            .replace(":", "_")
        )

        pdf_dir = (
            Path.home()
            / "AI_Minutes"
            / "pdf"
        )

        pdf_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        pdf_path = (
            pdf_dir
            / f"{safe_title}.pdf"
        )


        font_path = (
            "C:/Windows/Fonts/msgothic.ttc"
        )

        pdfmetrics.registerFont(
            TTFont(
                "MSGothic",
                font_path
            )
        )

        document = SimpleDocTemplate(
            str(pdf_path)
        )

        styles = getSampleStyleSheet()

        styles["Normal"].fontName = (
            "MSGothic"
        )

        styles["Title"].fontName = (
            "MSGothic"
        )

        story = []

        story.append(
            Paragraph(
                meeting_title,
                styles["Title"]
            )
        )

        story.append(
            Spacer(1, 10)
        )

        for line in minutes.split("\n"):

            story.append(
                Paragraph(
                    line,
                    styles["Normal"]
                )
            )

        document.build(
            story
        )

        return str(pdf_path)