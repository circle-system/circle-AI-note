# src/ui/pages/settings_page.py

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QListWidget,
    QInputDialog
)
from PySide6.QtCore import Qt
from database.repository import (
    save_settings,
    get_settings,
    add_person,
    get_persons,
    delete_person_by_name,
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

        layout.addWidget(
            QLabel("人物登録")
        )

        self.person_list = QListWidget()

        layout.addWidget(
            self.person_list
        )

        self.add_person_button = (
            QPushButton(
                "人物追加"
            )
        )

        self.add_person_button.clicked.connect(
            self.add_person
        )

        layout.addWidget(
            self.add_person_button
        )

        settings = get_settings()

        self.delete_person_button = QPushButton(
            "人物削除"
        )

        self.delete_person_button.clicked.connect(
            self.delete_person
        )

        layout.addWidget(
            self.delete_person_button
        )

        if settings:

            self.teams_url.setText(
                settings.teams_url or ""
            )

            self.format_box.setText(
                settings.file_format or "docx"
            )

        self.load_persons()

        layout.addStretch()

        version_label = QLabel(
            "Version 1.0.0"
        )

        version_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(
            version_label
        )

    def save_settings(self):

        print("設定保存開始")

        save_settings(
            self.teams_url.text(),
            self.format_box.text()
        )

        print("設定保存終了")

    def add_person(self):

        name, ok = (
            QInputDialog.getText(
                self,
                "人物追加",
                "名前"
            )
        )

        if ok and name:

            print("追加:", name)

            add_person(name)

            self.load_persons()

    def delete_person(self):

        item = self.person_list.currentItem()

        if not item:
            return

        delete_person_by_name(
            item.text()
        )

        self.load_persons()

    def load_persons(self):

        self.person_list.clear()

        for person in get_persons():

            self.person_list.addItem(
                person.name
            )
