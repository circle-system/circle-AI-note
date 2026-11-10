# src/ui/pages/recording_page.py

from pathlib import Path
from datetime import datetime

from PySide6.QtCore import (
    Qt,
    QTimer
)

from PySide6.QtWidgets import (
    QWidget,
    QTextEdit,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QListWidget,
    QMessageBox
)

from services.recording.recorder import Recorder

from core.app_state import AppState

from database.repository import (
    save_note,
    get_notes,
    get_meeting,
    get_settings,
    save_transcript,
    save_minutes,
    update_meeting_audio,
)

from services.speech.speech_service import (
    SpeechService
)


from services.ai.minutes_service import (
    MinutesService
)


from services.document.word_service import (
    WordService
)

from services.document.pdf_service import (
    PdfService
)

import os
import webbrowser

class RecordingPage(QWidget):

    def __init__(self):
        super().__init__()

        self.recorder = Recorder()

        self.is_recording = False

        self.current_file_path = ""

        self.elapsed_seconds = 0

        self.timer = QTimer()
        self.timer.timeout.connect(
            self.update_timer
        )

        # =================
        # レイアウト
        # =================

        layout = QHBoxLayout(self)

        # =================
        # 左側
        # =================

        left = QVBoxLayout()

        # 会議名

        self.meeting_title_label = QLabel(
            "会議未選択"
        )

        self.meeting_title_label.setStyleSheet("""
            font-size:20px;
            font-weight:bold;
        """)

        self.meeting_title_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        # マイク

        self.mic_label = QLabel("🎤")

        self.mic_label.setStyleSheet("""
            font-size:80px;
            color:gray;
        """)

        self.mic_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        #  状態

        self.status_label = QLabel(
            "待機中"
        )

        self.status_label.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
            color:gray;
        """)

        self.status_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        # タイマー

        self.timer_label = QLabel(
            "00:00:00"
        )

        self.timer_label.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
        """)

        self.timer_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        # ファイル表示

        self.file_label = QLabel(
            "録音ファイルなし"
        )

        self.file_label.setWordWrap(True)

        self.file_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        # ボタン

        self.record_button = QPushButton(
            "録音開始"
        )

        self.record_button.clicked.connect(
            self.toggle_record
        )

        self.transcript_button = QPushButton(
            "文字起こし"
        )

        self.transcript_button.clicked.connect(
            self.transcribe_audio
        )

        self.minutes_button = QPushButton(
            "議事録生成"
        )

        self.minutes_button.clicked.connect(
            self.generate_minutes
        )

        self.export_button = QPushButton(
            "Word出力"
        )

        self.export_button.clicked.connect(
            self.export_to_word
        )

        self.pdf_service = PdfService()

        self.pdf_button = QPushButton(
            "PDF出力"
        )

        self.pdf_button.clicked.connect(
            self.export_to_pdf
        )

        # -----------------
        # ボタンエリア
        # -----------------

        left.addWidget(
            self.minutes_button
        )

        left.addWidget(
            self.export_button
        )

        left.addWidget(
            self.pdf_button
        )

# -----------------
# 中央表示エリア
# -----------------

        center_widget = QWidget()

        center_layout = QVBoxLayout(
            center_widget
        )

        center_layout.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        center_layout.addWidget(
            self.meeting_title_label
        )

        center_layout.addWidget(
            self.mic_label
        )

        center_layout.addWidget(
            self.status_label
        )

        center_layout.addWidget(
            self.timer_label
        )

        center_layout.addWidget(
            self.file_label
        )

        center_layout.addWidget(
            self.record_button
        )

        center_layout.addWidget(
            self.transcript_button
        )

        left.addWidget(
            center_widget,
            1
        )

# =================
# 右側
# =================

        right = QVBoxLayout()

        memo_title = QLabel(
            "会議メモ"
        )

        self.memo_area = QTextEdit()

        self.memo_area.setPlaceholderText(
            "会議中のメモを入力..."
        )

        self.send_button = QPushButton(
            "保存"
        )

        self.memo_list = QListWidget()

        right.addWidget(
            memo_title
        )

        right.addWidget(
            self.memo_area,
            1
        )

        right.addWidget(
            self.send_button
        )

        right.addWidget(
            QLabel("保存済みメモ")
        )

        right.addWidget(
            self.memo_list,
            1
        )

# =====================
# 文字起こし結果
# =====================

        right.addWidget(
            QLabel("文字起こし")
        )

        self.transcript_area = QTextEdit()

        self.transcript_area.setReadOnly(
            True
        )

        right.addWidget(
            self.transcript_area,
            2
        )

