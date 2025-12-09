"""
URL Shortener - Flask Application
=================================
A fully functional URL shortening service (like bit.ly or tinyurl).

FEATURES:
- Shorten long URLs to short codes
- Redirect short codes to original URLs
- Track click counts
- API endpoints for programmatic access
- Beautiful, modern UI

ARCHITECTURE:
- Flask web framework
- PostgreSQL for persistent storage (production)
- SQLite fallback for development
- Redis for caching (optional, for high performance)

YOUR DOCKER CHALLENGE:
1. Create a Dockerfile to containerize this app
2. Create a docker-compose.yml with:
   - This Flask app as a service
   - PostgreSQL database service
   - (Bonus) Redis for caching
   - (Bonus) Nginx as a reverse proxy
3. Configure environment variables properly
4. Set up health checks
5. Use volumes for database persistence

Good luck! 🐳
"""

from flask import Flask, request, redirect, jsonify, render_template_string
import os
import string
import random
from datetime import datetime

# =============================================================================
# FLASK APP INITIALIZATION
# =============================================================================
app = Flask(__name__)

# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================
# For simplicity, we'll use an in-memory dictionary for now
# In production with Docker, you'll want to connect to PostgreSQL
# 
# HINT FOR DOCKER: Use environment variables for database connection!
# Example: DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///urls.db')

# In-memory storage (replace with database in production)
url_database = {}
click_counts = {}

# =============================================================================
# CONFIGURATION FROM ENVIRONMENT VARIABLES
# =============================================================================
# DOCKER TIP: These should be set in your docker-compose.yml or .env file
APP_NAME = os.environ.get('APP_NAME', 'URL Shortener')
BASE_URL = os.environ.get('BASE_URL', 'http://localhost:5000')
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-change-in-production')
DEBUG = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'

app.secret_key = SECRET_KEY


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================
def generate_short_code(length=6):
    """Generate a random short code for URLs"""
    characters = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choices(characters, k=length))
        if code not in url_database:
            return code


def is_valid_url(url):
    """Basic URL validation"""
    return url.startswith(('http://', 'https://'))


