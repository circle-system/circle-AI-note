import sounddevice as sd
import soundfile as sf


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

        import numpy as np

        audio = np.concatenate(
            self.recording_data,
            axis=0
        )

        sf.write(
            self.filepath,
            audio,
            self.sample_rate
        )

        return self.filepath