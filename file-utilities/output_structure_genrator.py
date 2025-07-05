import os

# --- Folder Structure ---
folders = [
    "prompts",
    "outputs/txt",
    "outputs/script",
    "outputs/audio"
]

files = {
    "api_key_text.txt": "# Paste your Text-to-Text Gemini API key here",
    "api_key_tts.txt": "# Paste your TTS Gemini API key here",
    "prompts/prompt1.txt": '''Mere paas "mgt502" book hai.
Main chahta hoon ke tum is book ke lectures (20-45) ko detail mein roman Urdu mein samjhao.
Har concept ko asaan lafzon mein breakdown karo, aise examples do jise real life ya aam zindagi se relate kiya ja sake.    
Jaise teacher class mein baith kar samjha raha ho, waise hi explain karo. 
Meri preparation exam ke liye hai is liye clear aur chipk janay wala explanation chahiye. 
Technical terms ko bhi simplify karo lekin asli naam zaroor mention karo.
Sirf lecture {lec_num} cover karo is part mein.''',

    "prompts/prompt2.txt": '''Is content ko or zyda simple aur detail mein explain karo jaise YouTube ya teachers lesson video script ho.
Simple tareeqay se explain karo jaise low-IQ level student ho.
Summarize mat karo, expand karo, extra knowledge do, related topics bhi cover karo agar ho sakay.
Mujhe iski audio banana hai, is liye directly lesson ka tone use karo.
Koi intro ya outro nahi — sirf lesson ka material.''',
}

for folder in folders:
    os.makedirs(folder, exist_ok=True)

for path, content in files.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Folder structure and placeholder files created.")
print("🔑 Now open 'api_key_text.txt' and 'api_key_tts.txt' to paste your API keys.")
