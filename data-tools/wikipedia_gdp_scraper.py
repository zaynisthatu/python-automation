import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import time

def scrape_gdp_data():
    """
    Wikipedia se countries by GDP (nominal) ka table scrape karta hai
    """
    url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"
    
    try:
        print("Wikipedia page fetch kar rahe hain...")
        
        # Headers add karte hain taaki Wikipedia block na kare
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        print("Page successfully fetch ho gaya!")
        
        # BeautifulSoup se HTML parse karte hain
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Main GDP table dhundte hain (usually pehla table hota hai)
        tables = soup.find_all('table', {'class': 'wikitable'})
        
        if not tables:
            print("Error: GDP table nahi mila!")
            return None
            
        # Pehla table usually main GDP data hota hai
        main_table = tables[0]
        
        print("Table data extract kar rahe hain...")
        
        # Table headers extract karte hain
        headers = []
        header_row = main_table.find('tr')
        if header_row:
            for th in header_row.find_all(['th', 'td']):
                headers.append(th.get_text().strip())
        
        # Table rows extract karte hain
        rows_data = []
        for row in main_table.find_all('tr')[1:]:  # Pehla row header hai, skip karte hain
            cells = row.find_all(['td', 'th'])
            if len(cells) > 0:
                row_data = []
                for cell in cells:
                    # Text extract karte hain aur clean karte hain
                    text = cell.get_text().strip()
                    # References [1], [2] etc. remove karte hain
                    text = ''.join(char for char in text if not (char == '[' or char == ']' or char.isdigit() and text.count('[') > 0))
                    text = text.replace('\n', ' ').replace('\t', ' ')
                    # Multiple spaces ko single space bana dete hain
                    while '  ' in text:
                        text = text.replace('  ', ' ')
                    row_data.append(text.strip())
                
                if len(row_data) > 0 and any(cell.strip() for cell in row_data):
                    rows_data.append(row_data)
        
        print(f"Total {len(rows_data)} countries ka data extract ho gaya!")
        return headers, rows_data
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")
        return None
    except Exception as e:
        print(f"Error processing data: {e}")
        return None

def save_to_csv(headers, data, filename="gdp_data.csv"):
    """
    Data ko CSV file mein save karta hai
    """
    try:
        print(f"Data ko {filename} mein save kar rahe hain...")
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Headers write karte hain
            if headers:
                writer.writerow(headers)
            
            # Data rows write karte hain
            for row in data:
                writer.writerow(row)
        
        print(f"✅ Data successfully save ho gaya: {filename}")
        print(f"Total rows: {len(data)}")
        
    except Exception as e:
        print(f"Error saving to CSV: {e}")

def main():
    """
    Main function - scraping aur saving ka process
    """
    print("=== Wikipedia GDP Data Scraper ===")
    print("Countries by GDP (nominal) ka data scrape kar rahe hain...\n")
    
    # Data scrape karte hain
    result = scrape_gdp_data()
    
    if result:
        headers, data = result
        
        # CSV mein save karte hain
        save_to_csv(headers, data)
        
        print("\n=== Summary ===")
        print(f"Headers: {len(headers) if headers else 0}")
        print(f"Countries: {len(data)}")
        print("\nFirst few entries:")
        for i, row in enumerate(data[:5]):
            print(f"{i+1}. {row[0] if len(row) > 0 else 'N/A'}")
    else:
        print("❌ Data scraping failed!")

if __name__ == "__main__":
    main()