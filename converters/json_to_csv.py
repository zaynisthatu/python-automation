import json
import csv
import os
import sys

def json_to_csv(json_file_path, csv_file_path):
    """
    Convert JSON file to CSV format
    
    Args:
        json_file_path (str): Path to input JSON file
        csv_file_path (str): Path to output CSV file
    """
    try:
        # Read JSON file
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        
        # Check if data is empty
        if not data:
            print("JSON file is empty or contains no data.")
            return
        
        # Handle case where JSON contains a single object (convert to list)
        if isinstance(data, dict):
            data = [data]
        
        # Ensure data is a list of dictionaries
        if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
            print("Error: JSON must contain a list of objects or a single object.")
            return
        
        # Get all unique keys from all objects to create CSV headers
        all_keys = set()
        for item in data:
            all_keys.update(item.keys())
        
        # Sort keys for consistent column order
        fieldnames = sorted(all_keys)
        
        # Write to CSV file
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            
            # Write header
            writer.writeheader()
            
            # Write data rows
            for item in data:
                writer.writerow(item)
        
        print(f"✅ Successfully converted {json_file_path} to {csv_file_path}")
        print(f"📊 Converted {len(data)} records with {len(fieldnames)} columns")
        
    except FileNotFoundError:
        print(f"❌ Error: File '{json_file_path}' not found.")
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON format in '{json_file_path}': {e}")
    except PermissionError:
        print(f"❌ Error: Permission denied when accessing files.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def main():
    """Main function to handle command line arguments and file conversion"""
    
    # Default file paths
    default_json_file = "data.json"
    default_csv_file = "data.csv"
    
    # Check if custom file paths are provided as command line arguments
    if len(sys.argv) == 3:
        json_file = sys.argv[1]
        csv_file = sys.argv[2]
    elif len(sys.argv) == 2:
        json_file = sys.argv[1]
        csv_file = json_file.replace('.json', '.csv')
    else:
        json_file = default_json_file
        csv_file = default_csv_file
    
    print("🔄 JSON to CSV Converter")
    print("=" * 30)
    print(f"Input file: {json_file}")
    print(f"Output file: {csv_file}")
    print("=" * 30)
    
    # Check if input file exists
    if not os.path.exists(json_file):
        print(f"❌ Input file '{json_file}' does not exist.")
        print("\n📝 Creating sample data.json file...")
        
        # Create sample JSON file
        sample_data = [
            {"name": "Ali Khan", "age": 30, "city": "Karachi"},
            {"name": "Sara Malik", "age": 25, "city": "Lahore"},
            {"name": "Imran", "age": 40, "city": "Islamabad"}
        ]
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(sample_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Sample file '{json_file}' created successfully!")
        print("🔄 Now converting to CSV...")
    
    # Convert JSON to CSV
    json_to_csv(json_file, csv_file)

if __name__ == "__main__":
    main()