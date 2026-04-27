import requests
from bs4 import BeautifulSoup

def scrape_behance(query, page=1, per_page=20):
    url = f'https://www.behance.net/search/projects?search={query}&page={page}'
    headers = {'User-Agent': 'Mozilla/5.0'}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')

    images = []
    for img_tag in soup.find_all('img'):
        src = img_tag.get('src')
        if src:
            images.append({'url': src, 'source': 'Behance'})
        if len(images) >= per_page:
            break
    return images
