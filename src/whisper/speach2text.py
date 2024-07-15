import whisper

model_name = "medium"

try:
    model = whisper.load_model(model_name)
except Exception as e:
    print(f"Error loading model '{model_name}': {e}")
    exit(1)

audio_file_path = "src/whisper/audio/Winston_Church.ogg"

try:
    result = model.transcribe(audio_file_path)
    print("The text in video:")
    print(result["text"])
except Exception as e:
    print(f"Error transcribing file '{audio_file_path}': {e}")
