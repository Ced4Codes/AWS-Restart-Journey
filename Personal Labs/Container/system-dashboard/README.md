# 📊 System Health Dashboard - Docker Practice Project

A real-time system monitoring dashboard showing CPU, memory, disk, and network metrics. Perfect for learning Docker containerization and observability concepts.

## 🎯 Your Mission

Containerize this monitoring application and learn about container resource management.

## 📁 Project Structure

```
system-dashboard/
├── app.py              # Flask dashboard application
├── requirements.txt    # Python dependencies
├── README.md           # You're reading it!
├── .env.example        # Environment variables template
│
# ═══════════ YOUR DOCKER FILES (create these!) ═══════════
├── Dockerfile          # TODO: Create this!
├── docker-compose.yml  # TODO: Create this!
└── .dockerignore       # TODO: Create this!
```

## 🚀 Quick Test (Without Docker)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Visit http://localhost:5001 to see the dashboard!

---

## 🐳 Docker Challenges

### Level 1: Basic Dockerfile ⭐

Create a `Dockerfile` that:
- [ ] Uses Python 3.11 slim image
- [ ] Installs psutil (needs build tools!)
- [ ] Runs on port 5001

<details>
<summary>💡 Hint: psutil needs compilation</summary>

```dockerfile
FROM python:3.11-slim

# psutil needs gcc for compilation
RUN apt-get update && apt-get install -y gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 5001
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app:app"]
```
</details>

---

### Level 2: Resource Limits ⭐⭐

Add resource constraints in docker-compose:
- [ ] Limit CPU to 50%
- [ ] Limit memory to 256MB
- [ ] Watch how the dashboard shows these limits!

<details>
<summary>💡 Hint</summary>

```yaml
services:
  dashboard:
    build: .
    ports:
      - "5001:5001"
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 256M
        reservations:
          cpus: '0.25'
          memory: 128M
```
</details>

---

### Level 3: Prometheus + Grafana ⭐⭐⭐⭐

Add a full monitoring stack:
- [ ] Add Prometheus to scrape metrics
- [ ] Add Grafana for visualization
- [ ] Create a dashboard showing container metrics

---

## 🌐 API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/` | Dashboard UI |
| `/api/metrics` | All system metrics (JSON) |
| `/api/cpu` | CPU metrics only |
| `/api/memory` | Memory metrics only |
| `/api/disk` | Disk metrics only |
| `/health` | Health check |

---

## 🏆 Skills You'll Learn

- ✅ Container resource limits
- ✅ Build dependencies (gcc for psutil)
- ✅ Real-time monitoring concepts
- ✅ Observability fundamentals

Happy Containerizing! 🐳
