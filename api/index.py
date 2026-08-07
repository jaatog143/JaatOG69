from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ==========================================
# 1. SETUP PAGE (PREMIUM UI MATCHING ECLIPSIA)
# ==========================================
SETUP_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JaatOG Eclipsia Setup</title>
    <style>
        body {
            background-color: #0b0c10;
            color: #c5c6c7;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 20px;
            padding-bottom: 100px;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .header h1 { color: #ffffff; font-weight: 400; letter-spacing: 2px;}
        
        .provider-card {
            background-color: #14151a;
            border: 1px solid #2a2b32;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .provider-info h3 {
            margin: 0 0 5px 0;
            color: #ffffff;
            font-size: 16px;
            letter-spacing: 1px;
        }
        .provider-info p {
            margin: 0;
            font-size: 13px;
            color: #888;
        }

        /* Toggle Switch CSS */
        .switch { position: relative; display: inline-block; width: 50px; height: 26px; }
        .switch input { opacity: 0; width: 0; height: 0; }
        .slider {
            position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0;
            background-color: #2a2b32; transition: .4s; border-radius: 34px;
        }
        .slider:before {
            position: absolute; content: ""; height: 18px; width: 18px; left: 4px; bottom: 4px;
            background-color: #888; transition: .4s; border-radius: 50%;
        }
        input:checked + .slider { background-color: #4a6b8c; }
        input:checked + .slider:before { transform: translateX(24px); background-color: #ffffff; }

        .bottom-bar {
            position: fixed; bottom: 0; left: 0; right: 0;
            background-color: #0b0c10; border-top: 1px solid #2a2b32;
            padding: 20px; text-align: center;
        }
        .install-btn {
            background-color: #2a2b32; color: white; border: none;
            padding: 15px 30px; border-radius: 25px; font-size: 16px;
            width: 100%; max-width: 400px; cursor: pointer; transition: 0.3s;
        }
        .install-btn:hover { background-color: #3a3b42; }
    </style>
</head>
<body>

    <div class="header">
        <h1>eclipsia jaatog</h1>
    </div>

    <!-- Provider 1 -->
    <div class="provider-card">
        <div class="provider-info">
            <h3>VixSrc .</h3>
            <p>Provider: VixSrc | English, Italian</p>
        </div>
        <label class="switch">
            <input type="checkbox" class="prov-checkbox" value="vixsrc" checked>
            <span class="slider"></span>
        </label>
    </div>

    <!-- Provider 2 -->
    <div class="provider-card">
        <div class="provider-info">
            <h3>Lyrin .</h3>
            <p>Provider: BanglaPlex | English, Hindi</p>
        </div>
        <label class="switch">
            <input type="checkbox" class="prov-checkbox" value="lyrin" checked>
            <span class="slider"></span>
        </label>
    </div>

    <!-- Provider 3 -->
    <div class="provider-card">
        <div class="provider-info">
            <h3>Mavonyx .</h3>
            <p>Provider: MovieBox | English, Bangla, Hindi</p>
        </div>
        <label class="switch">
            <input type="checkbox" class="prov-checkbox" value="mavonyx" checked>
            <span class="slider"></span>
        </label>
    </div>

    <div class="bottom-bar">
        <button class="install-btn" onclick="generateManifest()">Generate manifest URL</button>
    </div>

    <script>
        function generateManifest() {
            // Saare checked toggles ki values ikkathi karo
            const checkboxes = document.querySelectorAll('.prov-checkbox:checked');
            let selectedProviders = Array.from(checkboxes).map(cb => cb.value);
            
            let config = selectedProviders.length > 0 ? selectedProviders.join(',') : 'none';
            let baseUrl = window.location.host;
            
            // Stremio install link banao
            let installLink = `stremio://${baseUrl}/${config}/manifest.json`;
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
        "id": "org.jaatog.eclipsia.v2",
        "version": "2.0.0",
        "name": "JaatOG Eclipsia",
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
# 3. STREAM HANDLER (MULTIPLE LINKS LOGIC)
# ==========================================
@app.route('/<config>/stream/<type_>/<video_id>.json')
@app.route('/stream/<type_>/<video_id>.json')
def get_stream(type_, video_id, config="all"):
    streams = []
    
    # URL mein se provider list nikalo (e.g., "vixsrc,lyrin")
    selected_providers = config.split(',') if config != "all" else ["vixsrc", "lyrin", "mavonyx"]

    # Har provider ki apni dummy streaming link aur title define kiya hai
    # (Baad mein yahan web scraping ka code aayega)
    if "vixsrc" in selected_providers:
        streams.append({
            "name": "JaatOG VixSrc",
            "title": "VixSrc | English [1080p]\nAuto-generated link",
            "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"
        })

    if "lyrin" in selected_providers:
        streams.append({
            "name": "JaatOG Lyrin",
            "title": "Lyrin | Hindi [720p]\nAuto-generated link",
            "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8" 
        })

    if "mavonyx" in selected_providers:
        streams.append({
            "name": "JaatOG Mavonyx",
            "title": "Mavonyx | Multi-Lang [4K]\nAuto-generated link",
            "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"
        })

    return jsonify({"streams": streams})

if __name__ == '__main__':
    app.run()
