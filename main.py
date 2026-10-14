import speech_recognition as sr

def recognize_speech_continuous():
    #音声認識初期化
    recognizer = sr.Recognizer()

    #マイクからの入力を使う
    with sr.Microphone() as source:
        print("録音開始、話してください...")

        #環境ノイズ調整
        recognizer.adjust_for_ambient_noise(source)

        while True:
            try:
                #ユーザの声を記録
                audio = recognizer.listen(source)

                #GoogleのSpeechAPIを使用してテキスト化
                text = recognizer.recognize_google(audio, language="ja-JP")
                print("認識したテキスト: " + text)

                #"終わり"という単語で終了
                if "終わり" in text or "おわり" in text:
                    print("プログラム終了")
                    break
            except sr.UnknownValueError:
                print("音声認識できない")
            except sr.RequestError:
                print("リクエストに失敗、インターネット接続の確認をしてください")

if __name__ == "__main__":
    recognize_speech_continuous()