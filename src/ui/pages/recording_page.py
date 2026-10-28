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
    QListWidget
)

from services.recording.recorder import Recorder

from core.app_state import AppState

from database.repository import (
    save_note
)

from database.repository import (
    save_note,
    get_notes,
    update_meeting_audio

)

from services.speech.speech_service import (
    SpeechService
)

from database.repository import (
    save_transcript
)

from services.ai.minutes_service import (
    MinutesService
)

from database.repository import (
    save_minutes,
    get_meeting
)


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

        left = QVBoxLayout()

        self.mic_label = QLabel("🎤")

        self.mic_label.setStyleSheet("""
            font-size:80px;
            color:gray;
        """)

        self.mic_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

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

        self.file_label = QLabel(
            "録音ファイルなし"
        )

        self.file_label.setWordWrap(True)

        self.file_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.record_button = QPushButton(
            "録音開始"
        )

        self.record_button.clicked.connect(
            self.toggle_record
        )

        self.transcript_button = QPushButton(
            "文字起こし"
        )

        self.minutes_button = QPushButton(
            "議事録生成"
        )

        self.minutes_button.clicked.connect(
            self.generate_minutes
        )

        self.transcript_button.clicked.connect(
            self.transcribe_audio
        )

        left.addWidget(
            self.transcript_button
        )

        left.addWidget(
            self.minutes_button
        )

        left.addStretch()

        left.addWidget(
            self.meeting_title_label
        )

        left.addWidget(self.mic_label)

        left.addWidget(self.status_label)

        left.addWidget(self.timer_label)

        left.addWidget(self.file_label)

        left.addWidget(self.record_button)

        left.addWidget(self.transcript_button)

        left.addStretch()

        # =================
        # 右側
        # =================

        right = QVBoxLayout()

        memo_title = QLabel("会議メモ")

        self.memo_area = QTextEdit()

        self.memo_area.setPlaceholderText(
            "会議中のメモを入力..."
        )

        self.send_button = QPushButton(
            "保存"
        )

        self.memo_list = QListWidget()

        right.addWidget(memo_title)

        right.addWidget(self.memo_area)

        right.addWidget(self.send_button)

        right.addWidget(
            QLabel("保存済みメモ")
        )

        right.addWidget(self.memo_list)

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
            self.transcript_area
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
            self.minutes_area
        )

        right.addWidget(self.memo_list)

        layout.addLayout(left, 2)
        layout.addLayout(right, 1)

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

        Path(
            "data/recordings"
        ).mkdir(
            parents=True,
            exist_ok=True
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        meeting_id = AppState.current_meeting_id

        if meeting_id is None:
            meeting_id = "unknown"

        self.current_file_path = (
            f"data/recordings/meeting_{meeting_id}_{timestamp}.wav"
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
            self.load_minutes()

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