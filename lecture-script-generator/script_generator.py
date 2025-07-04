import os
from pathlib import Path
from google import genai

# Set up folders
LECTURE_FOLDER = Path("lectures")
AUDIO_SCRIPT_FOLDER = Path("audio_scripts")
AUDIO_SCRIPT_FOLDER.mkdir(exist_ok=True)

# Initialize Gemini client (API key must be set in your environment)
client = genai.Client()

def generate_audio_script(lecture_text):
    prompt = (
        """Is content ko or zyda simple aur detail mein explain karo jaise YouTube ya teachers lesson video script ho.
Simple tareeqay se explain karo jaise low-IQ level student ho.
Summarize mat karo, expand karo, extra knowledge do, related topics bhi cover karo agar ho sakay.
Mujhe iski audio banana hai, is liye directly lesson ka tone use karo.
Koi intro ya outro nahi — sirf lesson ka material.:\n\n"""
        + lecture_text
    )
    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=[prompt],
    )
    return response.text

# Process each .txt file in the lectures folder
for lec_file in sorted(LECTURE_FOLDER.glob("*.txt")):
    print(f"Processing {lec_file.name}...")
    lecture_text = lec_file.read_text(encoding="utf-8")
    audio_script = generate_audio_script(lecture_text)
    out_file = AUDIO_SCRIPT_FOLDER / f"audio_script_{lec_file.stem}.txt"
    out_file.write_text(audio_script, encoding="utf-8")
    print(f"Saved: {out_file}")

print("All audio scripts generated.")
