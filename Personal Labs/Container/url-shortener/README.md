# 🔗 URL Shortener - Docker Practice Project

A fully functional URL shortening service built with Flask. This project is designed for **learning Docker containerization** - the application code is complete, but you need to containerize it!

## 🎯 Your Mission

Create Docker configuration to containerize this application. This is a hands-on project to practice real-world DevOps skills.

## 📁 Project Structure

```
url-shortener/
├── app.py              # Flask application (complete!)
├── requirements.txt    # Python dependencies
├── README.md           # You're reading it!
├── .env.example        # Environment variables template
│
# ═══════════ YOUR DOCKER FILES (create these!) ═══════════
├── Dockerfile          # TODO: Create this!
├── docker-compose.yml  # TODO: Create this!
├── .dockerignore       # TODO: Create this!
└── nginx/              # BONUS: Nginx reverse proxy config
    └── nginx.conf
```

## 🚀 Quick Test (Without Docker)

Before containerizing, test that the app works:

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Visit http://localhost:5000 to see it working!

---

## 🐳 Docker Challenges

### Level 1: Basic Dockerfile ⭐

Create a `Dockerfile` that:
- [ ] Uses Python 3.11 slim image
- [ ] Sets up a working directory
- [ ] Copies and installs requirements
- [ ] Copies application code
- [ ] Exposes port 5000
- [ ] Runs the app with gunicorn

<details>
<summary>💡 Hints</summary>

```dockerfile
# Start with a Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (better caching!)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port
EXPOSE 5000

# Run with gunicorn (production server)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```
</details>

---

### Level 2: Docker Compose ⭐⭐

Create a `docker-compose.yml` that:
- [ ] Builds the Flask app from Dockerfile
- [ ] Sets environment variables
- [ ] Maps ports correctly
- [ ] Adds a health check
- [ ] Uses a restart policy

<details>
<summary>💡 Hints</summary>

```yaml
version: "3.8"

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - APP_NAME=URL Shortener
      - BASE_URL=http://localhost:5000
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped
```
</details>

---

### Level 3: Add PostgreSQL ⭐⭐⭐

Upgrade to persistent storage:
- [ ] Add PostgreSQL service to docker-compose
- [ ] Configure database environment variables
- [ ] Use a named volume for data persistence
- [ ] Make the Flask app wait for the database

<details>
<summary>💡 Hints</summary>

```yaml
services:
  web:
    # ... your flask config ...
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/urlshortener

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: urlshortener
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d urlshortener"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```
</details>

---

### Level 4: Add Redis Caching ⭐⭐⭐⭐

Add a caching layer:
- [ ] Add Redis service to docker-compose
- [ ] Link the Flask app to Redis
- [ ] Redis should start before the Flask app

<details>
<summary>💡 Hints</summary>

```yaml
services:
  web:
    depends_on:
      - db
      - redis
    environment:
      - REDIS_URL=redis://redis:6379/0

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  redis_data:
```
</details>

---

### Level 5: Nginx Reverse Proxy ⭐⭐⭐⭐⭐

Production-ready setup:
- [ ] Add Nginx as reverse proxy
- [ ] Nginx handles port 80 traffic
- [ ] Flask runs on internal network only
- [ ] Configure SSL (stretch goal)

<details>
<summary>💡 Hints</summary>

Create `nginx/nginx.conf`:
```nginx
upstream flask {
    server web:5000;
}

server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://flask;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Add to docker-compose:
```yaml
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - web
```
</details>

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home page with URL form |
| GET | `/<code>` | Redirect to original URL |
| POST | `/api/shorten` | Create short URL (JSON) |
| GET | `/api/stats/<code>` | Get URL statistics |
| GET | `/api/urls` | List all URLs |
| GET | `/health` | Health check |

### Example API Usage

```bash
# Shorten a URL
curl -X POST http://localhost:5000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com/very/long/url"}'

# Get stats
curl http://localhost:5000/api/stats/abc123
```

---

## ☁️ AWS EC2 Deployment

After completing the Docker challenges, deploy to AWS:

1. Launch an EC2 instance (Amazon Linux 2023 or Ubuntu)
2. Install Docker and Docker Compose
3. Clone your repo
4. Run `docker-compose up -d`
5. Access via EC2 public IP!

---

## 📋 Checklist

- [ ] Dockerfile created and working
- [ ] docker-compose.yml with Flask service
- [ ] .dockerignore to exclude unnecessary files
- [ ] PostgreSQL added for persistence
- [ ] Redis added for caching
- [ ] Nginx reverse proxy configured
- [ ] Deployed to AWS EC2
- [ ] README updated with your learnings

---

## 🏆 What Recruiters Will See

When you complete this project, you'll demonstrate:
- ✅ Docker containerization skills
- ✅ Multi-container orchestration
- ✅ Database integration
- ✅ Production best practices (health checks, restart policies)
- ✅ AWS deployment experience
- ✅ Understanding of reverse proxies

---

## 🎓 Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Guide](https://docs.docker.com/compose/)
- [PostgreSQL Docker Image](https://hub.docker.com/_/postgres)
- [Redis Docker Image](https://hub.docker.com/_/redis)
- [Nginx Docker Image](https://hub.docker.com/_/nginx)

---

Happy Containerizing! 🐳

*Fork this repo, complete the challenges, and add it to your portfolio!*
