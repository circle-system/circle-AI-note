import sounddevice as sd
from PySide6.QtWidgets import QMessageBox
import numpy as np
import wave

class Recorder:

    def __init__(self):

        self.sample_rate = 16000

        self.channels = 1

        self.recording_data = []

        self.stream = None

        self.filepath = None

    def callback(
        self,
        indata,
        frames,
        time,
        status
    ):

        

        self.recording_data.append(
            indata.copy()
        )

    def start_recording(
        self,
        filepath
    ):

        self.filepath = filepath

        self.recording_data = []

        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            callback=self.callback
        )

        self.stream.start()

    def stop_recording(self):

        self.stream.stop()

        self.stream.close()

        if len(self.recording_data) == 0:

            raise RuntimeError(
                "録音データ数0"
            )
        import numpy as np

        audio = np.concatenate(
            self.recording_data,
            axis=0
        )

        audio = (
            audio * 32767
        ).astype(np.int16)

        with wave.open(
            self.filepath,
            "wb"
        ) as wav_file:

            wav_file.setnchannels(
                self.channels
            )

            wav_file.setsampwidth(
                2
            )

            wav_file.setframerate(
                self.sample_rate
            )

            wav_file.writeframes(
                audio.tobytes()
            )

        return self.filepath