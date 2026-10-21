# src/ui/widgets/sidebar.py

from PySide6.QtCore import Signal

from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
)


class Sidebar(QWidget):

    home_clicked = Signal()
    record_clicked = Signal()
    settings_clicked = Signal()

    def __init__(self):
        super().__init__()

        self.setFixedWidth(80)

        layout = QVBoxLayout(self)

        btn_home = QPushButton("🏠")
        btn_record = QPushButton("🎤")
        btn_setting = QPushButton("⚙")

        btn_home.clicked.connect(self.home_clicked)
        btn_record.clicked.connect(self.record_clicked)
        btn_setting.clicked.connect(self.settings_clicked)

        layout.addWidget(btn_home)
        layout.addWidget(btn_record)

        layout.addStretch()

        layout.addWidget(btn_setting)