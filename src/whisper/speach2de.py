import whisper
from api import client

model_name = "large"

try:
    model = whisper.load_model(model_name)
except Exception as e:
    print(f"Error loading model '{model_name}': {e}")
    exit(1)

audio_file_path = "src/whisper/audio/Winston_Church.ogg"
# audio_file_path = "src/whisper/audio/Lenin.ogg"

try:
    transcript = model.transcribe(audio_file_path)
    print("original:")
    print(transcript["text"])
except Exception as e:
    print(f"Error transcribing file '{audio_file_path}': {e}")

system_prompt = "You are an interpreter. Your role is to translate the text to German."
response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": transcript["text"]
                }
            ]
        )
print("translation:")
print(response.choices[0].message.content)
