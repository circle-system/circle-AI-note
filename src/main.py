import sys
import ctypes

from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from database.init_db import create_database
from PySide6.QtGui import QIcon

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

(BASE_DIR / "data").mkdir(
    exist_ok=True
)

from pathlib import Path

Path("data").mkdir(
    exist_ok=True
)

Path("data/pdf").mkdir(
    parents=True,
    exist_ok=True
)

Path("data/minutes").mkdir(
    parents=True,
    exist_ok=True
)

Path("data/recordings").mkdir(
    parents=True,
    exist_ok=True
)

def main():

    create_database()

    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
        "AI.Minutes.1.0"
    )

    app = QApplication(sys.argv)

    window = MainWindow()

    ICON_PATH = (
        Path(__file__).resolve().parent
        / "icon.ico"
    )
    window.setWindowIcon(
        QIcon(str(ICON_PATH))
    )

    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()