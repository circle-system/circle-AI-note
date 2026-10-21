from PySide6.QtCore import QObject
from services.recording.recorder import Recorder


class RecordWorker(QObject):

    def __init__(self):

        super().__init__()

        self.recorder = Recorder()