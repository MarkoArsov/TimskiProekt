import requests
from bs4 import BeautifulSoup
import re

def scrape_page(id):
    obj = {}
    url = 'http://delta.mk/property/details/?id=' + id
    obj['Линк'] = url
    obj['Шифра'] = id
    response = requests.get(url)
    raw_html = response.text
    html = BeautifulSoup(raw_html, "html.parser")
    box = html.find_all(id="description")

    description_box = box[0].findChildren(recursive=False)[2]
    obj['Опис'] = description_box.text

    images = html.find(id="multiple_images").findChildren("img")
    obj['Слики'] = list(map(lambda img: img['src'], images))

    description_table = box[0]
    ul_tag = description_table.find('ul')
    for li in ul_tag.find_all('li'):
        key_value = li.text.split(':')
        key = key_value[0].strip()
        if li.find('strong'):
            value = li.find('strong').text.strip()
        else:
            value = key_value[1].strip() if len(key_value) > 1 else ''
        obj[key] = value

    price_section = html.find(id="search_query")
    price_text = price_section.find('h2').text.strip()
    price_value = re.search(r'\d+', price_text).group()
    obj['Цена'] = price_value

    return obj


def scrape_delta(**kwargs):
    data = []
    url = 'http://delta.mk/property/search/?t=0&o=0&p='
    i = 1
    while True:
        response = requests.get(url + str(i))
        raw_html = response.text
        html = BeautifulSoup(raw_html, "html.parser")
        estate_cards = html.find_all(class_="result")
        for card in estate_cards:
            link = card.findChildren(recursive=False)[1].findChildren(recursive=False)[-1].findChildren(recursive=False)[0]
            # print(link)
            match = re.search(r'id=(\w+)', link['href'])
            # print(match.group(1))
            if match:
                id = match.group(1)
                obj = scrape_page(id)
                data.append(obj)
        i += 1
        # REMOVE BREAK TO SCRAPE ALL PAGES
        if i == 3:
          break
    kwargs['ti'].xcom_push(key='scraped_data', value=data)

