import pandas as pd
import json

# Path to the Excel file
excel_file_path = 'final_data.xlsx'  # Replace with your Excel file path
json_file_path = 'final_data_converted.json'  # Output JSON file path

# Load the Excel data
df = pd.read_excel(excel_file_path)

# Convert DataFrame to JSON
data = df.to_dict(orient='records')

# Save JSON to file
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, indent=2)

print(f"Excel data has been successfully converted to JSON and saved as '{json_file_path}'.")
