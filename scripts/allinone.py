import csv
import json
import google.generativeai as genai
import os
import sys
from dotenv import load_dotenv

load_dotenv()


# Define variables
input_file = './dirty tools/sraped.json'  # Path to input file
json_file_path = './working/ai_tools.json'  # Path where the JSON file will be saved
cleaned_file_path = './working/cleaned_file.json'  # Path for the cleaned JSON file
with_default_fields_file_path = './working/with_default_fields.json'  # Path for the JSON file with default fields
final_file_path = './ready tools/data4.json'  # Path for the final JSON file with categories
ai_tool_name = 'name'  # Field name in the CSV file that corresponds to the AI tool name

# Gemini API key and model setup
api_key = os.getenv('API_KEY')
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')

# Predefined categories
categories = ["Business & Productivity", "Tech & Development", "Design & Media", "Lifestyle & Growth", "Writing & Content"]

def csv_to_json(csv_file, json_file):
    """Convert CSV file to JSON."""
    with open(csv_file, mode='r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        data = [row for row in csv_reader]
    
    with open(json_file, mode='w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=2)

def remove_duplicates_by_name(data):
    """Remove duplicates based on the 'name' field."""
    seen_names = set()
    unique_data = []

    for item in data:
        name = item.get(ai_tool_name)

        if name and name not in seen_names:
            seen_names.add(name)
            unique_data.append(item)

    return unique_data

def get_category(name, description):
    """Get category from Gemini API."""
    prompt = f"""
    Given the following AI tool:
    Name: {name}
    Description: {description}
    
    Categorize this tool into one of the following categories:
    {', '.join(categories)}
    
    Return only the category name, nothing else.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating category for {name}: {e}")
        return ''  # Return empty string to indicate failure

def update_fields(data):
    """Add default fields, rename 'AI Tool' to 'name', set 'directLink' from 'URL' if it exists, and remove extra fields."""
    updated_data = []
    for item in data:
        # Add default fields
        item.setdefault('image', 'https://via.placeholder.com/150')
        item.setdefault('category', '')
        item.setdefault('pricing', '')
        item.setdefault('directLink', '')

        # Rename 'AI Tool' to 'name'
        if ai_tool_name in item:
            item['name'] = item.pop(ai_tool_name)

        # Set 'directLink' from 'URL' if it exists
        url_field = next((key for key in item if 'url' in key.lower()), None)
        if url_field and url_field in item:
            item['directLink'] = item.pop(url_field)

        # Keep only the required fields
        item = {k: item[k] for k in ['name', 'description', 'pricing', 'image', 'directLink', 'category'] if k in item}
        
        updated_data.append(item)

    return updated_data

# Check if input file is CSV or JSON and process accordingly
if input_file.lower().endswith('.csv'):
    # Convert CSV file to JSON
    csv_to_json(input_file, json_file_path)
    print(f"CSV file '{input_file}' has been converted to JSON file '{json_file_path}'.")

    # Load the JSON file and remove duplicates
    with open(json_file_path, 'r') as file:
        data = json.load(file)
else:
    # Directly load JSON file
    with open(input_file, 'r') as file:
        data = json.load(file)

# Remove duplicates
cleaned_data = remove_duplicates_by_name(data)
if not cleaned_data:
    print("No data after removing duplicates. Exiting.")
    sys.exit()

with open(cleaned_file_path, 'w') as file:
    json.dump(cleaned_data, file, indent=2)

print("Duplicates removed. Cleaned data saved to 'cleaned_file.json'.")

# Add default values, rename fields, and remove extra fields
updated_data = update_fields(cleaned_data)
if not updated_data:
    print("No data after updating fields. Exiting.")
    sys.exit()

# Save the data with default fields and updated structure
with open(with_default_fields_file_path, 'w') as file:
    json.dump(updated_data, file, indent=2)

print(f"Default fields added and fields renamed. Updated data saved to '{with_default_fields_file_path}'.")

# Update category field for each item
for item in updated_data:
    try:
        name = item['name']
        description = item['description']
        
        if item.get('category', '') == '':
            category = get_category(name, description)
            if category:
                item['category'] = category
            else:
                print(f"Skipping {name}: failed to categorize.")
        else:
            print(f"Skipping {name}: category already exists.")
    except Exception as e:
        print(f"Critical error with {name}: {e}")
        break  # Stop processing if a critical error occurs

# Save the updated data with categories
with open(final_file_path, 'w') as file:
    json.dump(updated_data, file, indent=2)

print("Processing complete. Updated data saved to 'data4.json'.")
