import requests
from bs4 import BeautifulSoup
import pandas as pd



book_list =[]
for i in range(1,33):
    html_text = requests.get(f'https://aidemos.com/?page={i}').text
    soup = BeautifulSoup(html_text, 'lxml')

    category_list = soup.find_all('li', class_='w-full max-sm:w-[85%] mx-auto')

   
    iteration = 1
    for list in category_list:
        name = list.h2.text.strip()
        description = list.p.text.strip()
        book_list.append([name,description])
        iteration +=1


df = pd.DataFrame(book_list, columns = ['AI Tool','description'])
df.to_csv('ai_tools.csv')