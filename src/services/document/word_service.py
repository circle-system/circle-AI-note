from pathlib import Path

from docx import Document


class WordService:

    def export_minutes(
        self,
        meeting_title,
        minutes
    ):

        minutes_dir = (
            Path.home()
            / "AI_Minutes"
            / "minutes"
        )

        minutes_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        safe_title = (
            meeting_title
            .replace("/", "_")
            .replace("\\", "_")
            .replace(":", "_")
            .replace("*", "_")
            .replace("?", "_")
            .replace('"', "_")
            .replace("<", "_")
            .replace(">", "_")
            .replace("|", "_")
        )

        file_path = (
            minutes_dir
            / f"{safe_title}.docx"
        )

        document = Document()

        document.add_heading(
            meeting_title,
            level=1
        )

        document.add_paragraph(
            minutes
        )

        document.save(
            str(file_path)
        )

        return str(file_path)