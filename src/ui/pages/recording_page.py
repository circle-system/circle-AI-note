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

        left.addStretch()

        left.addWidget(self.mic_label)

        left.addWidget(self.status_label)

        left.addWidget(self.timer_label)

        left.addWidget(self.file_label)

        left.addWidget(self.record_button)

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

        layout.addLayout(left, 2)
        layout.addLayout(right, 1)

        self.send_button.clicked.connect(
            self.save_memo
        )

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

        self.current_file_path = (
            f"data/recordings/{timestamp}.wav"
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
            self.memo_area.toPlainText()
            .strip()
        )

        if not memo_text:
            return

        timestamp = (
            self.timer_label.text()
        )

        display_text = (
            f"[{timestamp}] {memo_text}"
        )

        self.memo_list.addItem(
            display_text
        )

        self.memo_area.clear()

class Note(Base):

    __tablename__ = "notes"

    id = Column(
        Integer,
        primary_key=True
    )

    timestamp = Column(String)

    content = Column(Text)
