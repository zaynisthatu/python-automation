
import os
import re

def update_html_to_dark_theme(directory_path):
    html_files = [f for f in os.listdir(directory_path) if f.endswith('.html')]
    
    if not html_files:
        print("Koi .html file nahi mili.")
        return
    
    dark_theme_style = """    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 40px; 
            line-height: 1.6; 
            color: #ffffff;
            background-color: #111111;
        }
        h1, h2, h3 { color: #ffffff; }
        code { 
            background-color: #333333; 
            color: #ffffff;
            padding: 2px 4px; 
            border-radius: 3px; 
        }
        pre { 
            background-color: #222222; 
            color: #ffffff;
            padding: 10px; 
            border-radius: 5px; 
            overflow-x: auto; 
        }
        table { border-collapse: collapse; width: 100%; }
        th, td { 
            border: 1px solid #444444; 
            padding: 8px; 
            text-align: left; 
            color: #ffffff;
        }
        th { background-color: #333333; }
        a { color: #66ccff; }
        a:visited { color: #cc99ff; }
    </style>"""
    
    for html_file in html_files:
        file_path = os.path.join(directory_path, html_file)
        
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Replace the existing style section with dark theme
        updated_content = re.sub(
            r'<style>.*?</style>', 
            dark_theme_style, 
            content, 
            flags=re.DOTALL
        )
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)
        
        print(f"Updated {html_file} to dark theme")

# Usage
take_input = input("enter path: ").replace("\\", "/")
update_html_to_dark_theme(take_input)