from pathlib import Path
from pypdf import PdfReader

def pdf_to_text(pdf_path: Path) -> str:
    """Extracts all text from a PDF file."""
    reader = PdfReader(pdf_path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def convert_all_pdfs_in_dir(directory: Path):
    """Converts all PDF files in a directory to .txt files."""
    pdf_files = list(directory.glob("*.pdf"))

    if not pdf_files:
        print("⚠️ No PDF files found in this directory.")
        return

    for pdf_path in pdf_files:
        txt_path = pdf_path.with_suffix(".txt")
        try:
            text = pdf_to_text(pdf_path)
            txt_path.write_text(text, encoding="utf-8")
            print(f"✅ {pdf_path.name} → {txt_path.name}")
        except Exception as e:
            print(f"❌ Error converting {pdf_path.name}: {e}")

if __name__ == "__main__":
    current_dir = Path.cwd()
    print(f"📂 Working in: {current_dir}")
    convert_all_pdfs_in_dir(current_dir)
