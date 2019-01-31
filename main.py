import requests
from bs4 import BeautifulSoup
import csv


warning = "Без согласия Компании запрещено использовать (в том числе, извлекать из базы данных, собирать, записывать, систематизировать, передавать, распространять, копировать, воспроизводить) пользовательский контент (включая изображения, фотографии, описание товара в объявлении, сведения о товаре, контактные данные пользователя и иные элементы) и объекты исключительных прав Компании любыми способами и в любых целях, которые не предусмотрены настоящими Условиями (например, для создания базы данных или включения в уже имеющиеся базы данных, размещения в информационных системах третьих лиц, нерелевантных звонков пользователям), независимо от их объема и согласования с конкретными пользователями."
print("WARNING: ", warning)

file = open('avi-output.csv', mode='w')
fieldnames = ['Комнат', 'Площадь', 'Этаж', 'Высота', 'Цена']
writer = csv.DictWriter(file, fieldnames=fieldnames)
writer.writeheader()

url = input()
# https://www.avito.ru/moskovskaya_oblast_zheleznodorozhnyy/kvartiry/prodam
url += "/?f=549_5695-5696-5697-5698-5699-5700-5701-11018-11019-11020-11021.499_5254-5255" # &pmax=100000000&pmin=100000&s_trg=4"
i = 0
page_code = requests.get(url)

print(page_code)
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

        output_dict = {'Комнат': rooms, 'Площадь': area, 'Этаж': floor, 'Высота': height, 'Цена': price}
        writer.writerow(output_dict)

        print("{", end="")
        print(rooms, area, floor, height, price, sep=", ", end="")
        print("}", end="\n")

        i += 1
        if page_number % 10 == 0:
            pages += 10
print(i, page_code)
print("\nPress any button to quit.")
input()


