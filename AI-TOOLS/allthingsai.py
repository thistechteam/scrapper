import pandas as pd
import time

from helper_functions import page_parser


# Initialize an empty list `book_list` to store scraped data
book_list = []

# Parse the AllThingsAI Marketplace homepage using the `page_parser` function
soup = page_parser('https://allthingsai.com/marketplace')


def scrape_all_pages(base_url, page_num=1):
    """
    This function scrapes data from all pages of the AllThingsAI Marketplace.

    Args:
        base_url: The base URL of the marketplace
            (https://allthingsai.com/marketplace).
        page_num: The current page number (starts at 1).

    Returns:
        A list containing all scraped data.
    """
    book_list = []
    url = f"{base_url}?22022970_page={page_num}"
    soup = page_parser(url)

    iteration = 0

    # Identify all the div element containing all AI tool cards using class
    # names
    categories = soup.find_all('div', class_='card-border')
    for card in categories:
        # Finds the ai tool name div element
        name_element = card.find(
            'h3',
            class_='text-style-1lines heading-style-h5'
        )
        if name_element:
            # Extracts the name (text)
            name = name_element.get_text(strip=True)
            print(f'========= {name} ==========')

        # Find the ai tool category's div element
        category_element = card.find(
            'div',
            class_='text-size-small'
        )
        if category_element:
            # Extract the category
            category = category_element.get_text(strip=True)
            print(f"{name} is in the category `{category}`")

        # # Find the tool's subcategory div element
        # subcategory_element = card.find(
        #     'div',
        #     class_='text-size-tiny'
        # )
        # if subcategory_element:
        #     # Extracts the subcategory
        #     subcategory = subcategory_element.get_text(strip=True)
        #     print(f"and the subcategory `{subcategory}`.")

        # Find the pricing div element
        pricing_element = card.find(
            'div',
            class_='text-size-regular text-color-black'
        )
        # If the pricing element exists i.e the price is found
        if pricing_element:
            # Extract the price
            price = pricing_element.get_text(strip=True)
            # Initialize pricing with the string 'PAID'
            pricing = 'PAID'
            print(pricing, price)
        # Otherwise
        else:
            # There is no price
            price = None
            # Initialize pricing with the string 'FREE'
            pricing = 'FREE'
            print(pricing)

        # Find the link element for the tool details page
        link_element = card.find('a')
        if link_element:
            # Constructs the complete URL
            link = 'https://allthingsai.com' + link_element['href']

        # Parse the tool details page using `page_parser`
        link_soup = page_parser(link)

        # Find the div element containing the tool description
        description_element = link_soup.find(
            'div',
            class_='tools-rich-text w-richtext'
        )
        if description_element:
            # Extract the description text
            description = description_element.get_text(
                strip=True,
                separator=" "
            )
            print(f'Description: {description}')

        # Find the div element containing the tool link
        tool_link_tag = link_soup.find('div', class_='tool-hero-left')
        if tool_link_tag:
            # Find the tool link tag and extract its URL if
            url = tool_link_tag.find(
                'a',
                class_='button is-icon cms-link w-inline-block'
            )['href']
            print(f'To visit and learn more about {name} go to 👉: {url}')

        print()

        # Append all scraped data for a tool in the list `book_list`
        book_list.append(
            [name, category, description, pricing, price, url]
        )

        iteration += 1
        # if iteration:
        if iteration == 36:
            print("🔼")
            # Pause the script for a minute to avoide exceeding max retries
            time.sleep(60)
        print("🚨🚨🚨🚨🚨")

    # Check for "Load More" link and continue scraping if available
    next_page_link = soup.find(
        'a',
        class_='w-pagination-next button is-alternate'
    )
    if next_page_link:
        book_list.extend(scrape_all_pages(base_url, page_num + 1))

    return book_list


def main():
    """
    This function executes the script to scrape and save AI tool data from
    all pages.
    """
    all_tools_data = scrape_all_pages('https://allthingsai.com/marketplace')
    df = pd.DataFrame(
        all_tools_data,
        columns=[
            'AI Tool',
            'category',
            'description',
            'pricing',
            'price',
            'url'
        ]
    )
    df.to_csv('ai_tools_from_allthingsai_main.csv')


if __name__ == "__main__":
    main()
