# Python Automation Tools

Python scripts I built to automate my study and content workflow: turning lecture material into scripts, MCQs and audio, converting Markdown to HTML/PDF, and organizing files.

| Folder | What it does |
|---|---|
| `lecture-script-generator/` | Reads lecture text files and uses Gemini to write explanation scripts for audio or video lessons |
| `mcq-generator/` | Generates exam MCQs from lecture files with Gemini; includes Markdown-to-HTML conversion and a project folder creator |
| `tts-converters/` | Batch text-to-speech: `tts.py` (Gemini TTS, with retries and logging) and `robust_gtts_converter.py` (gTTS) |
| `openai-content-tools/` | OpenAI versions: script generation, text-to-speech, and a simple chat loop |
| `transcript-cleaner/` | Cleans `.vtt` caption files (timestamps and metadata removed) and converts the text with Gemini |
| `document-processing/` | Splits a large text into lesson files by heading (two early versions and a newer one); PDF to text; splitter for GPT/Gemini output |
| `markdown-tools/` | Markdown to HTML, Markdown to PDF, dark-theme HTML updater, batch file namer |
| `converters/` | DOCX to PDF (Word automation, Windows), CSV to styled PDF, JSON to CSV |
| `data-tools/` | Scrapes the Wikipedia "countries by GDP (nominal)" table into a CSV |
| `file-utilities/` | Sorts files by extension, numbered renamer, output folder generator, zip and unzip, duplicate file finder (hash based), empty folder remover, bulk file mover, prefix remover |

## Setup
Python 3.10 or newer.
```
pip install google-genai openai gtts pypdf markdown markdown-pdf requests beautifulsoup4 pandas reportlab comtypes
```
API keys are read from environment variables, never from the code:
```
set GEMINI_API_KEY=your-key       (Windows)
export GEMINI_API_KEY=your-key    (Linux/macOS)
set OPENAI_API_KEY=your-key
```
Scripts read from folders next to where you run them (`lectures/`, `audios/`, `tts_input/`). Change the folder names at the top of each file if needed.



| Period | What was built |
|---|---|
| Sep to Dec 2024 | File utilities: duplicate finder, file mover, empty-folder remover |
| Apr to Jun 2025 | Zip and unzip tools, DOCX to PDF, file organizer, prefix remover |
| Jul 2025 | Lesson splitters and PDF to text, folder/prompt scaffold generator, script generators (Gemini and OpenAI), TTS converters, MCQ generator, Markdown tools, CSV/JSON converters, Wikipedia GDP scraper |
| Sep 2025 | Newer lecture splitter and GPT/Gemini output splitter |
| Jan 2026 | VTT transcript cleaner |
