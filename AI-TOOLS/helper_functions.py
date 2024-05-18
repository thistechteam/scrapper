import requests
from bs4 import BeautifulSoup

def page_parser(url):
    # Retrieve text data (HTML content) from the URL
    html_text = requests.get(url).text

    # Parse the HTML content
    soup = BeautifulSoup(html_text, 'lxml')
    # print(soup.prettify())

    # Return the parsed content
    return soup
