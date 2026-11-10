import re

class MinutesService:

    def generate_minutes(
        self,
        transcript,
        notes
    ):

        summary = self.create_summary(
            transcript
        )

        decisions = self.extract_decisions(
            transcript,
            notes
        )

        todos = self.extract_todos(
            transcript,
            notes
        )

        members = self.extract_members(
            transcript,
            notes
        )

        return f"""
# 会議概要

{summary}

# 出席者候補

{members}

# 決定事項

{decisions}

# ToDo

{todos}

# 会議メモ

{notes}

# 文字起こし全文

{transcript}
""".strip()

    def create_summary(
        self,
        transcript
    ):

        decision_keywords = [
            "決定",
            "承認",
            "採用",
            "確定",
            "可決"
        ]

        todo_keywords = [
            "作成",
            "提出",
            "確認",
            "連絡",
            "申請",
            "対応",
            "準備",
            "修正",
            "送付",
            "共有"
        ]

        summary = []

        for sentence in self.split_sentences(
            transcript
        ):

            if  any(
                keyword in sentence
                for keyword in decision_keywords
            ):
                continue

            if any(
                keyword in sentence
                for keyword in todo_keywords
            ):
                continue

            summary.append(
                f"・{sentence}"
            )

        if not summary:

            return "会議の目的や背景を抽出できませんでした"

        return "\n".join(summary[:5])

    def extract_members(
        self,
        transcript,
        notes
    ):

        candidates = [
            "佐々木",
            "田中",
            "山田",
            "鈴木",
            "中村",
            "高橋",
            "伊藤",
            "荒木"
        ]

        result = []

        text = (
            transcript +
            "\n" +
            notes
        )

        for name in candidates:

            if name in text:

                result.append(
                    f"・{name}"
                )

        if not result:

            return "・抽出できませんでした"

        return "\n".join(result)

    def extract_decisions(
        self,
        transcript,
        notes
    ):

        decision_keywords = [
            "決定",
            "承認",
            "採用",
            "確定",
            "可決"
        ]

        decisions = []

        text = transcript + "\n" + notes

        for sentence in self.split_sentences(
            text
        ):

            if any(
                keyword in sentence
                for keyword in decision_keywords
            ):

                decisions.append(
                    f"・{sentence}"
                )

        if not decisions:

            return "・決定事項は抽出されませんでした"

        return "\n".join(decisions)

    def extract_todos(
        self,
        transcript,
        notes
    ):

        todo_keywords = [
            "作成",
            "提出",
            "確認",
            "連絡",
            "申請",
            "対応",
            "準備",
            "修正",
            "送付",
            "共有"
        ]

        todos = []

        text = transcript + "\n" + notes

        for sentence in self.split_sentences(
            text
        ):

            if any(
                keyword in sentence
                for keyword in todo_keywords
            ):

                assignee = self.extract_assignee(
                    sentence
                )

                deadline = self.extract_deadline(
                    sentence
                )

                todos.append(
                    f"""・内容: {sentence}
    担当: {assignee}
    期限: {deadline}"""
                )

        if not todos:

            return "・ToDoは抽出されませんでした"

        return "\n\n".join(todos)

    def split_sentences(
        self,
        text
    ):

        sentences = re.split(
            r"[。！？]",
            text
        )

        return [
            s.strip()
            for s in sentences
            if s.strip()
        ]

    def extract_deadline(
        self,
        sentence
    ):

        patterns = [

            r"\d+月\d+日",

            r"\d+/\d+",

            r"今週中",

            r"来週",

            r"次回まで",

            r"月末"
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                sentence
            )

            if match:

                return match.group()

        return "未設定"

    def extract_assignee(
        self,
        sentence
    ):

        persons = get_persons()

        candidates = [
            p.name
            for p in persons
        ]

        for name in candidates:

            if name in sentence:

                return name

        return "未設定"