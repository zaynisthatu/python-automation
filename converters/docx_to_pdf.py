import os
import comtypes.client
from pathlib import Path

def doc_to_pdf(source_path, dest_path):
    word = comtypes.client.CreateObject('Word.Application')
    word.Visible = False
    word.DisplayAlerts = 0

    success = []
    failed = []

    for root, _, files in os.walk(source_path):
        for file in files:
            if file.lower().endswith(('.doc', '.docx')):
                try:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, source_path)
                    pdf_path = os.path.join(dest_path, Path(rel_path).with_suffix('.pdf'))

                    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

                    doc = word.Documents.Open(full_path)
                    doc.SaveAs(pdf_path, FileFormat=17)  # 17 is PDF
                    doc.Close()
                    success.append(file)
                except Exception as e:
                    failed.append((file, str(e)))

    word.Quit()

    return success, failed

if __name__ == "__main__":
    print("=== DOC/DOCX to PDF Converter ===\n")

    source = input("🔹 Source directory: ").strip('" ')
    destination = input("🔹 Destination directory: ").strip('" ')

    print("\n⏳ Converting...\n")

    success, failed = doc_to_pdf(source, destination)

    total = len(success) + len(failed)
    print("\n=== ✅ Summary ===")
    print(f"📁 Total files found: {total}")
    print(f"✅ Successfully converted: {len(success)}")
    print(f"❌ Failed conversions: {len(failed)}\n")

    if failed:
        print("🛑 Failed files:")
        for fname, reason in failed:
            print(f" - {fname}: {reason}")
