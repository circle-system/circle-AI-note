class MinutesService:

    def generate_minutes(
        self,
        transcript,
        notes
    ):

        return f"""
# 会議概要

{transcript}

# 決定事項

（要確認）

# ToDo

（要確認）

# 会議メモ

{notes}
"""