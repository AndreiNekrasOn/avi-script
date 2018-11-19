import requests
from bs4 import BeautifulSoup

url = input()
i = 0
page_code = requests.get(url)
soup = BeautifulSoup(page_code.content, "html.parser")
pages = len(soup.find("div", "pagination-pages").find_all('a'))
for page_number in range(1, pages):
    payload = "&p=" + str(page_number)
    page_code = requests.get(url, params=payload)

    soup = BeautifulSoup(page_code.content, "html.parser")

    apartments = soup.find_all("div", "item")
    # titles = soup.find_all(itemprop="name")
    for apartment in apartments:

        title = apartment.find(itemprop="name")
        title = title.text

        # number of rooms
        rooms = int(title[0]) if title[0].isdigit() else 0
        title = title[1:].split(', ')

        # area
        title = title[1:]
        title[0] = title[0].replace("м²", "")
        area = float(title[0])

        # floors
        title = title[1]
        title = title.split('/')
        floor = int(title[0])
        height = int(title[1].replace("эт.", ""))

        # price
        price_tag = apartment.find(itemprop="price").text
        price = price_tag.replace(" ", "")
        price = int(price.replace("₽", ""))

        print("{", end="")
        print(rooms, area, floor, height, price, sep=", ", end="")
        print("}", end="\n")
        i += 1
        if page_number % 10 == 0:
            pages += 10
print(i)