# =====================
# 議事録
# =====================

        right.addWidget(
            QLabel("議事録")
        )

        self.minutes_area = QTextEdit()

        self.minutes_area.setReadOnly(
            True
        )

        right.addWidget(
            self.minutes_area,
            3
        )

# =====================
# 左右配置
# =====================

        layout.addLayout(
            left,
            2
        )

        layout.addLayout(
            right,
            1
        )

        self.loaded_meeting_id = None

        self.send_button.clicked.connect(
            self.save_memo
        )

        self.page_timer = QTimer()

        self.page_timer.timeout.connect(
            self.update_meeting_title
        )

        self.page_timer.start(500)

        self.speech_service = (
            SpeechService()
        )

        self.minutes_service = (
            MinutesService()
        )

        self.word_service = (
            WordService()
        )  

    def check_meeting_change(self):

        if AppState.meeting_changed:

            self.load_notes()

            AppState.meeting_changed = False

    # ==================================
    # 録音開始/停止切り替え
    # ==================================

    def toggle_record(self):

        if not self.is_recording:

            self.start_recording()

        else:

            self.stop_recording()

    # ==================================
    # 録音開始
    # ==================================

    def start_recording(self):

        recording_dir = (
            Path.home()
            / "AI_Minutes"
            / "recordings"
        )

        recording_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        meeting_id = AppState.current_meeting_id

        if meeting_id is None:
            meeting_id = "unknown"

        self.current_file_path = str(
            recording_dir
            / f"meeting_{meeting_id}_{timestamp}.wav"
        )

        self.recorder.start_recording(
            self.current_file_path
        )

        self.elapsed_seconds = 0

        self.timer_label.setText(
            "00:00:00"
        )

        self.timer.start(1000)

        self.is_recording = True

        self.record_button.setText(
            "録音停止"
        )

        self.file_label.setText(
            f"""
        録音中...

        保存先:
        {self.current_file_path}
        """
        )

        self.status_label.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
            color:red;
        """)

        self.mic_label.setStyleSheet("""
            font-size:80px;
            color:red;
        """)

        self.file_label.setText(
            f"保存先:\n{self.current_file_path}"
        )

    # ==================================
    # 録音停止
    # ==================================

    def stop_recording(self):
        
        saved_file = (
            self.recorder.stop_recording()
        )

        if AppState.current_meeting_id:

            update_meeting_audio(
                AppState.current_meeting_id,
                saved_file
            )

        self.timer.stop()

        self.is_recording = False

        self.record_button.setText(
            "録音開始"
        )

        self.status_label.setText(
            "■ 停止"
        )

        self.status_label.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
            color:green;
        """)

        self.mic_label.setStyleSheet("""
            font-size:80px;
            color:green;
        """)

        self.file_label.setText(
            f"""
        保存済

        {saved_file}

        録音時間:
        {self.timer_label.text()}
        """
        )

    # ==================================
    # タイマー更新
    # ==================================

    def update_timer(self):

        self.elapsed_seconds += 1

        hours = (
            self.elapsed_seconds // 3600
        )

        minutes = (
            self.elapsed_seconds % 3600
        ) // 60

        seconds = (
            self.elapsed_seconds % 60
        )

        self.timer_label.setText(
            f"{hours:02}:{minutes:02}:{seconds:02}"
        )

    def save_memo(self):

        memo_text = (
            self.memo_area
            .toPlainText()
            .strip()
        )

        if not memo_text:
            return

        if AppState.current_meeting_id is None:
            return

        timestamp = (
            self.timer_label.text()
        )

        save_note(
            AppState.current_meeting_id,
            timestamp,
            memo_text
        )

        

        self.load_notes()

        self.memo_area.clear()

    def load_notes(self):

        self.memo_list.clear()

        if AppState.current_meeting_id is None:
            return

        notes = get_notes(
            AppState.current_meeting_id
        )

        for note in notes:

            self.memo_list.addItem(
                f"[{note.timestamp}] {note.content}"
            )

    def update_meeting_title(self):

        if AppState.current_meeting_title:

            self.meeting_title_label.setText(
                f"会議名:\n{AppState.current_meeting_title}"
            )

        if (
            AppState.current_meeting_id
            != self.loaded_meeting_id
        ):

            self.loaded_meeting_id = (
                AppState.current_meeting_id
            )

            self.load_notes()
            self.load_minutes()
            self.load_transcript()

    def export_to_word(self):

        try:

            if AppState.current_meeting_id is None:

                QMessageBox.warning(
                    self,
                    "エラー",
                    "会議が選択されていません"
                )

                return

            meeting = get_meeting(
                AppState.current_meeting_id
            )

            if not meeting:

                QMessageBox.warning(
                    self,
                    "エラー",
                    "会議情報が見つかりません"
                )

                return

            minutes = (
                self.minutes_area
                .toPlainText()
                .strip()
            )

            if not minutes:

                QMessageBox.warning(
                    self,
                    "エラー",
                    "議事録が生成されていません"
                )

                return

            file_path = (
                self.word_service.export_minutes(
                    meeting.title,
                    minutes
                )
            )

            QMessageBox.information(
                self,
                "保存完了",
                f"{file_path}\nへ保存しました"
            )

        except PermissionError:

            QMessageBox.critical(
                self,
                "保存失敗",
                "Wordファイルが開かれています。\n閉じてから再度保存してください。"
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "予期しないエラー",
                str(error)
            )

            print(error)

    def transcribe_audio(self):

        if self.is_recording:

            print(
                "録音中は文字起こしできません"
            )

            return

        if not self.current_file_path:

            return


        transcript = (
            self.speech_service
            .transcribe_file(
                self.current_file_path
            )
        )

        save_transcript(
            AppState.current_meeting_id,
            transcript
        )

        self.transcript_area.setPlainText(
            transcript
        )

        print()
        print("=====文字起こし結果=====")
        self.transcript_area.setPlainText(
            transcript
        )

    def generate_minutes(self):

        if AppState.current_meeting_id is None:
            return

        meeting = get_meeting(
            AppState.current_meeting_id
        )

        if not meeting:
            return

        notes = []

        for i in range(
            self.memo_list.count()
        ):

            notes.append(
                self.memo_list.item(i).text()
            )

        minutes = (
            self.minutes_service
            .generate_minutes(
                meeting.transcript or "",
                "\n".join(notes)
            ) 
        )

        self.minutes_area.setPlainText(
            minutes
        )

        save_minutes(
            AppState.current_meeting_id,
            minutes
        )

    def load_minutes(self):

        if AppState.current_meeting_id is None:
            return

        meeting = get_meeting(
            AppState.current_meeting_id
        )

        if meeting:

            self.minutes_area.setPlainText(
                meeting.minutes or ""
            )

    def load_transcript(self):

        if AppState.current_meeting_id is None:
            return

        meeting = get_meeting(
            AppState.current_meeting_id
        )

        if meeting:

            self.transcript_area.setPlainText(
                meeting.transcript or ""
            )

    def export_to_pdf(self):

        try:

            if AppState.current_meeting_id is None:

                QMessageBox.warning(
                    self,
                    "エラー",
                    "会議を選択してください"
                )

                return

            meeting = get_meeting(
                AppState.current_meeting_id
            )

            if not meeting:

                QMessageBox.warning(
                    self,
                    "エラー",
                    "会議情報が見つかりません"
                )

                return

            minutes = (
                self.minutes_area
                .toPlainText()
                .strip()
            )

            if not minutes:

                QMessageBox.warning(
                    self,
                    "エラー",
                    "議事録が生成されていません"
                )

                return

            pdf_path = (
                self.pdf_service.export_minutes(
                    meeting.title,
                    minutes
                )
            )

            settings = get_settings()

            teams_url = ""

            if settings:

                teams_url = (
                    settings.teams_url
                )

            msg = QMessageBox(self)

            msg.setWindowTitle(
                "PDF出力完了"
            )

            msg.setIcon(
                QMessageBox.Information
            )

            msg.setText(
                f"""
    PDFを保存しました

    保存先:
    {pdf_path}

    次の手順

    ① Teams が開きます

    ② 「保存フォルダを開く」をクリック

    ③ PDF ファイルを
    Teamsへドラッグ＆ドロップ

    ④ 投稿完了
    """
            )

            open_pdf_button = msg.addButton(
                "PDFを開く",
                QMessageBox.ActionRole
            )

            open_folder_button = msg.addButton(
                "保存フォルダを開く",
                QMessageBox.ActionRole
            )

            msg.addButton(
                QMessageBox.Ok
            )

            if teams_url:

                import webbrowser

                webbrowser.open(
                    teams_url
                )

            msg.exec()

            clicked_button = (
                msg.clickedButton()
            )

            if clicked_button == open_pdf_button:

                import os

                os.startfile(
                    pdf_path
                )

            elif clicked_button == open_folder_button:

                import os

                os.startfile(
                    os.path.dirname(
                        os.path.abspath(
                            pdf_path
                        )
                    )
                )

        except PermissionError:

            QMessageBox.critical(
                self,
                "保存失敗",
                "PDFファイルが開かれています。"
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "エラー",
                str(error)
            )

            print(error)