"""
File Upload Service - Flask Application
=======================================
A file upload/download service with temporary sharing links.

FEATURES:
- Upload files via web UI or API
- Generate temporary download links
- File expiration after configurable time
- Beautiful drag-and-drop UI
- File size limits

ARCHITECTURE:
- Flask web framework
- Local file storage (or MinIO/S3 in production)
- SQLite for metadata (or PostgreSQL)

YOUR DOCKER CHALLENGE:
1. Create a Dockerfile to containerize this app
2. Use volumes to persist uploaded files
3. (Bonus) Add MinIO as S3-compatible storage
4. (Bonus) Add Nginx for serving static files
5. Deploy to AWS EC2

Good luck! 🐳
"""

from flask import Flask, request, jsonify, render_template_string, send_file, abort
import os
import uuid
import hashlib
from datetime import datetime, timedelta
from pathlib import Path

# =============================================================================
# FLASK APP INITIALIZATION
# =============================================================================
app = Flask(__name__)

# =============================================================================
# CONFIGURATION
# =============================================================================
APP_NAME = os.environ.get('APP_NAME', 'File Share')
BASE_URL = os.environ.get('BASE_URL', 'http://localhost:5002')
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', './uploads')
MAX_FILE_SIZE = int(os.environ.get('MAX_FILE_SIZE', 50 * 1024 * 1024))  # 50MB default
EXPIRY_HOURS = int(os.environ.get('EXPIRY_HOURS', 24))

# Ensure upload folder exists
Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)

# In-memory storage (replace with database in production)
files_db = {}

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================
def generate_file_id():
    """Generate a unique file ID"""
    return str(uuid.uuid4())[:8]

def get_file_extension(filename):
    """Get file extension"""
    return Path(filename).suffix.lower()

