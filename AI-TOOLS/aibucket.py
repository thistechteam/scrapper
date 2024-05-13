import pandas as pd

from helper_functions import page_parser


book_list = []

soup = page_parser('https://www.aibucket.io/all-tools')

category_list = soup.find_all('div', class_='popular-products_text-wrapper')
for list in category_list:
    name_element = list.find('div', class_='card-heading side-margin')
    if name_element is not None:
        name = name_element.get_text(strip=True)
        # print(name)

    description_element = list.find(
        'div',
        class_='text-size-small height-1-5 w-richtext'
    )
    if description_element:
        description = description_element.get_text(strip=True)
        # print(description)
    link_element = list.find('div', class_='redirect-btn-wrapper')

    pricing_element = list.find(
        'div',
        class_='price-capsule'
    )
    if pricing_element:
        pricing = pricing_element.get_text(strip=True)
        print(pricing)

    url = ''
    if link_element:
        link = 'https://www.aibucket.io' + link_element.find('a')['href']
        link_soup = page_parser(link)
        url = link_soup.find(
            'a',
            class_='learn-more-link w-inline-block'
        )['href']
        # print(url)

    book_list.append([name, description, pricing, url])

df = pd.DataFrame(book_list, columns=['AI Tool', 'description', 'pricing', 'url'])
df.to_csv('ai_tools_from_aibucket.csv')
