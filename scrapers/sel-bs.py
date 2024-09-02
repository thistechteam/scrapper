from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import datetime

# Initialize WebDriver
driver = webdriver.Firefox()  

# Open the webpage
driver.get('https://allthingsai.com/category/chatbots')

tool_list = []

while True:
    # Parse HTML and save to BeautifulSoup object
    soup = BeautifulSoup(driver.page_source, 'lxml')

    category = soup.find('div', class_='category-section-2')
    tools = soup.find_all('div', class_='vertical-centered w-dyn-itemcategory-section-2')
    

    for item in tools:
        name = item.h3.text.strip()
        purpose = item.p.text.strip()
        current_date = datetime.date.today().strftime('%Y-%m-%d')  
        pricing_per_month = item.find('div', class_='text-size-regular text-color-black')
        tool_info = {"AI tool": name, "Purpose": purpose, "Scraped Date": current_date, "monthly_price": pricing_per_month}
        tool_list.append(tool_info)

    try:
        # Try to click the 'next' button
        next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#w-tabs-0-data-w-pane-0 > div > div.w-pagination-wrapper")))
        next_button.click()
    except Exception as e:
        # If 'next' button is not found, we're on the last page
        print(e)
        break

driver.quit()

# Convert data to JSON string
json_data = json.dumps(tool_list)

# Write JSON data to file (recplace with your desired filename)
with open('chatbots.json', 'w') as outfile:
  outfile.write(json_data)

