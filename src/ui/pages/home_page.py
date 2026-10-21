# src/ui/pages/home_page.py

from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QGroupBox,
    QVBoxLayout,
    QPushButton,
    QListWidget,
    QInputDialog
)

from database.repository import (
    create_meeting,
    get_meetings
)

from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QListWidget
from PySide6.QtWidgets import QInputDialog


class HomePage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QHBoxLayout(self)

        left = QGroupBox("新規会議")
        left_layout = QVBoxLayout(left)

        self.create_button = QPushButton(
            "＋ 新規作成"
        )

        left_layout.addWidget(
            self.create_button
        )

        left_layout.addStretch()

        right = QGroupBox("会議一覧")
        right_layout = QVBoxLayout(right)

        self.meeting_list = QListWidget()

        right_layout.addWidget(
            self.meeting_list
        )

        layout.addWidget(left)
        layout.addWidget(right)

        self.create_button.clicked.connect(
            self.create_new_meeting
        )

        self.load_meetings()

    def create_new_meeting(self):
        title, ok = QInputDialog.getText(
            self,
            "新規会議",
            "会議名を入力してください"
        )

        if ok and title:

            create_meeting(title)

            self.load_meetings()

    def load_meetings(self):

        self.meeting_list.clear()

        meetings = get_meetings()

        for meeting in meetings:

            self.meeting_list.addItem(
                meeting.title
            )

    def load_meetings(self):

        self.meeting_list.clear()

        meetings = get_meetings()

        for meeting in meetings:

            self.meeting_list.addItem(
                meeting.title
            )