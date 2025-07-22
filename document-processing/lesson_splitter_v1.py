import os

# Read the entire text
with open("full_book.txt", "r", encoding="utf-8") as f:
    content = f.read()

# Split by 'Lesson XX' pattern
import re
lectures = re.split(r'Lesson\s+(\d{1,2})', content)

# Create a directory for output
output_dir = "Split_Lectures"
os.makedirs(output_dir, exist_ok=True)

# Combine lesson number with content
for i in range(1, len(lectures), 2):
    lec_number = lectures[i].zfill(2)  # Pad numbers to 2 digits (e.g., 01, 02)
    lec_content = lectures[i+1].strip()

    # Optional: Extract first line as title
    title_line = lec_content.splitlines()[0].strip()
    safe_title = re.sub(r'[\\/*?:"<>|]', "", title_line)[:50]  # Remove unsafe characters and trim

    # File name
    filename = f"Lecture {lec_number} - {safe_title}.txt"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as out:
        out.write(f"Lesson {lec_number}\n{lec_content}")

print(f"Done! Lectures saved in folder: {output_dir}")