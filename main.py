import requests
from bs4 import BeautifulSoup
import json


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'}
pages = []
for page_count in range(1, 11):
    page = requests.get(f'https://rezka.ag/page/{page_count}', headers=headers).text
    soup = BeautifulSoup(page, 'html.parser')
    elements = soup.find(class_='b-content__inline_items').find_all_next(class_='b-content__inline_item-link')
    json_data = {f"page_{page_count}": []}
    for element in elements:
        title = element.find_next('a').text
        link = element.find_next('a').get('href')
        text = element.find_next('div').text.split(', ')
        if len(text) == 3:
            json_data[f"page_{page_count}"].append({"title": title, "year": text[0].rstrip(' - ...'),
                                        "country": text[1], "genre": text[2], "link": link})
        else:
            json_data[f"page_{page_count}"].append({"title": title, "year": text[0].rstrip(' - ...'),
                                        "genre": text[1], "link": link})
    pages.append(json_data)
with open('movies.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(pages, ensure_ascii=False))
