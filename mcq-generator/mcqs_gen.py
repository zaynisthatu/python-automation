import os
from pathlib import Path
from google import genai

# Initialize Gemini Client
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# Folder setup
LECTURE_FOLDER = Path("lectures")
MCQ_OUTPUT_FOLDER = Path("mcq_outputs")
MCQ_OUTPUT_FOLDER.mkdir(exist_ok=True)

# Gemini Prompt Template
def generate_mcqs_prompt(lecture_text):
    return f"""
Lecture content:
-----------------
{lecture_text}

Now your task is:

1. Analyze this lecture and identify all the **main topics** or **subtopics** inside it.
2. For each topic, generate **10 high-level, complicated MCQs** that:
   - Are **deeply connected** to the content.
   - Cover all **critical ideas** — nothing important should be left.
   - Are suitable for **advanced students** or **exams**.
3. Each MCQ should have:
   - Question
   - 4 options labeled A, B, C, D
   - Correct answer
   - Explanation that shows **why it is correct** and **from which part of the lecture** (quote or paraphrase).
4. Structure:

Topic: [Topic Title]
MCQ 1:
Q: ...
A. ...
B. ...
C. ...
D. ...
Correct Answer: B
Explanation: ...

[Repeat for 10 MCQs for each topic]

No intro or outro — just direct educational content.

Make sure the explanation is rich, connects back to the exact section of lecture, and is teacher-level clear.
"""

# Generate MCQs using Gemini
def generate_mcqs(lecture_text):
    prompt = generate_mcqs_prompt(lecture_text)
    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=[prompt]
    )
    return response.text

# Process lectures from lec_1.txt to lec_45.txt
for i in range(1, 46):
    lec_file = LECTURE_FOLDER / f"lec_{i}.txt"

    if not lec_file.exists():
        print(f"⚠️ File not found: {lec_file.name}, skipping.")
        continue

    print(f"📘 Processing {lec_file.name}...")
    lecture_text = lec_file.read_text(encoding="utf-8")

    try:
        mcqs_output = generate_mcqs(lecture_text)
        output_file = MCQ_OUTPUT_FOLDER / f"lec_{i}_mcqs.txt"
        output_file.write_text(mcqs_output, encoding="utf-8")
        print(f"✅ Saved: {output_file.resolve()}")
    except Exception as e:
        print(f"❌ Error processing {lec_file.name}: {e}")

print("🎉 All MCQ files generated.")
