import whisper

# Explicitly load model
model = whisper.load_model("tiny")
print("✅ Model loaded successfully!")

# Explicit transcription of MP4 file
result = model.transcribe("7gc meeting notes mock.mp4")

# Explicit output
print("Transcription:", result["text"])

# Save output explicitly
with open("transcription.txt", "w") as file:
    file.write(result["text"])


