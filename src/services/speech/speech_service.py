import whisper
import torch


class SpeechService:

    def __init__(self):

        self.model = None

    def load_model(self):

        if self.model is None:

            device = (
                "cuda"
                if torch.cuda.is_available()
                else "cpu"
            )

            print(
                f"使用デバイス: {device}"
            )

            print(
                "Whisper 読み込み中..."
            )

            self.model = whisper.load_model(
                "small",
                device=device
            )

            print(
                "Whisper 準備完了"
            )

    def transcribe_file(
        self,
        audio_file
    ):

        self.load_model()

        result = self.model.transcribe(
            audio_file,
            language="ja",
            task="transcribe",
            fp16=False,
            temperature=0
        )

        return result["text"]
