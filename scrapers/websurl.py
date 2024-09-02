import requests
from bs4 import BeautifulSoup
import pandas as pd


def page_parser(url):
    # Retrieve text data (HTML content) from the URL
    html_text = requests.get(url).text

    # Parse the HTML content
    soup = BeautifulSoup(html_text, 'lxml')

    # Return the parsed content
    return soup


book_list = []
for i in range(1, 89):
    soup = page_parser('https://www.websurl.com/websites?page={i}')
    category_list = soup.find_all('div', class_='dec')

    iteration = 1
    for list in category_list:
        h2_tag = list.find('h2')
        h2_link = h2_tag.find('a')
        name = h2_link.text.strip()

        webpage_url = h2_link['href']
        soup_desc = page_parser(webpage_url)
        p_tag = soup_desc.find('p')
        description = p_tag.text.strip()

        h3_tag = list.find('h3')
        h3_link = h3_tag.find('a')
        url = h3_link['href']

        # name = list.h2.text.strip()
        # description = list.p.text.strip()
        # url = list.h3.find('a').get('href')
        book_list.append([name, description, url])
        iteration += 1

df = pd.DataFrame(book_list, columns=['AI Tool', 'Description', 'url'])
df.to_csv('ai_tools_from_websurl.csv')
