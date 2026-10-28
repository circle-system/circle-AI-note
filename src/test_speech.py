from pathlib import Path

from services.speech.speech_service import (
    SpeechService
)

wav_files = list(
    Path("data/recordings").glob("*.wav")
)

wav_files.sort(
    key=lambda x: x.stat().st_mtime,
    reverse=True
)

audio_file = str(wav_files[0])

print(
    "使用ファイル:",
    audio_file
)

service = SpeechService()

result = service.transcribe_file(
    audio_file
)

print()
print("=====文字起こし結果=====")
print(result)