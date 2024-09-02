import json

# Step 1: Read the JSON file
with open('./dirty tools/scraped_tools.json', 'r') as file:
    data = json.load(file)

# Step 2: Modify each object in the data
for item in data:
    # Replace field names
    if "AI tool" in item:
        item["name"] = item.pop("AI tool")
    if "Purpose" in item:
        item["description"] = item.pop("Purpose")
    
    # Remove "Scraped Date" if it exists
    if "Scraped Date" in item:
        del item["Scraped Date"]
    
    # Add new fields
    # item["pricing"] = ""
    # item["image"] = "https://via.placeholder.com/150"
    # item["directLink"] = ""
    # item["category"] = ""

# Step 3: Write the modified data back to a JSON file
with open('./dirty tools/sraped.json', 'w') as file:
    json.dump(data, file, indent=2)

print("JSON file has been modified and saved as modified_file.json")