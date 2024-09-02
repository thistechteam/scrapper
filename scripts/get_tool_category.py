import json
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Setup the Gemini API (replace with your actual API key)
api_key = os.getenv('API_KEY')
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')

# Predefined categories
categories = ["Business & Productivity", "Tech & Development", "Design & Media", "Lifestyle & Growth", "Writing & Content"]

def get_category(name, description):
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
        return None

# Load the JSON file
with open('./modified_file.json', 'r') as file:
    data = json.load(file)

# Process each item in the data
for item in data:
    try:
        name = item['name']
        description = item['description']
        
        # Check if category is an empty string
        if item.get('category', '') == '':
            # Get category from Gemini if it's an empty string
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

# Save the updated data back to a JSON file
with open('withcategory.json', 'w') as file:
    json.dump(data, file, indent=2)

print("Processing complete. Updated data saved to 'withcategory.json'")
