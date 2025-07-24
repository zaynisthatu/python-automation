import os
from markdown_pdf import MarkdownPdf, Section

take_input = input("enter path: ").replace("\\", "/")

md_files = [f for f in os.listdir(take_input) if f.endswith('.md')]

if not md_files:
    print("Koi .md file nahi mili.")
else:
    for md_file in md_files:
        # Create a new PDF object for each file
        pdf = MarkdownPdf(toc_level=1)
        
        file_path = os.path.join(take_input, md_file)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        pdf.add_section(Section(content, toc=True))
        pdf_filename = md_file.replace('.md', '.pdf')
        pdf.save(os.path.join(take_input, pdf_filename))
        print(f"Converted {md_file} to {pdf_filename}")