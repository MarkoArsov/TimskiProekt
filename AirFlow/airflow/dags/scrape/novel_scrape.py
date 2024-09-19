import requests 
from bs4 import BeautifulSoup
import re

def scrape_page(id):
    obj = {}
    url = 'https://www.novelestate.com/estate_view.html?id=' + id
    obj['Линк'] = url
    obj['Шифра'] = id
    response = requests.get(url)
    raw_html = response.text
    html = BeautifulSoup(raw_html, "html.parser")
    box = html.find_all(class_="span box")
    info_box = box[0].findChildren(recursive=False)[1]
    description_box = info_box.findChildren(recursive=False)[1]
    obj['Опис'] = description_box.find(class_="estate-description").text

    images = info_box.find(class_="galery").findChildren("img")
    obj['Слики'] = list(map(lambda img: img['src'], images))

    description_table = description_box.findChildren(recursive=False)[1].findChildren(recursive=False)[0]
    properties = description_table.findChildren(recursive=False)
    for prop in properties:
      key = prop.findChildren(recursive=False)[0].text
      value = prop.findChildren(recursive=False)[1].text
      images = prop.findChildren(recursive=False)[1].find_all("img")
      if len(images) > 0:
        value = True
      obj[key] = value

    finance_table = description_box.findChildren(recursive=False)[3].findChildren(recursive=False)[0]
    finance_properties = finance_table.findChildren(recursive=False)
    for prop in finance_properties:
      key = prop.findChildren(recursive=False)[0].text
      value = prop.findChildren(recursive=False)[1].text
      images = prop.findChildren(recursive=False)[1].find_all("img")
      if len(images) > 0:
        value = True
      obj[key] = value

    return obj

def scrape_novel(**kwargs):
    data = []
    url = 'https://www.novelestate.com/estate_list.html?page='
    i = 1
    while True:
        response = requests.get(url + str(i))
        raw_html = response.text
        html = BeautifulSoup(raw_html, "html.parser")
        estate_cards = html.find_all(class_="estate-card")
        if len(estate_cards) == 0:
            break
        for card in estate_cards:
            link = card.findChildren(recursive=False)[-1].findChildren(recursive=False)[-1].findChildren(recursive=False)[0]
            match = re.search(r'id=(\w+)', link['href'])
            if match:
                id = match.group(1)
                obj = scrape_page(id)
                data.append(obj)
        i += 1
        # REMOVE BREAK TO SCRAPE ALL PAGES
        if i == 3:
          break
    kwargs['ti'].xcom_push(key='scraped_data', value=data)