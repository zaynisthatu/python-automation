import google.generativeai as genai
import re
import os

# Set the GEMINI_API_KEY environment variable before running
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def clean_and_convert(vtt_content):
    # Timestamps aur metadata hatane ke liye regex
    clean_text = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}.*', '', vtt_content)
    clean_text = re.sub(r'WEBVTT|Kind:.*|Language:.*|align:.*|position:.*', '', clean_text)
    
    # Extra khali lines hatana
    lines = [line.strip() for line in clean_text.split('\n') if line.strip()]
    final_input = "\n".join(lines)

    # 2. Naya model naam (gemini-2.5-flash stable hai)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""
    Convert the following Urdu text into Roman Urdu. 
    Only provide the Roman Urdu translation. 
    No timestamps, no extra notes.

    Urdu Text:
    {final_input}
    """
    
    response = model.generate_content(prompt)
    return response.text

# 3. File check karna aur read karna
file_name = "MGT504_Lecture27 [qlNpLIgGobE].ur.vtt"

if os.path.exists(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        vtt_data = file.read()
    
    print("File mil gayi, conversion shuru ho rahi hai...")
    
    try:
        roman_urdu_text = clean_and_convert(vtt_data)
        
        # Result save karna
        with open("Converted_Roman_Urdu.txt", "w", encoding="utf-8") as f:
            f.write(roman_urdu_text)
        print("Mubarak ho! Conversion mukammal ho gayi. 'Converted_Roman_Urdu.txt' check karein.")
        
    except Exception as e:
        print(f"API Error: {e}")
else:
    print(f"Error: '{file_name}' file is folder mein nahi mili jahan aapka script hai.")