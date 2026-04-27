import requests
from bs4 import BeautifulSoup

def scrape_pinterest(query, page=1, per_page=20):
    headers = {'User-Agent': 'Mozilla/5.0'}
    start = (page - 1) * per_page
    url = f'https://www.pinterest.com/search/pins/?q={query}&start={start}'
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')

    images = []
    for img_tag in soup.find_all('img'):
        src = img_tag.get('src')
        if src:
            images.append({'url': src, 'source': 'Pinterest'})
        if len(images) >= per_page:
            break
    return images
