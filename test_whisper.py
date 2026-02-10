import whisper

model = whisper.load_model("base")
result = model.transcribe("call.wav")

print(result["text"])
