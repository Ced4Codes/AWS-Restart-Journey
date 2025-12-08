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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a3e 50%, #2d1b4e 100%);
            min-height: 100vh;
            color: #fff;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        
        header {
            text-align: center;
            margin-bottom: 50px;
        }
        
        .logo {
            font-size: 3rem;
            margin-bottom: 10px;
        }
        
        h1 {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(90deg, #00d4ff, #7c3aed, #ff006e);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .tagline {
            color: #888;
            margin-top: 10px;
            font-size: 1.1rem;
        }
        
        /* Main Form Card */
        .card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(20px);
            border-radius: 24px;
            padding: 40px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            margin-bottom: 30px;
        }
        
        .input-group {
            display: flex;
            gap: 12px;
            margin-bottom: 20px;
        }
        
        input[type="url"] {
            flex: 1;
            padding: 16px 24px;
            border: 2px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            background: rgba(0, 0, 0, 0.3);
            color: #fff;
            font-size: 1rem;
            transition: all 0.3s ease;
        }
        
        input[type="url"]:focus {
            outline: none;
            border-color: #7c3aed;
            box-shadow: 0 0 20px rgba(124, 58, 237, 0.3);
        }
        
        input[type="url"]::placeholder {
            color: #666;
        }
        
        button {
            padding: 16px 32px;
            background: linear-gradient(135deg, #7c3aed, #00d4ff);
            border: none;
            border-radius: 12px;
            color: #fff;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(124, 58, 237, 0.4);
        }
        
        /* Result Box */
        .result {
            display: none;
            background: rgba(0, 212, 255, 0.1);
            border: 1px solid rgba(0, 212, 255, 0.3);
            border-radius: 12px;
            padding: 20px;
            margin-top: 20px;
        }
        
        .result.show { display: block; }
        
        .result-label {
            color: #00d4ff;
            font-size: 0.85rem;
            font-weight: 500;
            margin-bottom: 8px;
        }
        
        .result-url {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .result-url a {
            color: #fff;
            font-size: 1.2rem;
            text-decoration: none;
            word-break: break-all;
        }
        
        .copy-btn {
            padding: 8px 16px;
            font-size: 0.85rem;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .copy-btn:hover {
            background: rgba(255, 255, 255, 0.2);
        }
        
        /* Stats Section */
        .stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-top: 40px;
        }
        
        .stat-card {
            background: rgba(255, 255, 255, 0.03);
            border-radius: 16px;
            padding: 24px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        .stat-number {
            font-size: 2rem;
            font-weight: 700;
            background: linear-gradient(90deg, #00d4ff, #7c3aed);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .stat-label {
            color: #666;
            font-size: 0.9rem;
            margin-top: 5px;
        }
        
        /* Recent URLs */
        .recent {
            margin-top: 40px;
        }
        
        .recent h3 {
            color: #888;
            font-size: 0.9rem;
            font-weight: 500;
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .url-item {
            background: rgba(255, 255, 255, 0.03);
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border: 1px solid rgba(255, 255, 255, 0.05);
            transition: all 0.3s ease;
        }
        
        .url-item:hover {
            background: rgba(255, 255, 255, 0.06);
            border-color: rgba(124, 58, 237, 0.3);
        }
        
        .url-short {
            color: #00d4ff;
            text-decoration: none;
            font-weight: 500;
        }
        
        .url-original {
            color: #666;
            font-size: 0.85rem;
            max-width: 300px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        
        .url-clicks {
            color: #7c3aed;
            font-weight: 600;
        }
        
        /* API Section */
        .api-section {
            margin-top: 50px;
            padding-top: 30px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .api-section h3 {
            color: #7c3aed;
            margin-bottom: 15px;
        }
        
        .endpoint {
            background: rgba(0, 0, 0, 0.3);
            border-radius: 8px;
            padding: 12px 16px;
            margin: 8px 0;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
        }
        
        .method {
            background: #7c3aed;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
            margin-right: 10px;
        }
        
        .method.get { background: #00d4ff; color: #000; }
        
        /* Docker Banner */
        .docker-banner {
            background: linear-gradient(135deg, rgba(0, 123, 255, 0.1), rgba(0, 123, 255, 0.05));
            border: 1px solid rgba(0, 123, 255, 0.3);
            border-radius: 12px;
            padding: 20px;
            margin-top: 40px;
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .docker-banner .emoji { font-size: 2rem; }
        .docker-banner p { color: #888; font-size: 0.9rem; }
        .docker-banner strong { color: #00d4ff; }
        
        @media (max-width: 600px) {
            .input-group { flex-direction: column; }
            .stats { grid-template-columns: 1fr; }
            .url-item { flex-direction: column; gap: 10px; text-align: center; }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="logo">🔗</div>
            <h1>{{ app_name }}</h1>
            <p class="tagline">Transform long URLs into short, shareable links</p>
        </header>
        
        <div class="card">
            <form id="shorten-form" action="/shorten" method="POST">
                <div class="input-group">
                    <input type="url" name="url" placeholder="Paste your long URL here..." required>
                    <button type="submit">Shorten</button>
                </div>
            </form>
            
            <div class="result" id="result">
                <div class="result-label">Your shortened URL</div>
                <div class="result-url">
                    <a href="#" id="short-url" target="_blank"></a>
                    <button class="copy-btn" onclick="copyUrl()">Copy</button>
                </div>
            </div>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{{ total_urls }}</div>
                <div class="stat-label">URLs Shortened</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ total_clicks }}</div>
                <div class="stat-label">Total Clicks</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">∞</div>
                <div class="stat-label">Possibilities</div>
            </div>
        </div>
        
        {% if recent_urls %}
        <div class="recent">
            <h3>Recent URLs</h3>
            {% for item in recent_urls %}
            <div class="url-item">
                <a class="url-short" href="/{{ item.code }}" target="_blank">{{ base_url }}/{{ item.code }}</a>
                <span class="url-original">{{ item.original }}</span>
                <span class="url-clicks">{{ item.clicks }} clicks</span>
            </div>
            {% endfor %}
        </div>
        {% endif %}
        
        <div class="api-section">
            <h3>🔌 API Endpoints</h3>
            <div class="endpoint">
                <span class="method">POST</span>/api/shorten - Create short URL
            </div>
            <div class="endpoint">
                <span class="method get">GET</span>/api/stats/&lt;code&gt; - Get URL statistics
            </div>
            <div class="endpoint">
                <span class="method get">GET</span>/health - Health check endpoint
            </div>
        </div>
        
        <div class="docker-banner">
            <span class="emoji">🐳</span>
            <p><strong>Docker Challenge:</strong> Containerize this app with PostgreSQL and Redis. Check the README for hints!</p>
        </div>
    </div>
    
    <script>
        // Handle form submission with AJAX
        document.getElementById('shorten-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            
            const response = await fetch('/api/shorten', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: formData.get('url') })
            });
            
            const data = await response.json();
            
            if (data.short_url) {
                document.getElementById('short-url').href = data.short_url;
                document.getElementById('short-url').textContent = data.short_url;
                document.getElementById('result').classList.add('show');
            }
        });
        
        function copyUrl() {
            const url = document.getElementById('short-url').textContent;
            navigator.clipboard.writeText(url);
            document.querySelector('.copy-btn').textContent = 'Copied!';
            setTimeout(() => {
                document.querySelector('.copy-btn').textContent = 'Copy';
            }, 2000);
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