# =============================================================================
# HTML TEMPLATES
# =============================================================================
HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ app_name }}</title>
    <meta name="description" content="Transform long URLs into short, shareable links instantly">
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #030014;
            --bg-secondary: #0a0a1f;
            --accent-cyan: #00f5ff;
            --accent-purple: #a855f7;
            --accent-pink: #ec4899;
            --accent-blue: #3b82f6;
            --text-primary: #ffffff;
            --text-secondary: rgba(255,255,255,0.6);
            --glass-bg: rgba(255,255,255,0.03);
            --glass-border: rgba(255,255,255,0.08);
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Space Grotesk', sans-serif;
            background: var(--bg-primary);
            min-height: 100vh;
            color: var(--text-primary);
            overflow-x: hidden;
        }
        
        /* Animated Background */
        .bg-animation {
            position: fixed;
            inset: 0;
            z-index: -1;
            overflow: hidden;
        }
        
        .orb {
            position: absolute;
            border-radius: 50%;
            filter: blur(80px);
            opacity: 0.5;
            animation: float 20s ease-in-out infinite;
        }
        
        .orb-1 { width: 600px; height: 600px; background: var(--accent-purple); top: -200px; left: -100px; animation-delay: 0s; }
        .orb-2 { width: 500px; height: 500px; background: var(--accent-cyan); bottom: -150px; right: -100px; animation-delay: -5s; }
        .orb-3 { width: 400px; height: 400px; background: var(--accent-pink); top: 50%; left: 50%; transform: translate(-50%, -50%); animation-delay: -10s; }
        
        @keyframes float {
            0%, 100% { transform: translate(0, 0) scale(1); }
            25% { transform: translate(50px, -50px) scale(1.1); }
            50% { transform: translate(-30px, 30px) scale(0.9); }
            75% { transform: translate(-50px, -30px) scale(1.05); }
        }
        
        .grid-overlay {
            position: fixed;
            inset: 0;
            background-image: 
                linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
            background-size: 60px 60px;
            z-index: -1;
        }
        
        .container { max-width: 900px; margin: 0 auto; padding: 60px 24px; position: relative; }
        
        /* Header */
        header { text-align: center; margin-bottom: 60px; }
        
        .logo-container {
            width: 100px; height: 100px;
            margin: 0 auto 24px;
            background: linear-gradient(135deg, var(--accent-purple), var(--accent-cyan));
            border-radius: 28px;
            display: flex; align-items: center; justify-content: center;
            font-size: 3rem;
            box-shadow: 0 20px 60px -15px rgba(168, 85, 247, 0.5);
            animation: pulse-glow 3s ease-in-out infinite;
        }
        
        @keyframes pulse-glow {
            0%, 100% { box-shadow: 0 20px 60px -15px rgba(168, 85, 247, 0.5); }
            50% { box-shadow: 0 25px 80px -10px rgba(0, 245, 255, 0.4); }
        }
        
        h1 {
            font-size: 3.5rem; font-weight: 700; letter-spacing: -1px;
            background: linear-gradient(135deg, #fff 0%, var(--accent-cyan) 50%, var(--accent-purple) 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
        }
        
        .tagline { color: var(--text-secondary); margin-top: 16px; font-size: 1.2rem; font-weight: 300; }
        
        /* Main Card */
        .card {
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            border-radius: 32px;
            padding: 48px;
            border: 1px solid var(--glass-border);
            box-shadow: 0 40px 80px -20px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.05);
            margin-bottom: 40px;
            position: relative;
            overflow: hidden;
        }
        
        .card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--accent-cyan), var(--accent-purple), transparent);
        }
        
        .input-group { display: flex; gap: 16px; }
        
        input[type="url"] {
            flex: 1;
            padding: 20px 28px;
            border: 2px solid var(--glass-border);
            border-radius: 16px;
            background: rgba(0,0,0,0.4);
            color: #fff;
            font-size: 1.1rem;
            font-family: inherit;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        input[type="url"]:focus {
            outline: none;
            border-color: var(--accent-cyan);
            box-shadow: 0 0 0 4px rgba(0, 245, 255, 0.15), 0 0 40px rgba(0, 245, 255, 0.2);
        }
        
        input[type="url"]::placeholder { color: rgba(255,255,255,0.3); }
        
        .btn-primary {
            padding: 20px 40px;
            background: linear-gradient(135deg, var(--accent-purple), var(--accent-blue));
            border: none;
            border-radius: 16px;
            color: #fff;
            font-size: 1.1rem;
            font-weight: 600;
            font-family: inherit;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .btn-primary::before {
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
            opacity: 0;
            transition: opacity 0.3s;
        }
        
        .btn-primary:hover { transform: translateY(-3px); box-shadow: 0 20px 40px -10px rgba(168, 85, 247, 0.5); }
        .btn-primary:hover::before { opacity: 1; }
        .btn-primary span { position: relative; z-index: 1; }
        
        /* Result */
        .result {
            display: none;
            margin-top: 32px;
            padding: 28px;
            background: linear-gradient(135deg, rgba(0,245,255,0.1), rgba(168,85,247,0.1));
            border: 1px solid rgba(0, 245, 255, 0.3);
            border-radius: 20px;
            animation: slideIn 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .result.show { display: block; }
        
        @keyframes slideIn { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }
        
        .result-header { display: flex; align-items: center; gap: 10px; margin-bottom: 16px; }
        .result-header .icon { font-size: 1.5rem; }
        .result-label { color: var(--accent-cyan); font-size: 0.9rem; font-weight: 500; text-transform: uppercase; letter-spacing: 1px; }
        
        .result-content { display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 20px; }
        
        .result-url-section { flex: 1; }
        .result-url { color: #fff; font-size: 1.4rem; font-weight: 600; text-decoration: none; word-break: break-all; transition: color 0.3s; }
        .result-url:hover { color: var(--accent-cyan); }
        
        .result-actions { display: flex; gap: 12px; }
        
        .btn-secondary {
            padding: 12px 24px;
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 12px;
            color: #fff;
            font-size: 0.9rem;
            font-weight: 500;
            font-family: inherit;
            cursor: pointer;
            transition: all 0.3s;
            display: flex; align-items: center; gap: 8px;
        }
        
        .btn-secondary:hover { background: rgba(255,255,255,0.2); transform: translateY(-2px); }
        .btn-secondary.copied { background: rgba(0, 245, 255, 0.2); border-color: var(--accent-cyan); }
        
        /* QR Code */
        .qr-section { display: none; margin-top: 24px; padding-top: 24px; border-top: 1px solid var(--glass-border); }
        .qr-section.show { display: flex; align-items: center; gap: 24px; flex-wrap: wrap; }
        .qr-code { background: #fff; padding: 12px; border-radius: 12px; }
        .qr-code img { display: block; }
        .qr-info h4 { color: var(--text-secondary); font-size: 0.85rem; font-weight: 500; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px; }
        .qr-info p { color: var(--text-secondary); font-size: 0.9rem; }
        
        /* Stats */
        .stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; margin-top: 48px; }
        
        .stat-card {
            background: var(--glass-bg);
            border-radius: 24px;
            padding: 32px;
            text-align: center;
            border: 1px solid var(--glass-border);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .stat-card::before {
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(135deg, rgba(168, 85, 247, 0.1), rgba(0, 245, 255, 0.1));
            opacity: 0;
            transition: opacity 0.4s;
        }
        
        .stat-card:hover { transform: translateY(-8px); border-color: rgba(168, 85, 247, 0.3); }
        .stat-card:hover::before { opacity: 1; }
        
        .stat-icon { font-size: 2rem; margin-bottom: 12px; position: relative; z-index: 1; }
        .stat-number {
            font-size: 2.5rem; font-weight: 700; position: relative; z-index: 1;
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        .stat-label { color: var(--text-secondary); font-size: 0.9rem; margin-top: 8px; position: relative; z-index: 1; }
        
        /* Recent URLs */
        .recent { margin-top: 48px; }
        .section-header { display: flex; align-items: center; gap: 12px; margin-bottom: 20px; }
        .section-header h3 { color: var(--text-secondary); font-size: 0.85rem; font-weight: 500; text-transform: uppercase; letter-spacing: 2px; }
        .section-line { flex: 1; height: 1px; background: linear-gradient(90deg, var(--glass-border), transparent); }
        
        .url-item {
            background: var(--glass-bg);
            border-radius: 16px;
            padding: 20px 24px;
            margin-bottom: 12px;
            display: grid;
            grid-template-columns: 1fr auto auto;
            align-items: center;
            gap: 24px;
            border: 1px solid var(--glass-border);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .url-item:hover { background: rgba(255,255,255,0.05); border-color: rgba(168, 85, 247, 0.3); transform: translateX(8px); }
        
        .url-short { color: var(--accent-cyan); text-decoration: none; font-weight: 600; font-size: 1.05rem; transition: color 0.3s; }
        .url-short:hover { color: var(--accent-purple); }
        .url-original { color: var(--text-secondary); font-size: 0.85rem; max-width: 280px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
        .url-clicks { color: var(--accent-purple); font-weight: 600; display: flex; align-items: center; gap: 6px; }
        .url-clicks::before { content: '👁'; font-size: 0.9rem; }
        
        /* API Section */
        .api-section { margin-top: 56px; padding-top: 40px; border-top: 1px solid var(--glass-border); }
        .api-section h3 { color: var(--accent-purple); margin-bottom: 20px; display: flex; align-items: center; gap: 12px; font-size: 1.2rem; }
        
        .endpoints { display: grid; gap: 12px; }
        
        .endpoint {
            background: rgba(0,0,0,0.3);
            border-radius: 12px;
            padding: 16px 20px;
            font-family: 'JetBrains Mono', 'Fira Code', monospace;
            font-size: 0.9rem;
            display: flex;
            align-items: center;
            gap: 16px;
            border: 1px solid var(--glass-border);
            transition: all 0.3s;
        }
        
        .endpoint:hover { border-color: rgba(168, 85, 247, 0.3); }
        
        .method {
            padding: 4px 12px;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.5px;
        }
        
        .method.post { background: var(--accent-purple); }
        .method.get { background: var(--accent-cyan); color: #000; }
        
        .endpoint-path { color: var(--text-secondary); }
        .endpoint-desc { color: rgba(255,255,255,0.4); margin-left: auto; font-size: 0.8rem; }
        
        /* Docker Banner */
        .docker-banner {
            margin-top: 48px;
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(59, 130, 246, 0.05));
            border: 1px solid rgba(59, 130, 246, 0.3);
            border-radius: 20px;
            padding: 28px 32px;
            display: flex;
            align-items: center;
            gap: 20px;
            transition: all 0.4s;
        }
        
        .docker-banner:hover { border-color: rgba(59, 130, 246, 0.5); transform: translateY(-4px); }
        .docker-banner .emoji { font-size: 2.5rem; }
        .docker-banner-content h4 { color: var(--accent-blue); font-size: 1rem; margin-bottom: 6px; }
        .docker-banner-content p { color: var(--text-secondary); font-size: 0.9rem; }
        
        /* Footer */
        footer { text-align: center; margin-top: 60px; padding-top: 40px; border-top: 1px solid var(--glass-border); }
        footer p { color: var(--text-secondary); font-size: 0.85rem; }
        footer a { color: var(--accent-cyan); text-decoration: none; transition: color 0.3s; }
        footer a:hover { color: var(--accent-purple); }
        
        @media (max-width: 768px) {
            h1 { font-size: 2.5rem; }
            .input-group { flex-direction: column; }
            .stats { grid-template-columns: 1fr; }
            .url-item { grid-template-columns: 1fr; gap: 12px; text-align: center; }
            .card { padding: 32px 24px; }
            .result-content { flex-direction: column; align-items: flex-start; }
        }
    </style>
</head>
<body>
    <div class="bg-animation">
        <div class="orb orb-1"></div>
        <div class="orb orb-2"></div>
        <div class="orb orb-3"></div>
    </div>
    <div class="grid-overlay"></div>
    
    <div class="container">
        <header>
            <div class="logo-container">🔗</div>
            <h1>{{ app_name }}</h1>
            <p class="tagline">Transform long URLs into short, shareable links</p>
        </header>
        
        <div class="card">
            <form id="shorten-form">
                <div class="input-group">
                    <input type="url" name="url" id="url-input" placeholder="Paste your long URL here..." required autocomplete="off">
                    <button type="submit" class="btn-primary"><span>Shorten URL</span></button>
                </div>
            </form>
            
            <div class="result" id="result">
                <div class="result-header">
                    <span class="icon">✨</span>
                    <span class="result-label">Your shortened URL is ready!</span>
                </div>
                <div class="result-content">
                    <div class="result-url-section">
                        <a href="#" id="short-url" class="result-url" target="_blank"></a>
                    </div>
                    <div class="result-actions">
                        <button class="btn-secondary" id="copy-btn" onclick="copyUrl()">
                            <span>📋</span> Copy
                        </button>
                        <button class="btn-secondary" onclick="toggleQR()">
                            <span>📱</span> QR Code
                        </button>
                    </div>
                </div>
                <div class="qr-section" id="qr-section">
                    <div class="qr-code">
                        <img id="qr-img" src="" alt="QR Code" width="120" height="120">
                    </div>
                    <div class="qr-info">
                        <h4>Scan to visit</h4>
                        <p>Use your phone's camera to scan this QR code and open the shortened URL.</p>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-icon">🔗</div>
                <div class="stat-number">{{ total_urls }}</div>
                <div class="stat-label">URLs Shortened</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">👆</div>
                <div class="stat-number">{{ total_clicks }}</div>
                <div class="stat-label">Total Clicks</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">⚡</div>
                <div class="stat-number">∞</div>
                <div class="stat-label">Possibilities</div>
            </div>
        </div>
        
        {% if recent_urls %}
        <div class="recent">
            <div class="section-header">
                <h3>Recent URLs</h3>
                <div class="section-line"></div>
            </div>
            {% for item in recent_urls %}
            <div class="url-item">
                <div>
                    <a class="url-short" href="/{{ item.code }}" target="_blank">{{ base_url }}/{{ item.code }}</a>
                    <div class="url-original">{{ item.original }}</div>
                </div>
                <span class="url-clicks">{{ item.clicks }} clicks</span>
            </div>
            {% endfor %}
        </div>
        {% endif %}
        
        <div class="api-section">
            <h3>🔌 API Endpoints</h3>
            <div class="endpoints">
                <div class="endpoint">
                    <span class="method post">POST</span>
                    <span class="endpoint-path">/api/shorten</span>
                    <span class="endpoint-desc">Create short URL</span>
                </div>
                <div class="endpoint">
                    <span class="method get">GET</span>
                    <span class="endpoint-path">/api/stats/&lt;code&gt;</span>
                    <span class="endpoint-desc">Get URL statistics</span>
                </div>
                <div class="endpoint">
                    <span class="method get">GET</span>
                    <span class="endpoint-path">/health</span>
                    <span class="endpoint-desc">Health check</span>
                </div>
            </div>
        </div>
        
        <div class="docker-banner">
            <span class="emoji">🐳</span>
            <div class="docker-banner-content">
                <h4>Docker Challenge</h4>
                <p>Containerize this app with PostgreSQL and Redis. Check the README for hints!</p>
            </div>
        </div>
        
        <footer>
            <p>Built with ❤️ for learning Docker • <a href="https://github.com" target="_blank">View on GitHub</a></p>
        </footer>
    </div>
    
    <script>
        document.getElementById('shorten-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = e.target.querySelector('.btn-primary');
            const originalText = btn.innerHTML;
            btn.innerHTML = '<span>⏳ Shortening...</span>';
            btn.disabled = true;
            
            try {
                const response = await fetch('/api/shorten', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url: document.getElementById('url-input').value })
                });
                
                const data = await response.json();
                
                if (data.short_url) {
                    document.getElementById('short-url').href = data.short_url;
                    document.getElementById('short-url').textContent = data.short_url;
                    document.getElementById('qr-img').src = `https://api.qrserver.com/v1/create-qr-code/?size=120x120&data=${encodeURIComponent(data.short_url)}`;
                    document.getElementById('result').classList.add('show');
                    document.getElementById('url-input').value = '';
                }
            } catch (err) {
                console.error(err);
            }
            
            btn.innerHTML = originalText;
            btn.disabled = false;
        });
        
        function copyUrl() {
            const url = document.getElementById('short-url').textContent;
            navigator.clipboard.writeText(url);
            const btn = document.getElementById('copy-btn');
            btn.innerHTML = '<span>✅</span> Copied!';
            btn.classList.add('copied');
            setTimeout(() => {
                btn.innerHTML = '<span>📋</span> Copy';
                btn.classList.remove('copied');
            }, 2000);
        }
        
        function toggleQR() {
            document.getElementById('qr-section').classList.toggle('show');
        }
    </script>
</body>
</html>
"""


# =============================================================================
# WEB ROUTES
# =============================================================================

@app.route('/')
def home():
    """Home page with URL shortening form"""
    # Get recent URLs for display
    recent = []
    for code, url in list(url_database.items())[-5:]:
        recent.append({
            'code': code,
            'original': url[:50] + '...' if len(url) > 50 else url,
            'clicks': click_counts.get(code, 0)
        })
    
    return render_template_string(
        HOME_TEMPLATE,
        app_name=APP_NAME,
        base_url=BASE_URL,
        total_urls=len(url_database),
        total_clicks=sum(click_counts.values()),
        recent_urls=reversed(recent)
    )


@app.route('/<code>')
def redirect_to_url(code):
    """Redirect short code to original URL"""
    if code in url_database:
        # Increment click count
        click_counts[code] = click_counts.get(code, 0) + 1
        return redirect(url_database[code])
    return render_template_string("""
        <html>
        <head><title>Not Found</title></head>
        <body style="font-family: sans-serif; text-align: center; padding: 50px; background: #1a1a2e; color: #fff;">
            <h1>🔗 URL Not Found</h1>
            <p>The short URL you're looking for doesn't exist.</p>
            <a href="/" style="color: #00d4ff;">Go Home</a>
        </body>
        </html>
    """), 404


@app.route('/shorten', methods=['POST'])
def shorten_form():
    """Handle form submission (redirect back to home)"""
    url = request.form.get('url')
    if url and is_valid_url(url):
        code = generate_short_code()
        url_database[code] = url
        click_counts[code] = 0
    return redirect('/')


# =============================================================================
# API ROUTES
# =============================================================================

@app.route('/api/shorten', methods=['POST'])
def api_shorten():
    """
    API endpoint to create a short URL
    
    Request body: {"url": "https://example.com/very/long/url"}
    Response: {"short_url": "http://localhost:5000/abc123", "code": "abc123"}
    """
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({'error': 'URL is required'}), 400
    
    url = data['url']
    
    if not is_valid_url(url):
        return jsonify({'error': 'Invalid URL. Must start with http:// or https://'}), 400
    
    code = generate_short_code()
    url_database[code] = url
    click_counts[code] = 0
    
    return jsonify({
        'short_url': f'{BASE_URL}/{code}',
        'code': code,
        'original_url': url,
        'created_at': datetime.now().isoformat()
    })


@app.route('/api/stats/<code>')
def api_stats(code):
    """
    Get statistics for a short URL
    
    Response: {"code": "abc123", "original_url": "...", "clicks": 42}
    """
    if code not in url_database:
        return jsonify({'error': 'URL not found'}), 404
    
    return jsonify({
        'code': code,
        'original_url': url_database[code],
        'clicks': click_counts.get(code, 0),
        'short_url': f'{BASE_URL}/{code}'
    })


@app.route('/api/urls')
def api_list_urls():
    """List all shortened URLs (for admin/debugging)"""
    urls = []
    for code, url in url_database.items():
        urls.append({
            'code': code,
            'short_url': f'{BASE_URL}/{code}',
            'original_url': url,
            'clicks': click_counts.get(code, 0)
        })
    return jsonify({'urls': urls, 'total': len(urls)})


@app.route('/health')
def health():
    """
    Health Check Endpoint
    ---------------------
    CRITICAL for container orchestration!
    
    Docker, Kubernetes, and AWS ECS use this to determine if your container
    is healthy and ready to receive traffic.
    
    DOCKER TIP: Add this to your docker-compose.yml:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    """
    return jsonify({
        'status': 'healthy',
        'app': APP_NAME,
        'timestamp': datetime.now().isoformat(),
        'total_urls': len(url_database),
        'database': 'in-memory'  # Change to 'postgresql' when you add DB
    })


# =============================================================================
# RUN THE APP
# =============================================================================
if __name__ == '__main__':
    # DOCKER TIP: 
    # - host='0.0.0.0' makes the app accessible from outside the container
    # - In production, use gunicorn instead of Flask's dev server:
    #   gunicorn --bind 0.0.0.0:5000 app:app
    
    port = int(os.environ.get('PORT', 5000))
    print(f"""
    ╔══════════════════════════════════════════════════════════════╗
    ║                    🔗 URL SHORTENER                          ║
    ║══════════════════════════════════════════════════════════════║
    ║  Running at: http://localhost:{port}                          ║
    ║                                                              ║
    ║  DOCKER CHALLENGE:                                           ║
    ║  1. Create a Dockerfile for this app                         ║
    ║  2. Add PostgreSQL with docker-compose                       ║
    ║  3. Add Redis for caching (bonus)                            ║
    ║  4. Deploy to AWS EC2                                        ║
    ║                                                              ║
    ║  Good luck! 🐳                                               ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    app.run(host='0.0.0.0', port=port, debug=DEBUG)
