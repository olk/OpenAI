import os
from api import client

text_file_path = os.path.abspath("src/data/tts/speech.txt")

with open(text_file_path, "r") as file:
    text = file.read()

voice_model = "tts-1"
voice_characters = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

for voice_character in voice_characters:
    audio_file_path = os.path.abspath(
            "src/data/tts/speech_" + voice_character + ".mp3"
        )
    response = client.audio.speech.create(
            model=voice_model,
            voice=voice_character,
            input=text
        )

    response.stream_to_file(audio_file_path)
    print(f"Audio saved to {audio_file_path}")
