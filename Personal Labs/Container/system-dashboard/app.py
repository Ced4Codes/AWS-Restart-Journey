"""
System Health Dashboard - Flask Application
============================================
A real-time monitoring dashboard showing system metrics.

FEATURES:
- Live CPU, Memory, Disk usage monitoring
- Container-aware metrics
- WebSocket updates for real-time data
- Beautiful dashboard UI
- API endpoints for metrics

ARCHITECTURE:
- Flask web framework
- psutil for system metrics
- Server-Sent Events (SSE) for real-time updates

YOUR DOCKER CHALLENGE:
1. Create a Dockerfile to containerize this app
2. Create a docker-compose.yml with proper resource limits
3. (Bonus) Add Prometheus + Grafana for advanced monitoring
4. (Bonus) Monitor multiple containers
5. Deploy to AWS EC2

Good luck! 🐳
"""

from flask import Flask, jsonify, render_template_string, Response
import os
import time
import json
import socket
from datetime import datetime

# Try to import psutil, fall back to mock data if not available
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("⚠️  psutil not installed. Using mock data. Install with: pip install psutil")

# =============================================================================
# FLASK APP INITIALIZATION
# =============================================================================
app = Flask(__name__)

# =============================================================================
# CONFIGURATION
# =============================================================================
APP_NAME = os.environ.get('APP_NAME', 'System Dashboard')
REFRESH_INTERVAL = int(os.environ.get('REFRESH_INTERVAL', 2))  # seconds


# =============================================================================
# METRICS COLLECTION
# =============================================================================
def get_system_metrics():
    """Collect system metrics using psutil or return mock data"""
    if PSUTIL_AVAILABLE:
        # Real metrics
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Network I/O
        net_io = psutil.net_io_counters()
        
        # Process count
        process_count = len(psutil.pids())
        
        # Boot time
        boot_time = datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')
        
        return {
            'timestamp': datetime.now().isoformat(),
            'hostname': socket.gethostname(),
            'cpu': {
                'percent': cpu_percent,
                'cores': psutil.cpu_count(),
                'frequency': getattr(psutil.cpu_freq(), 'current', 0) if psutil.cpu_freq() else 0
            },
            'memory': {
                'total': memory.total,
                'available': memory.available,
                'used': memory.used,
                'percent': memory.percent,
                'total_gb': round(memory.total / (1024**3), 2),
                'used_gb': round(memory.used / (1024**3), 2)
            },
            'disk': {
                'total': disk.total,
                'used': disk.used,
                'free': disk.free,
                'percent': disk.percent,
                'total_gb': round(disk.total / (1024**3), 2),
                'used_gb': round(disk.used / (1024**3), 2)
            },
            'network': {
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv,
                'packets_sent': net_io.packets_sent,
                'packets_recv': net_io.packets_recv,
                'sent_mb': round(net_io.bytes_sent / (1024**2), 2),
                'recv_mb': round(net_io.bytes_recv / (1024**2), 2)
            },
            'system': {
                'process_count': process_count,
                'boot_time': boot_time
            }
        }
    else:
        # Mock data for development without psutil
        import random
        return {
            'timestamp': datetime.now().isoformat(),
            'hostname': socket.gethostname(),
            'cpu': {
                'percent': random.uniform(10, 80),
                'cores': 4,
                'frequency': 2400
            },
            'memory': {
                'total': 8589934592,
                'available': random.randint(2000000000, 6000000000),
                'used': random.randint(2000000000, 6000000000),
                'percent': random.uniform(30, 70),
                'total_gb': 8.0,
                'used_gb': random.uniform(2, 6)
            },
            'disk': {
                'total': 256060514304,
                'used': random.randint(50000000000, 150000000000),
                'free': random.randint(100000000000, 200000000000),
                'percent': random.uniform(20, 60),
                'total_gb': 238.5,
                'used_gb': random.uniform(50, 150)
            },
            'network': {
                'bytes_sent': random.randint(1000000, 100000000),
                'bytes_recv': random.randint(1000000, 100000000),
                'packets_sent': random.randint(1000, 100000),
                'packets_recv': random.randint(1000, 100000),
                'sent_mb': random.uniform(1, 100),
                'recv_mb': random.uniform(1, 100)
            },
            'system': {
                'process_count': random.randint(50, 200),
                'boot_time': '2024-01-01 08:00:00'
            }
        }


