import json

# Define variables
input_file_path = './withcategory.json'  # Path to the input JSON file
output_file_path = './ready tools/data2.json'  # Path to the output JSON file
ai_tool_name = 'AI Tool'  # The field name to rename to 'name'

def update_fields(data):
    """Rename 'AI Tool' to 'name' and remove extra fields."""
    updated_data = []
    for item in data:
        # Rename 'AI Tool' to 'name'
        if ai_tool_name in item:
            item['name'] = item.pop(ai_tool_name)

        # Keep only the required fields
        item = {k: item[k] for k in ['name', 'description', 'pricing', 'image', 'directLink', 'category'] if k in item}
        
        updated_data.append(item)

    return updated_data

# Load the JSON file
with open(input_file_path, 'r') as file:
    data = json.load(file)

# Update the fields
updated_data = update_fields(data)

# Save the updated data back to a JSON file
with open(output_file_path, 'w') as file:
    json.dump(updated_data, file, indent=2)

print(f"Fields updated and extra fields removed. Updated data saved to '{output_file_path}'.")
