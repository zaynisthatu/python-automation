import os
from pathlib import Path
import openai

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Input folder where text files are saved
input_folder = Path("audios")
output_folder = input_folder  # or you can define a new folder

# Loop through specific lecture files
for i in range(34, 46):  # lec_34.txt to lec_45.txt
    script_path = input_folder / f"lec_{i}.txt"

    if not script_path.is_file():
        print(f"File not found: {script_path}, skipping.")
        continue

    print(f"🔊 Processing {script_path.name}...")

    # Read the content of the script
    text = script_path.read_text(encoding="utf-8")

    # Generate speech using OpenAI TTS (gpt-4o / tts-1)
    response = openai.audio.speech.create(
        model="tts-1",  # or "tts-1-hd" for higher quality
        voice="nova",   # other options: alloy, echo, fable, onyx, shimmer
        input=text
    )

    # Save as MP3
    audio_path = script_path.with_suffix(".mp3")
    with open(audio_path, "wb") as f:
        f.write(response.content)

    print(f"✅ Saved audio to {audio_path}\n")

print("🎉 All TTS audio files created.")
