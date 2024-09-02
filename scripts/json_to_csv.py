import json
import csv

# Path to the JSON file
json_file_path = 'final_data.json'  # Replace with your JSON file path
csv_file_path = 'final_data.csv'  # Output CSV file path

# Load the JSON data
with open(json_file_path, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Convert JSON to CSV
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    if len(data) > 0:
        fieldnames = data[0].keys()  # Get column names from the keys of the first item
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(data)

print(f"JSON data has been successfully converted to CSV and saved as '{csv_file_path}'.")
