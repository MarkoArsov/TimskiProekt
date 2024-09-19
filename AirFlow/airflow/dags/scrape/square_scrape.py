import requests
from bs4 import BeautifulSoup
import re

def scrape_square(**kwargs):
    data = []
    url = 'https://www.square.mk/prodazba-na-stanovi-vo-skopje/?jsf=jet-engine&pagenum='
    i = 1
    while True:
        response = requests.get(url + str(i))
        raw_html = response.text
        html = BeautifulSoup(raw_html, "html.parser")

        estate_cards = html.find_all(class_="e-con-inner")

        if len(estate_cards) == 0:
            break

        for card in estate_cards:
            heading_title = card.find('h2', class_='elementor-heading-title')
            if heading_title and heading_title.find('a'):
                link = heading_title.find('a')['href']
                obj = scrape_square_page(link)
                data.append(obj)

        i += 1
        # REMOVE BREAK TO SCRAPE ALL PAGES
        if i == 3:
            break

    kwargs['ti'].xcom_push(key='scraped_data', value=data)


def scrape_square_page(url):
    obj = {}
    response = requests.get(url)
    html = BeautifulSoup(response.text, 'html.parser')

    boxes = html.find_all(class_="elementor-widget-container")

    images_wrapper = html.find(class_="elementor-image-carousel swiper-wrapper")
    images = images_wrapper.find_all("img")

    for i, box in enumerate(boxes):
        if "Цена" in box.get_text(strip=True):
            obj["Цена"] = boxes[i + 1].get_text(strip=True) if i + 1 < len(boxes) else None
        if "Провизија" in box.get_text(strip=True):
            obj["Провизија"] = boxes[i + 1].get_text(strip=True) if i + 1 < len(boxes) else None

    info_start_index = None
    for i, box in enumerate(boxes):
        if "Информации" in box.get_text(strip=True):
            info_start_index = i
            break

    end_phrase = "Дали сте заинтересирани за овој стан?"
    info_end_index = None
    for i in range(len(boxes) - 1, -1, -1):
        if end_phrase in boxes[i].get_text(strip=True):
            info_end_index = i
            break

    if info_start_index is not None and info_end_index is not None:
        boxes = boxes[info_start_index + 1:info_end_index - 1]
    elif info_start_index is not None:
        boxes = boxes[info_start_index + 1:-1]
    elif info_end_index is not None:
        boxes = boxes[:info_end_index]

    for i in range(0, len(boxes), 2):
        key = boxes[i].get_text(strip=True)
        value = boxes[i + 1].get_text(strip=True) if i + 1 < len(boxes) else None
        obj[key] = value

    match = re.search(r'/(\d+)/$', url)
    if match:
        obj["Шифра"] = match.group(1)

    obj['Слики'] = [img['data-src'] for img in images]

    return obj