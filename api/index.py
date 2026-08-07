import re
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ==========================================
# CONSTANTS & HEADERS (From Durnel JS)
# ==========================================
TMDB_API_KEY = '307b7b8ef035c6aa336900aef4e203bd'
CTG_API_BASE = 'https://cockpit.103.109.92.178.nip.io/api/v1'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
    'Accept': 'application/json',
    'Referer': 'https://ctgmovies.com/',
    'Origin': 'https://ctgmovies.com',
}

# ==========================================
# 1. SETUP PAGE UI (Premium Multi-Provider)
# ==========================================
SETUP_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JaatOG Eclipsia Setup</title>
    <style>
        body { background-color: #0b0c10; color: #c5c6c7; font-family: -apple-system, sans-serif; margin: 0; padding: 20px; padding-bottom: 100px; }
        .header { text-align: center; margin-bottom: 30px; }
        .header h1 { color: #ffffff; font-weight: 400; letter-spacing: 2px;}
        .provider-card { background-color: #14151a; border: 1px solid #2a2b32; border-radius: 12px; padding: 20px; margin-bottom: 15px; display: flex; align-items: center; justify-content: space-between; }
        .provider-info h3 { margin: 0 0 5px 0; color: #ffffff; font-size: 16px; letter-spacing: 1px;}
        .provider-info p { margin: 0; font-size: 13px; color: #888; }
        .switch { position: relative; display: inline-block; width: 50px; height: 26px; }
        .switch input { opacity: 0; width: 0; height: 0; }
        .slider { position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background-color: #2a2b32; transition: .4s; border-radius: 34px; }
        .slider:before { position: absolute; content: ""; height: 18px; width: 18px; left: 4px; bottom: 4px; background-color: #888; transition: .4s; border-radius: 50%; }
        input:checked + .slider { background-color: #4a6b8c; }
        input:checked + .slider:before { transform: translateX(24px); background-color: #ffffff; }
        .bottom-bar { position: fixed; bottom: 0; left: 0; right: 0; background-color: #0b0c10; border-top: 1px solid #2a2b32; padding: 20px; text-align: center; }
        .install-btn { background-color: #2a2b32; color: white; border: none; padding: 15px 30px; border-radius: 25px; font-size: 16px; width: 100%; max-width: 400px; cursor: pointer; transition: 0.3s; }
        .install-btn:hover { background-color: #3a3b42; }
    </style>
</head>
<body>
    <div class="header">
        <h1>eclipsia jaatog</h1>
        <p>Select your Providers</p>
    </div>

    <!-- Provider 1: Durnel (Real Engine) -->
    <div class="provider-card">
        <div class="provider-info">
            <h3>Durnel (Real Logic) .</h3>
            <p>Provider: CTGMovies | Multi-Lang</p>
        </div>
        <label class="switch">
            <input type="checkbox" class="prov-checkbox" value="durnel" checked>
            <span class="slider"></span>
        </label>
    </div>

    <!-- Provider 2: VixSrc -->
    <div class="provider-card">
        <div class="provider-info">
            <h3>VixSrc (Pending) .</h3>
            <p>Provider: VixSrc | English, Italian</p>
        </div>
        <label class="switch">
            <input type="checkbox" class="prov-checkbox" value="vixsrc" checked>
            <span class="slider"></span>
        </label>
    </div>

    <!-- Provider 3: Lyrin -->
    <div class="provider-card">
        <div class="provider-info">
            <h3>Lyrin (Pending) .</h3>
            <p>Provider: BanglaPlex | English, Hindi</p>
        </div>
        <label class="switch">
            <input type="checkbox" class="prov-checkbox" value="lyrin" checked>
            <span class="slider"></span>
        </label>
    </div>

    <div class="bottom-bar">
        <button class="install-btn" onclick="generateManifest()">Generate manifest URL</button>
    </div>

    <script>
        function generateManifest() {
            const checkboxes = document.querySelectorAll('.prov-checkbox:checked');
            let selectedProviders = Array.from(checkboxes).map(cb => cb.value);
            
            let config = selectedProviders.length > 0 ? selectedProviders.join(',') : 'none';
            let installLink = `stremio://${window.location.host}/${config}/manifest.json`;
            window.location.href = installLink;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return SETUP_HTML

# ==========================================
# 2. MANIFEST GENERATION
# ==========================================
@app.route('/<config>/manifest.json')
@app.route('/manifest.json')
def get_manifest(config="all"):
    return jsonify({
        "id": "org.jaatog.eclipsia.full",
        "version": "4.0.0",
        "name": "JaatOG Eclipsia VIP",
        "description": "Multi-provider streaming addon",
        "resources": ["stream"],
        "types": ["movie", "series"],
        "idPrefixes": ["tt"],
        "behaviorHints": {
            "configurable": True,
            "configurationRequired": True
        },
        "catalogs": []
    })

# ==========================================
# HELPER FUNCTIONS FOR DURNEL
# ==========================================
def clean_title(title):
    return re.sub(r'[^a-z0-9]+', ' ', str(title).lower()).strip()

def get_tmdb_info(imdb_id, type_):
    try:
        url = f"https://api.themoviedb.org/3/find/{imdb_id}?api_key={TMDB_API_KEY}&external_source=imdb_id"
        res = requests.get(url).json()
        if type_ == "movie" and res.get('movie_results'):
            data = res['movie_results'][0]
            year = data.get('release_date', '').split('-')[0] if data.get('release_date') else None
            return data.get('title'), year
        elif type_ == "series" and res.get('tv_results'):
            data = res['tv_results'][0]
            year = data.get('first_air_date', '').split('-')[0] if data.get('first_air_date') else None
            return data.get('name'), year
    except:
        return None, None
    return None, None

def scrape_ctg_movies(title, year, type_, season=None, episode=None):
    streams = []
    if not title: return streams
    try:
        search_endpoint = "/movies" if type_ == "movie" else "/tv"
        search_url = f"{CTG_API_BASE}{search_endpoint}?search={title}"
        search_res = requests.get(search_url, headers=HEADERS).json()
        items = search_res if isinstance(search_res, list) else search_res.get('data', [])
        best_match_id = None
        
        target_norm = clean_title(title)
        for item in items:
            item_norm = clean_title(item.get('title') or item.get('name') or '')
            if target_norm in item_norm:
                best_match_id = item.get('slug') or item.get('id')
                break
                
        if not best_match_id: return streams

        detail_url = f"{CTG_API_BASE}{search_endpoint}/{best_match_id}"
        detail_data = requests.get(detail_url, headers=HEADERS).json()
        
        links = []
        if type_ == "movie":
            links = detail_data.get('links', [])
        else:
            episodes = detail_data.get('episodes', [])
            for ep in episodes:
                if str(ep.get('season_number')) == str(season) and str(ep.get('episode_number')) == str(episode):
                    links = ep.get('links', [])
                    break
        
        for link in links:
            url = link.get('url') or link.get('file') or link.get('link')
            if not url: continue
            lang = link.get('language') or link.get('lang') or "Unknown"
            quality = link.get('quality') or "1080p"
            
            streams.append({
                "name": "JaatOG Durnel",
                "title": f"CTGMovies | {quality}\nLang: {lang}",
                "url": url,
                "behaviorHints": {"notWebReady": True}
            })
    except Exception as e:
        print("Scraping error:", e)
    return streams

# ==========================================
# 3. STREAM HANDLER (Multiple Providers)
# ==========================================
@app.route('/<config>/stream/<type_>/<video_id>.json')
@app.route('/stream/<type_>/<video_id>.json')
def get_stream(type_, video_id, config="all"):
    streams = []
    selected_providers = config.split(',') if config != "all" else ["durnel", "vixsrc", "lyrin"]

    parts = video_id.split(':')
    imdb_id = parts[0]
    season = parts[1] if len(parts) > 1 else None
    episode = parts[2] if len(parts) > 2 else None

    title, year = get_tmdb_info(imdb_id, type_)

    # 1. Real Scraping for DURNEL (CTGMovies)
    if "durnel" in selected_providers and title:
        durnel_streams = scrape_ctg_movies(title, year, type_, season, episode)
        streams.extend(durnel_streams)

    # 2. VIXSRC (Need Code)
    if "vixsrc" in selected_providers:
        # Abhi ke liye yahan message bhej rahe hain taaki Stremio crash na ho
        streams.append({
            "name": "JaatOG VixSrc",
            "title": "VixSrc Engine Pending\n(Code Required)",
            "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"
        })

    # 3. LYRIN (Need Code)
    if "lyrin" in selected_providers:
        streams.append({
            "name": "JaatOG Lyrin",
            "title": "Lyrin Engine Pending\n(Code Required)",
            "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"
        })

    return jsonify({"streams": streams})

if __name__ == '__main__':
    app.run()
