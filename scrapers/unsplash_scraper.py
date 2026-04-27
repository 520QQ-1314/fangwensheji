import requests

def scrape_unsplash(query, page=1, per_page=20):
    url = f'https://unsplash.com/napi/search/photos?query={query}&per_page={per_page}&page={page}'
    resp = requests.get(url).json()
    images = [{'url': item['urls']['small'], 'source': 'Unsplash'} for item in resp['results']]
    return images
