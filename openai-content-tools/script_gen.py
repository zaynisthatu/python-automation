import os
from pathlib import Path
import openai

# Set your OpenAI API key (store it securely)
openai.api_key = os.getenv("OPENAI_API_KEY")

LECTURE_FOLDER = Path(".")
AUDIO_SCRIPT_FOLDER = Path(".")
# AUDIO_SCRIPT_FOLDER.mkdir(exist_ok=True)

def generate_audio_script(lecture_text):
    prompt = (
        "Is content ko aur zyada simple aur detail mein explain karo jaise YouTube ya teachers lesson video script ho.\n"
        "Simple tareeqay se explain karo jaise low-IQ level student ho.\n"
        "Summarize mat karo, expand karo, extra knowledge do, related topics bhi cover karo agar ho sakay.\n"
        "Mujhe iski audio banana hai, is liye directly lesson ka tone use karo.\n"
        "Koi intro ya outro nahi — sirf lesson ka material.\n\n"
        + lecture_text
    )

    response = openai.ChatCompletion.create(
        model="gpt-4-0613",  # Or use gpt-4o if available
        messages=[
            {"role": "system", "content": "You're a helpful teaching assistant."},
            {"role": "user", "content": prompt},
        ]
    )

    return response.choices[0].message.content.strip()

# Process each .txt file in the lectures folder
for lec_file in sorted(LECTURE_FOLDER.glob("*.txt")):
    print(f"Processing {lec_file.name}...")
    lecture_text = lec_file.read_text(encoding="utf-8")
    audio_script = generate_audio_script(lecture_text)
    out_file = AUDIO_SCRIPT_FOLDER / f"audio_script_{lec_file.stem}.txt"
    out_file.write_text(audio_script, encoding="utf-8")
    print(f"Saved: {out_file}")

print("✅ All audio scripts generated.")