def format_file_size(size_bytes):
    """Format file size for display"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"

def is_file_expired(file_info):
    """Check if file has expired"""
    expiry = datetime.fromisoformat(file_info['expires_at'])
    return datetime.now() > expiry


# =============================================================================
# HTML TEMPLATE
# =============================================================================
HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ app_name }}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh;
            color: #fff;
            padding: 40px 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        
        header {
            text-align: center;
            margin-bottom: 40px;
        }
        
        .logo { font-size: 4rem; margin-bottom: 15px; }
        
        h1 {
            font-size: 2.5rem;
            background: linear-gradient(90deg, #00d4ff, #7c3aed);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .tagline {
            color: #888;
            margin-top: 10px;
        }
        
        /* Upload Area */
        .upload-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(20px);
            border-radius: 24px;
            padding: 40px;
            border: 2px dashed rgba(255, 255, 255, 0.2);
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
            margin-bottom: 30px;
        }
        
        .upload-card:hover, .upload-card.dragover {
            border-color: #7c3aed;
            background: rgba(124, 58, 237, 0.1);
        }
        
        .upload-icon {
            font-size: 3rem;
            margin-bottom: 20px;
        }
        
        .upload-text {
            font-size: 1.2rem;
            margin-bottom: 10px;
        }
        
        .upload-hint {
            color: #666;
            font-size: 0.9rem;
        }
        
        #file-input { display: none; }
        
        .btn {
            display: inline-block;
            padding: 14px 28px;
            background: linear-gradient(135deg, #7c3aed, #00d4ff);
            border: none;
            border-radius: 12px;
            color: #fff;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            margin-top: 20px;
            transition: all 0.3s ease;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(124, 58, 237, 0.4);
        }
        
        /* Progress */
        .progress-container {
            display: none;
            margin-top: 20px;
        }
        
        .progress-bar {
            height: 8px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
            overflow: hidden;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #7c3aed, #00d4ff);
            width: 0%;
            transition: width 0.3s ease;
        }
        
        /* Result */
        .result {
            display: none;
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: 16px;
            padding: 24px;
            margin-top: 20px;
        }
        
        .result.show { display: block; }
        
        .result-title {
            color: #10b981;
            font-weight: 600;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .result-link {
            display: flex;
            align-items: center;
            gap: 12px;
            background: rgba(0, 0, 0, 0.3);
            padding: 16px;
            border-radius: 10px;
        }
        
        .result-link a {
            color: #00d4ff;
            text-decoration: none;
            font-family: monospace;
            word-break: break-all;
            flex: 1;
        }
        
        .copy-btn {
            padding: 8px 16px;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            color: #fff;
            cursor: pointer;
            font-size: 0.85rem;
        }
        
        .result-info {
            margin-top: 15px;
            font-size: 0.85rem;
            color: #888;
        }
        
        /* Files List */
        .files-section {
            margin-top: 40px;
        }
        
        .section-title {
            color: #888;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 15px;
        }
        
        .file-item {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.3s ease;
        }
        
        .file-item:hover {
            background: rgba(255, 255, 255, 0.06);
        }
        
        .file-info {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .file-icon { font-size: 1.5rem; }
        
        .file-name {
            font-weight: 500;
            margin-bottom: 4px;
        }
        
        .file-meta {
            font-size: 0.8rem;
            color: #666;
        }
        
        .file-actions a {
            color: #00d4ff;
            text-decoration: none;
            padding: 8px 16px;
            background: rgba(0, 212, 255, 0.1);
            border-radius: 8px;
            font-size: 0.85rem;
        }
        
        /* API Section */
        .api-section {
            margin-top: 40px;
            padding-top: 30px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .endpoint {
            background: rgba(0, 0, 0, 0.3);
            padding: 10px 16px;
            border-radius: 8px;
            margin: 8px 0;
            font-family: monospace;
            font-size: 0.9rem;
        }
        
        .method {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
            margin-right: 10px;
        }
        
        .method.post { background: #7c3aed; }
        .method.get { background: #00d4ff; color: #000; }
        
        /* Docker Banner */
        .docker-banner {
            margin-top: 40px;
            background: linear-gradient(135deg, rgba(0, 123, 255, 0.1), rgba(0, 123, 255, 0.05));
            border: 1px solid rgba(0, 123, 255, 0.3);
            border-radius: 12px;
            padding: 20px;
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .docker-banner .emoji { font-size: 2rem; }
        .docker-banner p { color: #888; font-size: 0.9rem; }
        .docker-banner strong { color: #00d4ff; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="logo">📁</div>
            <h1>{{ app_name }}</h1>
            <p class="tagline">Upload and share files with temporary links</p>
        </header>
        
        <div class="upload-card" id="upload-area">
            <div class="upload-icon">⬆️</div>
            <div class="upload-text">Drag & drop files here</div>
            <div class="upload-hint">or click to browse (max {{ max_size }})</div>
            <input type="file" id="file-input" multiple>
            
            <div class="progress-container" id="progress">
                <div class="progress-bar">
                    <div class="progress-fill" id="progress-fill"></div>
                </div>
            </div>
            
            <div class="result" id="result">
                <div class="result-title">✅ File uploaded successfully!</div>
                <div class="result-link">
                    <a href="#" id="download-link" target="_blank"></a>
                    <button class="copy-btn" onclick="copyLink()">Copy</button>
                </div>
                <div class="result-info" id="result-info"></div>
            </div>
        </div>
        
        {% if files %}
        <div class="files-section">
            <div class="section-title">Recent Uploads</div>
            {% for file in files %}
            <div class="file-item">
                <div class="file-info">
                    <span class="file-icon">📄</span>
                    <div>
                        <div class="file-name">{{ file.original_name }}</div>
                        <div class="file-meta">{{ file.size }} • Expires in {{ file.expires_in }}</div>
                    </div>
                </div>
                <div class="file-actions">
                    <a href="/download/{{ file.id }}">Download</a>
                </div>
            </div>
            {% endfor %}
        </div>
        {% endif %}
        
        <div class="api-section">
            <div class="section-title">API Endpoints</div>
            <div class="endpoint">
                <span class="method post">POST</span>/api/upload - Upload a file
            </div>
            <div class="endpoint">
                <span class="method get">GET</span>/api/files - List all files
            </div>
            <div class="endpoint">
                <span class="method get">GET</span>/download/&lt;id&gt; - Download a file
            </div>
            <div class="endpoint">
                <span class="method get">GET</span>/health - Health check
            </div>
        </div>
        
        <div class="docker-banner">
            <span class="emoji">🐳</span>
            <p><strong>Docker Challenge:</strong> Use volumes to persist uploads! Try adding MinIO for S3-compatible storage.</p>
        </div>
    </div>
    
    <script>
        const uploadArea = document.getElementById('upload-area');
        const fileInput = document.getElementById('file-input');
        const progress = document.getElementById('progress');
        const progressFill = document.getElementById('progress-fill');
        const result = document.getElementById('result');
        
        // Click to upload
        uploadArea.addEventListener('click', () => fileInput.click());
        
        // Drag and drop
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            handleFiles(e.dataTransfer.files);
        });
        
        fileInput.addEventListener('change', (e) => {
            handleFiles(e.target.files);
        });
        
        async function handleFiles(files) {
            if (files.length === 0) return;
            
            const file = files[0];
            const formData = new FormData();
            formData.append('file', file);
            
            progress.style.display = 'block';
            result.classList.remove('show');
            
            try {
                const response = await fetch('/api/upload', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.success) {
                    progressFill.style.width = '100%';
                    document.getElementById('download-link').href = data.download_url;
                    document.getElementById('download-link').textContent = data.download_url;
                    document.getElementById('result-info').textContent = 
                        `${data.original_name} (${data.size}) • Expires in ${data.expires_in}`;
                    result.classList.add('show');
                } else {
                    alert('Upload failed: ' + data.error);
                }
            } catch (error) {
                alert('Upload failed: ' + error.message);
            }
            
            setTimeout(() => {
                progress.style.display = 'none';
                progressFill.style.width = '0%';
            }, 1000);
        }
        
        function copyLink() {
            const link = document.getElementById('download-link').href;
            navigator.clipboard.writeText(link);
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
    """Home page with upload form"""
    # Get recent files
    files = []
    for file_id, info in list(files_db.items())[-5:]:
        if not is_file_expired(info):
            expires = datetime.fromisoformat(info['expires_at'])
            time_left = expires - datetime.now()
            hours = int(time_left.total_seconds() / 3600)
            
            files.append({
                'id': file_id,
                'original_name': info['original_name'],
                'size': format_file_size(info['size']),
                'expires_in': f"{hours}h" if hours > 0 else "< 1h"
            })
    
    return render_template_string(
        HOME_TEMPLATE,
        app_name=APP_NAME,
        max_size=format_file_size(MAX_FILE_SIZE),
        files=reversed(files)
    )


@app.route('/download/<file_id>')
def download_file(file_id):
    """Download a file by ID"""
    if file_id not in files_db:
        abort(404)
    
    file_info = files_db[file_id]
    
    if is_file_expired(file_info):
        # Clean up expired file
        try:
            os.remove(file_info['path'])
        except:
            pass
        del files_db[file_id]
        abort(404)
    
    return send_file(
        file_info['path'],
        download_name=file_info['original_name'],
        as_attachment=True
    )


# =============================================================================
# API ROUTES
# =============================================================================

@app.route('/api/upload', methods=['POST'])
def api_upload():
    """
    Upload a file via API
    
    Request: multipart/form-data with 'file' field
    Response: {"success": true, "download_url": "...", ...}
    """
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400
    
    # Check file size
    file.seek(0, 2)
    size = file.tell()
    file.seek(0)
    
    if size > MAX_FILE_SIZE:
        return jsonify({
            'success': False, 
            'error': f'File too large. Max size: {format_file_size(MAX_FILE_SIZE)}'
        }), 400
    
    # Generate file ID and save
    file_id = generate_file_id()
    extension = get_file_extension(file.filename)
    stored_filename = f"{file_id}{extension}"
    file_path = os.path.join(UPLOAD_FOLDER, stored_filename)
    
    file.save(file_path)
    
    # Store metadata
    expires_at = datetime.now() + timedelta(hours=EXPIRY_HOURS)
    files_db[file_id] = {
        'original_name': file.filename,
        'stored_name': stored_filename,
        'path': file_path,
        'size': size,
        'uploaded_at': datetime.now().isoformat(),
        'expires_at': expires_at.isoformat()
    }
    
    download_url = f"{BASE_URL}/download/{file_id}"
    
    return jsonify({
        'success': True,
        'file_id': file_id,
        'download_url': download_url,
        'original_name': file.filename,
        'size': format_file_size(size),
        'expires_at': expires_at.isoformat(),
        'expires_in': f"{EXPIRY_HOURS} hours"
    })


@app.route('/api/files')
def api_list_files():
    """List all uploaded files"""
    files = []
    for file_id, info in files_db.items():
        if not is_file_expired(info):
            files.append({
                'id': file_id,
                'original_name': info['original_name'],
                'size': format_file_size(info['size']),
                'download_url': f"{BASE_URL}/download/{file_id}",
                'expires_at': info['expires_at']
            })
    
    return jsonify({'files': files, 'total': len(files)})


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'app': APP_NAME,
        'timestamp': datetime.now().isoformat(),
        'total_files': len(files_db),
        'upload_folder': UPLOAD_FOLDER
    })


# =============================================================================
# RUN THE APP
# =============================================================================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    debug = os.environ.get('FLASK_DEBUG', 'true').lower() == 'true'
    
    print(f"""
    ╔══════════════════════════════════════════════════════════════╗
    ║                    📁 FILE SHARE                             ║
    ║══════════════════════════════════════════════════════════════║
    ║  Running at: http://localhost:{port}                          ║
    ║  Upload folder: {UPLOAD_FOLDER}                               
    ║  Max file size: {format_file_size(MAX_FILE_SIZE)}                                    ║
    ║                                                              ║
    ║  DOCKER CHALLENGE:                                           ║
    ║  1. Use volumes to persist uploads!                          ║
    ║  2. Add MinIO for S3-compatible storage                      ║
    ║  3. Add Nginx for serving files                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    app.run(host='0.0.0.0', port=port, debug=debug)
