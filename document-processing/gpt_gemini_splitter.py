import os
import re

# --- Configuration ---
INPUT_FILE = "full_book.txt"
OUTPUT_DIR = "Split_Lectures"

# --- Main Script ---
try:
    # Read the entire content of the book
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Split the content by the "Lecture No. XX" pattern.
    # This pattern looks for the literal text "Lecture No. ", followed by one or two digits.
    # The parentheses around (\d+) capture the lecture number itself.
    lectures = re.split(r'Lecture No\.\s+(\d+)', content)

    # Create the output directory if it doesn't already exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # The first item in the 'lectures' list is the text before Lecture 1 (e.g., Table of Contents), so we skip it.
    # We then loop through the list two items at a time: one for the number, one for the content.
    for i in range(1, len(lectures), 2):
        lec_number = lectures[i].zfill(2)  # Pad number to 2 digits (e.g., "1" -> "01")
        lec_content = lectures[i+1].strip()

        # Extract the first line of the lecture content to use as a title
        # It handles cases where a lecture might start with a blank line.
        title_line = "Untitled"
        for line in lec_content.splitlines():
            if line.strip():
                title_line = line.strip()
                break
        
        # Remove characters that are illegal in filenames and trim the length
        safe_title = re.sub(r'[\\/*?:"<>|]', "", title_line)[:50]

        # Create the final filename and path
        filename = f"Lecture {lec_number} - {safe_title}.txt"
        filepath = os.path.join(OUTPUT_DIR, filename)

        # Write the content to the new file, adding the header back in
        with open(filepath, "w", encoding="utf-8") as out:
            out.write(f"Lecture No. {lec_number}\n\n{lec_content}")

    print(f"Success! {len(lectures) // 2} lectures have been saved in the '{OUTPUT_DIR}' folder.")

except FileNotFoundError:
    print(f"Error: The file '{INPUT_FILE}' was not found. Please make sure it's in the same directory as the script.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")