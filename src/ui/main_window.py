# src/ui/main_window.py

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QStackedWidget,
)

from ui.widgets.sidebar import Sidebar
from ui.pages.home_page import HomePage
from ui.pages.recording_page import RecordingPage
from ui.pages.settings_page import SettingsPage

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI Minutes")
        self.resize(1200, 800)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QHBoxLayout(central)

        self.sidebar = Sidebar()

        self.pages = QStackedWidget()

        self.home_page = HomePage()
        self.recording_page = RecordingPage()
        self.settings_page = SettingsPage()

        self.pages.addWidget(self.home_page)
        self.pages.addWidget(self.recording_page)
        self.pages.addWidget(self.settings_page)

        layout.addWidget(self.sidebar)
        layout.addWidget(self.pages)

        self.sidebar.home_clicked.connect(
            lambda: self.pages.setCurrentWidget(
                self.home_page
            )
        )

        self.sidebar.record_clicked.connect(
            lambda: self.pages.setCurrentWidget(
                self.recording_page
            )
        )

        self.sidebar.settings_clicked.connect(
            lambda: self.pages.setCurrentWidget(
                self.settings_page
            )
        )