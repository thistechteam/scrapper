import json

def remove_duplicates_by_name(data):
    seen_names = set()
    unique_data = []

    for item in data:
        name = item.get('AI Tool')

        if name and name not in seen_names:
            seen_names.add(name)
            unique_data.append(item)

    return unique_data

# Load the JSON file
with open('./ai_tools.json', 'r') as file:
    data = json.load(file)

# Remove duplicates based on the 'name' field
cleaned_data = remove_duplicates_by_name(data)

# Save the cleaned data back to a JSON file
with open('cleaned_file.json', 'w') as file:
    json.dump(cleaned_data, file, indent=2)

print("Duplicates removed based on 'name'. Cleaned data saved to 'cleaned_file.json'.")
