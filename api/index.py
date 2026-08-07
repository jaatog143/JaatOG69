from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ==========================================
# 1. SETUP PAGE (HTML) - Customization UI
# ==========================================
SETUP_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>JaatOG Custom Addon</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body style="background-color: #1a1a1a; color: white; font-family: sans-serif; text-align: center; padding: 40px;">
    
    <h2>JaatOG Eclipsia Addon Setup</h2>
    <p>Apne pasand ke providers select karo:</p>
    
    <div style="background: #2c2c2c; padding: 20px; border-radius: 10px; display: inline-block; text-align: left;">
        <label style="font-size: 18px; cursor: pointer;">
            <input type="checkbox" id="prov_hindi" value="hindi" checked> Hindi Links Provider
        </label><br><br>
        <label style="font-size: 18px; cursor: pointer;">
            <input type="checkbox" id="prov_english" value="english" checked> English Links Provider
        </label>
    </div>

    <br><br>
    
    <button onclick="installAddon()" style="padding: 12px 25px; font-size: 18px; background: #8a5a99; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">
        Install on Stremio
    </button>

    <script>
        function installAddon() {
            let selectedProviders = [];
            
            if(document.getElementById('prov_hindi').checked) selectedProviders.push('hindi');
            if(document.getElementById('prov_english').checked) selectedProviders.push('english');
            
            // Agar user ne kuch select nahi kiya, toh default 'all' de do
            let config = selectedProviders.length > 0 ? selectedProviders.join(',') : 'all';
            
            let baseUrl = window.location.host;
            // Custom link generate karo with configuration
            let installLink = `stremio://${baseUrl}/${config}/manifest.json`;
            
            window.location.href = installLink;
        }
    </script>
</body>
</html>
"""

# Home page par Setup UI dikhao
@app.route('/')
def home():
    return SETUP_HTML

# ==========================================
# 2. ADDON MANIFEST (With Config Logic)
# ==========================================
@app.route('/<config>/manifest.json')
@app.route('/manifest.json')
def get_manifest(config="all"):
    return jsonify({
        "id": "org.jaatog.custompython",
        "version": "1.0.0",
        "name": f"JaatOG Eclipsia", # Addon ka naam Stremio mein
        "description": f"Providers selected: {config}",
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
# 3. STREAM HANDLER (Custom Scraping Logic)
# ==========================================
@app.route('/<config>/stream/<type_>/<video_id>.json')
@app.route('/stream/<type_>/<video_id>.json')
def get_stream(type_, video_id, config="all"):
    # video_id IMDB ID hoti hai (e.g., tt1234567)
    streams = []

    # Config Check: Agar user ne 'hindi' select kiya hai
    if "hindi" in config or config == "all":
        # Yahan tum apna Hindi website ka scraping code lagaoge
        streams.append({
            "title": "Hindi Source [1080p]",
            "url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4"
        })

    # Config Check: Agar user ne 'english' select kiya hai
    if "english" in config or config == "all":
        # Yahan tum apna English website ka scraping code lagaoge
        streams.append({
            "title": "English Source [4K]",
            "url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
        })

    return jsonify({"streams": streams})

if __name__ == '__main__':
    app.run()