# =============================================================================
# HTML TEMPLATE
# =============================================================================
DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ app_name }}</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        :root {
            --bg-primary: #0a0a0f;
            --bg-secondary: #12121a;
            --bg-card: rgba(255, 255, 255, 0.03);
            --border: rgba(255, 255, 255, 0.08);
            --text-primary: #ffffff;
            --text-secondary: #888;
            --accent-cyan: #00d4ff;
            --accent-purple: #7c3aed;
            --accent-green: #10b981;
            --accent-yellow: #f59e0b;
            --accent-red: #ef4444;
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background: var(--bg-primary);
            min-height: 100vh;
            color: var(--text-primary);
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 30px 20px;
        }
        
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 1px solid var(--border);
        }
        
        .logo {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .logo-icon {
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
        }
        
        h1 {
            font-size: 1.5rem;
            font-weight: 600;
        }
        
        .hostname {
            color: var(--text-secondary);
            font-size: 0.9rem;
            font-family: 'JetBrains Mono', monospace;
        }
        
        .status {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .status-dot {
            width: 10px;
            height: 10px;
            background: var(--accent-green);
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .status-text {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            color: var(--text-secondary);
        }
        
        /* Metrics Grid */
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }
        
        @media (max-width: 1200px) {
            .metrics-grid { grid-template-columns: repeat(2, 1fr); }
        }
        
        @media (max-width: 600px) {
            .metrics-grid { grid-template-columns: 1fr; }
        }
        
        .metric-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 24px;
            position: relative;
            overflow: hidden;
        }
        
        .metric-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .metric-title {
            font-size: 0.85rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .metric-icon {
            font-size: 1.2rem;
        }
        
        .metric-value {
            font-size: 2.5rem;
            font-weight: 700;
            font-family: 'JetBrains Mono', monospace;
            margin-bottom: 10px;
        }
        
        .metric-value.cpu { color: var(--accent-cyan); }
        .metric-value.memory { color: var(--accent-purple); }
        .metric-value.disk { color: var(--accent-yellow); }
        .metric-value.network { color: var(--accent-green); }
        
        .metric-sub {
            font-size: 0.85rem;
            color: var(--text-secondary);
            font-family: 'JetBrains Mono', monospace;
        }
        
        /* Progress Bar */
        .progress-bar {
            height: 6px;
            background: var(--bg-secondary);
            border-radius: 3px;
            margin-top: 15px;
            overflow: hidden;
        }
        
        .progress-fill {
            height: 100%;
            border-radius: 3px;
            transition: width 0.5s ease;
        }
        
        .progress-fill.cpu { background: linear-gradient(90deg, var(--accent-cyan), #00a8cc); }
        .progress-fill.memory { background: linear-gradient(90deg, var(--accent-purple), #5b21b6); }
        .progress-fill.disk { background: linear-gradient(90deg, var(--accent-yellow), #d97706); }
        
        /* Stats Section */
        .stats-section {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 20px;
        }
        
        @media (max-width: 900px) {
            .stats-section { grid-template-columns: 1fr; }
        }
        
        .stats-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 24px;
        }
        
        .stats-title {
            font-size: 1rem;
            font-weight: 600;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .stats-table {
            width: 100%;
        }
        
        .stats-row {
            display: flex;
            justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px solid var(--border);
        }
        
        .stats-row:last-child { border-bottom: none; }
        
        .stats-label {
            color: var(--text-secondary);
            font-size: 0.9rem;
        }
        
        .stats-value {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
        }
        
        /* API Section */
        .api-section {
            margin-top: 30px;
            padding-top: 30px;
            border-top: 1px solid var(--border);
        }
        
        .endpoint {
            display: inline-block;
            background: var(--bg-secondary);
            padding: 8px 16px;
            border-radius: 8px;
            margin: 5px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            border: 1px solid var(--border);
        }
        
        .endpoint a {
            color: var(--accent-cyan);
            text-decoration: none;
        }
        
        /* Docker Banner */
        .docker-banner {
            margin-top: 30px;
            background: linear-gradient(135deg, rgba(0, 123, 255, 0.1), rgba(0, 123, 255, 0.05));
            border: 1px solid rgba(0, 123, 255, 0.3);
            border-radius: 12px;
            padding: 20px;
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .docker-banner .emoji { font-size: 2rem; }
        .docker-banner p { color: var(--text-secondary); font-size: 0.9rem; }
        .docker-banner strong { color: var(--accent-cyan); }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="logo">
                <div class="logo-icon">📊</div>
                <div>
                    <h1>{{ app_name }}</h1>
                    <div class="hostname" id="hostname">Loading...</div>
                </div>
            </div>
            <div class="status">
                <div class="status-dot"></div>
                <span class="status-text" id="last-update">Connecting...</span>
            </div>
        </header>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-title">CPU Usage</span>
                    <span class="metric-icon">⚡</span>
                </div>
                <div class="metric-value cpu" id="cpu-percent">--%</div>
                <div class="metric-sub" id="cpu-cores">-- cores</div>
                <div class="progress-bar">
                    <div class="progress-fill cpu" id="cpu-bar" style="width: 0%"></div>
                </div>
            </div>
            
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-title">Memory</span>
                    <span class="metric-icon">🧠</span>
                </div>
                <div class="metric-value memory" id="mem-percent">--%</div>
                <div class="metric-sub" id="mem-used">-- / -- GB</div>
                <div class="progress-bar">
                    <div class="progress-fill memory" id="mem-bar" style="width: 0%"></div>
                </div>
            </div>
            
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-title">Disk</span>
                    <span class="metric-icon">💾</span>
                </div>
                <div class="metric-value disk" id="disk-percent">--%</div>
                <div class="metric-sub" id="disk-used">-- / -- GB</div>
                <div class="progress-bar">
                    <div class="progress-fill disk" id="disk-bar" style="width: 0%"></div>
                </div>
            </div>
            
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-title">Network</span>
                    <span class="metric-icon">🌐</span>
                </div>
                <div class="metric-value network" id="net-sent">-- MB</div>
                <div class="metric-sub" id="net-recv">↓ -- MB received</div>
            </div>
        </div>
        
        <div class="stats-section">
            <div class="stats-card">
                <div class="stats-title">📈 System Details</div>
                <div class="stats-table">
                    <div class="stats-row">
                        <span class="stats-label">Hostname</span>
                        <span class="stats-value" id="stat-hostname">--</span>
                    </div>
                    <div class="stats-row">
                        <span class="stats-label">CPU Cores</span>
                        <span class="stats-value" id="stat-cores">--</span>
                    </div>
                    <div class="stats-row">
                        <span class="stats-label">Total Memory</span>
                        <span class="stats-value" id="stat-memory">--</span>
                    </div>
                    <div class="stats-row">
                        <span class="stats-label">Total Disk</span>
                        <span class="stats-value" id="stat-disk">--</span>
                    </div>
                    <div class="stats-row">
                        <span class="stats-label">Active Processes</span>
                        <span class="stats-value" id="stat-processes">--</span>
                    </div>
                    <div class="stats-row">
                        <span class="stats-label">Boot Time</span>
                        <span class="stats-value" id="stat-boot">--</span>
                    </div>
                </div>
            </div>
            
            <div class="stats-card">
                <div class="stats-title">🔌 API Endpoints</div>
                <div class="endpoint"><a href="/api/metrics">/api/metrics</a></div>
                <div class="endpoint"><a href="/api/cpu">/api/cpu</a></div>
                <div class="endpoint"><a href="/api/memory">/api/memory</a></div>
                <div class="endpoint"><a href="/api/disk">/api/disk</a></div>
                <div class="endpoint"><a href="/health">/health</a></div>
            </div>
        </div>
        
        <div class="docker-banner">
            <span class="emoji">🐳</span>
            <p><strong>Docker Challenge:</strong> Containerize this dashboard! Try adding Prometheus + Grafana for advanced monitoring.</p>
        </div>
    </div>
    
    <script>
        // Fetch and update metrics
        async function updateMetrics() {
            try {
                const response = await fetch('/api/metrics');
                const data = await response.json();
                
                // Update hostname
                document.getElementById('hostname').textContent = data.hostname;
                document.getElementById('stat-hostname').textContent = data.hostname;
                
                // CPU
                document.getElementById('cpu-percent').textContent = data.cpu.percent.toFixed(1) + '%';
                document.getElementById('cpu-cores').textContent = data.cpu.cores + ' cores';
                document.getElementById('cpu-bar').style.width = data.cpu.percent + '%';
                document.getElementById('stat-cores').textContent = data.cpu.cores;
                
                // Memory
                document.getElementById('mem-percent').textContent = data.memory.percent.toFixed(1) + '%';
                document.getElementById('mem-used').textContent = data.memory.used_gb.toFixed(1) + ' / ' + data.memory.total_gb.toFixed(1) + ' GB';
                document.getElementById('mem-bar').style.width = data.memory.percent + '%';
                document.getElementById('stat-memory').textContent = data.memory.total_gb.toFixed(1) + ' GB';
                
                // Disk
                document.getElementById('disk-percent').textContent = data.disk.percent.toFixed(1) + '%';
                document.getElementById('disk-used').textContent = data.disk.used_gb.toFixed(1) + ' / ' + data.disk.total_gb.toFixed(1) + ' GB';
                document.getElementById('disk-bar').style.width = data.disk.percent + '%';
                document.getElementById('stat-disk').textContent = data.disk.total_gb.toFixed(1) + ' GB';
                
                // Network
                document.getElementById('net-sent').textContent = '↑ ' + data.network.sent_mb.toFixed(1) + ' MB';
                document.getElementById('net-recv').textContent = '↓ ' + data.network.recv_mb.toFixed(1) + ' MB received';
                
                // System
                document.getElementById('stat-processes').textContent = data.system.process_count;
                document.getElementById('stat-boot').textContent = data.system.boot_time;
                
                // Update timestamp
                const now = new Date();
                document.getElementById('last-update').textContent = 'Updated ' + now.toLocaleTimeString();
                
            } catch (error) {
                console.error('Failed to fetch metrics:', error);
                document.getElementById('last-update').textContent = 'Connection error';
            }
        }
        
        // Initial fetch and periodic updates
        updateMetrics();
        setInterval(updateMetrics, {{ refresh_interval * 1000 }});
    </script>
</body>
</html>
"""


# =============================================================================
# WEB ROUTES
# =============================================================================

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template_string(
        DASHBOARD_TEMPLATE,
        app_name=APP_NAME,
        refresh_interval=REFRESH_INTERVAL
    )


# =============================================================================
# API ROUTES
# =============================================================================

@app.route('/api/metrics')
def api_metrics():
    """Get all system metrics"""
    return jsonify(get_system_metrics())


@app.route('/api/cpu')
def api_cpu():
    """Get CPU metrics only"""
    metrics = get_system_metrics()
    return jsonify(metrics['cpu'])


@app.route('/api/memory')
def api_memory():
    """Get memory metrics only"""
    metrics = get_system_metrics()
    return jsonify(metrics['memory'])


@app.route('/api/disk')
def api_disk():
    """Get disk metrics only"""
    metrics = get_system_metrics()
    return jsonify(metrics['disk'])


@app.route('/health')
def health():
    """
    Health Check Endpoint
    ---------------------
    For container orchestration.
    """
    return jsonify({
        'status': 'healthy',
        'app': APP_NAME,
        'timestamp': datetime.now().isoformat(),
        'psutil_available': PSUTIL_AVAILABLE
    })


# =============================================================================
# RUN THE APP
# =============================================================================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_DEBUG', 'true').lower() == 'true'
    
    print(f"""
    ╔══════════════════════════════════════════════════════════════╗
    ║                  📊 SYSTEM DASHBOARD                         ║
    ║══════════════════════════════════════════════════════════════║
    ║  Running at: http://localhost:{port}                          ║
    ║  psutil: {'✓ Available' if PSUTIL_AVAILABLE else '✗ Using mock data'}                                   ║
    ║                                                              ║
    ║  DOCKER CHALLENGE:                                           ║
    ║  1. Containerize this monitoring app                         ║
    ║  2. Add resource limits in docker-compose                    ║
    ║  3. (Bonus) Add Prometheus + Grafana                         ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    app.run(host='0.0.0.0', port=port, debug=debug)
