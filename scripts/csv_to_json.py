import csv
import json

# Path to your CSV file
csv_file_path = './dirty tools/ai_tools.csv'
# Path where the JSON file will be saved
json_file_path = 'ai_tools.json'

# Read CSV file and convert to JSON
def csv_to_json(csv_file, json_file):
    with open(csv_file, mode='r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        # Convert CSV rows to a list of dictionaries
        data = [row for row in csv_reader]
    
    with open(json_file, mode='w', encoding='utf-8') as jsonfile:
        # Convert list of dictionaries to JSON and write to file
        json.dump(data, jsonfile, indent=2)

# Convert the CSV file to JSON
csv_to_json(csv_file_path, json_file_path)

print(f"CSV file '{csv_file_path}' has been converted to JSON file '{json_file_path}'.")
