import json
import pandas as pd

# Path to the JSON file
json_file_path = './data/final.json'  # Replace with your JSON file path
excel_file_path = './research/ai_tools.xlsx'  # Output Excel file path

# Load the JSON data
with open(json_file_path, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Convert JSON to Excel
df = pd.DataFrame(data)
df.to_excel(excel_file_path, index=False)

print(f"JSON data has been successfully converted to Excel and saved as '{excel_file_path}'.")
