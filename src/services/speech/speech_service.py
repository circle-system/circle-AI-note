import whisper


class SpeechService:

    def __init__(self):

        print("Whisper 読み込み中...")

        self.model = whisper.load_model(
            "base"
        )

        print("Whisper 準備完了")

    def transcribe_file(
        self,
        audio_file
    ):

        result = self.model.transcribe(
            audio_file,
            language="ja"
        )

        return result["text"]