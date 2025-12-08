# 📁 File Share - Docker Practice Project

A file upload/download service with temporary sharing links. Great for learning Docker volumes and storage concepts.

## 🎯 Your Mission

Containerize this application and learn about **persistent storage with Docker volumes**.

## 📁 Project Structure

```
file-share/
├── app.py              # Flask file sharing application
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
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python app.py
```

Visit http://localhost:5002 and try uploading a file!

---

## 🐳 Docker Challenges

### Level 1: Basic Dockerfile ⭐

Create a `Dockerfile`:
- [ ] Use Python 3.11 slim
- [ ] Create an uploads directory
- [ ] Run on port 5002

---

### Level 2: Persistent Volumes ⭐⭐ (CRITICAL!)

Without volumes, files are **lost when the container restarts!**

- [ ] Create a named volume for uploads
- [ ] Mount it to `/app/uploads`
- [ ] Test: upload a file, restart container, verify file exists

<details>
<summary>💡 Hint</summary>

```yaml
services:
  fileshare:
    build: .
    ports:
      - "5002:5002"
    volumes:
      - uploads:/app/uploads
    environment:
      - UPLOAD_FOLDER=/app/uploads

volumes:
  uploads:
```
</details>

---

### Level 3: Add MinIO (S3-Compatible Storage) ⭐⭐⭐⭐

MinIO is a self-hosted S3-compatible object storage:
- [ ] Add MinIO service to docker-compose
- [ ] Configure Flask to use MinIO
- [ ] Access MinIO console at port 9001

<details>
<summary>💡 Hint</summary>

```yaml
  minio:
    image: minio/minio
    ports:
      - "9000:9000"   # API
      - "9001:9001"   # Console
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    command: server /data --console-address ":9001"
    volumes:
      - minio_data:/data

volumes:
  minio_data:
```
</details>

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Upload UI |
| POST | `/api/upload` | Upload a file |
| GET | `/api/files` | List all files |
| GET | `/download/<id>` | Download a file |
| GET | `/health` | Health check |

---

## 🏆 Skills You'll Learn

- ✅ Docker volumes for persistence
- ✅ Data management in containers
- ✅ Object storage concepts
- ✅ File handling in containerized apps

Happy Containerizing! 🐳
