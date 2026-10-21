# src/ui/pages/settings_page.py

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
)

from database.repository import (
    save_settings,
    get_settings
)


class SettingsPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        layout.addWidget(
            QLabel("Teams URL")
        )

        self.teams_url = QLineEdit()

        layout.addWidget(
            self.teams_url
        )

        layout.addWidget(
            QLabel("SharePoint URL")
        )

        self.sharepoint_url = QLineEdit()

        layout.addWidget(
            self.sharepoint_url
        )

        layout.addWidget(
            QLabel("保存形式")
        )

        self.format_box = QLineEdit("docx")

        layout.addWidget(
            self.format_box
        )

        layout.addStretch()

        # 先に生成
        self.save_button = QPushButton(
            "保存"
        )

        # 後でconnect
        self.save_button.clicked.connect(
            self.save_settings
        )

        layout.addWidget(
            self.save_button
        )

    def save_settings(self):
        pass