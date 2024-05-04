from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import datetime

# Initialize WebDriver
driver = webdriver.Firefox()  # Use the browser driver of your choice

# Open the webpage
driver.get('https://aitoptools.com/ai-tools/writing-content/')

tool_list = []

while True:
    # Parse HTML and save to BeautifulSoup object
    soup = BeautifulSoup(driver.page_source, 'lxml')

    tools = soup.find_all('div', class_='custom-listing-content')

    for item in tools:
        name = item.h2.text.strip()
        purpose = item.p.text.strip()
        current_date = datetime.date.today().strftime('%Y-%m-%d')  # Get today's date
        tool_info = {"AI tool": name, "Purpose": purpose, "Scraped Date": current_date}
        tool_list.append(tool_info)

    try:
        # Try to click the 'next' button
        next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#loadMore")))
        next_button.click()
    except Exception as e:
        # If 'next' button is not found, we're on the last page
        print(e)
        break

driver.quit()

# Convert data to JSON string
json_data = json.dumps(tool_list)

# Write JSON data to file (replace with your desired filename)
with open('scraped_tools.json', 'w') as outfile:
  outfile.write(json_data)

print("Data scraped and saved to scraped_tools.json!")
