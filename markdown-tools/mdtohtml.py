
import os
import markdown

take_input = input("enter path: ").replace("\\", "/")

md_files = [f for f in os.listdir(take_input) if f.endswith('.md')]

if not md_files:
    print("Koi .md file nahi mili.")
else:
    for md_file in md_files:
        file_path = os.path.join(take_input, md_file)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Convert markdown to HTML
        html_content = markdown.markdown(content, extensions=['toc', 'tables', 'fenced_code'])
        
        # Create a complete HTML page
        full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{md_file.replace('.md', '')}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
        h1, h2, h3 {{ color: #333; }}
        code {{ background-color: #f4f4f4; padding: 2px 4px; border-radius: 3px; }}
        pre {{ background-color: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""
        
        html_filename = md_file.replace('.md', '.html')
        html_file_path = os.path.join(take_input, html_filename)
        
        with open(html_file_path, 'w', encoding='utf-8') as html_file:
            html_file.write(full_html)
        
        print(f"Converted {md_file} to {html_filename}")