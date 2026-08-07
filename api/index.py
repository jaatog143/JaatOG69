import requests
from bs4 import BeautifulSoup # HTML se data nikalne ke liye

# ... (Upar ka UI aur Manifest code same rahega) ...

# ==========================================
# 3. ASLI STREAM HANDLER (WEB SCRAPING LOGIC)
# ==========================================
@app.route('/<config>/stream/<type_>/<video_id>.json')
@app.route('/stream/<type_>/<video_id>.json')
def get_stream(type_, video_id, config="all"):
    streams = []
    selected_providers = config.split(',') if config != "all" else ["vixsrc", "lyrin", "mavonyx"]

    # 1. Stremio ID ko parse karo (IMDB ID, Season, Episode alag karo)
    id_parts = video_id.split(':')
    imdb_id = id_parts[0] 
    
    is_series = len(id_parts) == 3
    season = id_parts[1] if is_series else None
    episode = id_parts[2] if is_series else None

    # Browser banne ka natak karne ke liye Headers (Taaki website block na kare)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }

    # 2. VIXSRC PROVIDER SCRAPING
    if "vixsrc" in selected_providers:
        try:
            # Yahan tumhari provider website ka base URL aayega
            # Example format (Tumhe Eclipsia ke JS se inka asli URL dekhna hoga):
            if type_ == "movie":
                provider_url = f"https://vidsrc.to/embed/movie/{imdb_id}"
            else:
                provider_url = f"https://vidsrc.to/embed/tv/{imdb_id}/{season}/{episode}"

            # Website ko request bhejo
            response = requests.get(provider_url, headers=headers, timeout=10)
            
            # Agar website khul gayi (Status 200)
            if response.status_code == 200:
                # Beautiful Soup se HTML parse karo
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # YAHAN MAIN KAAM HAI: HTML ke andar se .m3u8 ya .mp4 link dhoondhna
                # Example: <iframe src="https://player.site.com/movie.m3u8">
                iframe = soup.find('iframe')
                if iframe and iframe.get('src'):
                    asli_link = iframe.get('src')
                    
                    streams.append({
                        "name": "JaatOG VixSrc",
                        "title": f"VixSrc Provider | {type_.capitalize()}\n1080p scraped",
                        "url": asli_link # Asli link seedha player ko bhej diya
                    })
        except Exception as e:
            print(f"VixSrc error: {e}") # Agar website down hui toh addon crash nahi hoga

    # 3. LYRIN PROVIDER SCRAPING (Same logic, alag website)
    if "lyrin" in selected_providers:
        try:
            # Lyrin ka API endpoint yahan aayega
            api_url = f"https://api.lyrin-example.com/search?imdb={imdb_id}"
            res = requests.get(api_url, headers=headers).json()
            
            if "video_link" in res:
                streams.append({
                    "name": "JaatOG Lyrin",
                    "title": "Lyrin | Hindi Source",
                    "url": res["video_link"]
                })
        except Exception as e:
            pass

    return jsonify({"streams": streams})
