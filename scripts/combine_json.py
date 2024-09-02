import json
import os

# Define paths
input_files = [
    './ready tools/data1.json',  # Add paths to your JSON files
    './ready tools/data2.json',  # Add paths to your JSON files
    './ready tools/data3.json',  # Add paths to your JSON files
    './ready tools/data4.json',  # Add paths to your JSON files
]
output_file = './data/final.json'  # Path for the final JSON file

def remove_duplicates(data):
    """Remove duplicates based on the 'name' field, keeping the one with non-empty 'directLink'."""
    unique_data = {}
    for item in data:
        name = item.get('name')
        if name:
            if name not in unique_data:
                unique_data[name] = item
            else:
                # If 'directLink' in the current item is not empty, replace the existing item
                if item.get('directLink'):
                    unique_data[name] = item
    return list(unique_data.values())

def merge_json_files(files):
    """Merge multiple JSON files into one and remove duplicates."""
    all_data = []
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            all_data.extend(data)

    # Remove duplicates
    unique_data = remove_duplicates(all_data)

    # Save merged and cleaned data
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(unique_data, f, indent=2)

    # Print the count of the final data
    print(f"Total unique items: {len(unique_data)}")

# Run the script
merge_json_files(input_files)
