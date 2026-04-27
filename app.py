import json, os, time
from flask import Flask, request, jsonify, render_template
from scrapers.pinterest_scraper import scrape_pinterest
from scrapers.behance_scraper import scrape_behance
from scrapers.unsplash_scraper import scrape_unsplash

CACHE_FILE = 'cache/results.json'
CACHE_EXPIRY = 60 * 60  # 1小时缓存

app = Flask(__name__)

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_cache(data):
    os.makedirs('cache', exist_ok=True)
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', '')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    if not query:
        return jsonify([])

    cache = load_cache()
    cache_key = f"{query}_{page}"
    now = time.time()

    if cache_key in cache and now - cache[cache_key]['timestamp'] < CACHE_EXPIRY:
        return jsonify(cache[cache_key]['results'])

    results = []
    results += scrape_pinterest(query, page, per_page)
    results += scrape_behance(query, page, per_page)
    results += scrape_unsplash(query, page, per_page)

    cache[cache_key] = {'timestamp': now, 'results': results}
    save_cache(cache)

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
