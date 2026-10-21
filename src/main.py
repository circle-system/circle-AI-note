import sys

from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from database.init_db import create_database

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

(BASE_DIR / "data").mkdir(
    exist_ok=True
)

def main():

    create_database()
    
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()