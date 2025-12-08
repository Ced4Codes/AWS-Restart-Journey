# Task Management API 📋

A **RESTful API** for managing tasks with categories and priorities, built with Spring Boot for Docker containerization practice.

## 🎯 What You'll Learn

| Skill | Technology |
|-------|------------|
| REST API Development | Spring Boot, Spring MVC |
| Data Persistence | Spring Data JPA, PostgreSQL |
| API Documentation | OpenAPI/Swagger |
| Containerization | Docker, Docker Compose |
| Health Monitoring | Spring Actuator |

## 🚀 Quick Start

### Run Locally (Development)
```bash
# Using Maven Wrapper
./mvnw spring-boot:run

# Or with Maven installed
mvn spring-boot:run
```

### Access Points
| Endpoint | Description |
|----------|-------------|
| http://localhost:8080/swagger-ui.html | API Documentation |
| http://localhost:8080/api/v1/tasks | Task endpoints |
| http://localhost:8080/actuator/health | Health check |
| http://localhost:8080/h2-console | H2 Database console |

## 📡 API Endpoints

### Tasks CRUD
```
GET    /api/v1/tasks          - Get all tasks
GET    /api/v1/tasks/{id}     - Get task by ID
POST   /api/v1/tasks          - Create new task
PUT    /api/v1/tasks/{id}     - Update task
DELETE /api/v1/tasks/{id}     - Delete task
```

### Task Operations
```
PATCH  /api/v1/tasks/{id}/complete  - Mark as completed
PATCH  /api/v1/tasks/{id}/archive   - Archive task
```

### Filtering & Search
```
GET  /api/v1/tasks/status/{status}      - Filter by status
GET  /api/v1/tasks/priority/{priority}  - Filter by priority
GET  /api/v1/tasks/category/{category}  - Filter by category
GET  /api/v1/tasks/search?q=query       - Search by title
GET  /api/v1/tasks/overdue              - Get overdue tasks
GET  /api/v1/tasks/due-today            - Get tasks due today
GET  /api/v1/tasks/stats                - Get statistics
```

---

## 🐳 Docker Challenges

Progressive challenges to learn Docker containerization:

### Level 1: Basic Dockerfile ⭐
Create a Dockerfile that builds and runs the application.

<details>
<summary>💡 Hints</summary>

- Use multi-stage build (builder + runtime)
- Base image: `eclipse-temurin:17-jdk-alpine` for building
- Runtime image: `eclipse-temurin:17-jre-alpine`
- Expose port 8080

</details>

### Level 2: Docker Compose with PostgreSQL ⭐⭐
Add PostgreSQL database using Docker Compose.

<details>
<summary>💡 Hints</summary>

- Create `docker-compose.yml` with two services
- Use `postgres:15-alpine` image
- Set environment variables for database connection
- Use `depends_on` to control startup order

</details>

### Level 3: Health Checks & Restart Policies ⭐⭐⭐
Add container health monitoring.

<details>
<summary>💡 Hints</summary>

- Add `HEALTHCHECK` instruction in Dockerfile
- Use `/actuator/health` endpoint
- Configure `restart: unless-stopped`
- Set `start_period` for Spring Boot warmup

</details>

### Level 4: Security & Resource Limits ⭐⭐⭐⭐
Implement security best practices.

<details>
<summary>💡 Hints</summary>

- Run as non-root user
- Set memory and CPU limits with `deploy.resources`
- Use secrets for database password
- Add JVM container awareness flags

</details>

### Level 5: Production with Nginx ⭐⭐⭐⭐⭐
Add Nginx reverse proxy with SSL.

<details>
<summary>💡 Hints</summary>

- Add nginx service to docker-compose
- Create nginx.conf for reverse proxy
- Configure SSL/TLS certificates
- Set up proper headers (X-Forwarded-For, etc.)

</details>

---

## 🏗️ Project Structure

```
task-management-api/
├── src/
│   ├── main/
│   │   ├── java/com/taskapi/
│   │   │   ├── TaskManagementApiApplication.java
│   │   │   ├── config/
│   │   │   │   ├── DataInitializer.java
│   │   │   │   └── OpenApiConfig.java
│   │   │   ├── controller/
│   │   │   │   └── TaskController.java
│   │   │   ├── exception/
│   │   │   │   ├── GlobalExceptionHandler.java
│   │   │   │   └── TaskNotFoundException.java
│   │   │   ├── model/
│   │   │   │   └── Task.java
│   │   │   ├── repository/
│   │   │   │   └── TaskRepository.java
│   │   │   └── service/
│   │   │       └── TaskService.java
│   │   └── resources/
│   │       ├── application.yml
│   │       └── application-docker.yml
├── Dockerfile
├── docker-compose.yml
├── pom.xml
└── README.md
```

## 🔧 Configuration

### Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `SPRING_PROFILES_ACTIVE` | Active profile | (none) |
| `DB_HOST` | Database host | postgres |
| `DB_PORT` | Database port | 5432 |
| `DB_NAME` | Database name | taskdb |
| `DB_USERNAME` | Database user | postgres |
| `DB_PASSWORD` | Database password | postgres |

---

## ☁️ AWS Deployment

### EC2 Deployment
```bash
# On EC2 instance
sudo yum install -y docker
sudo systemctl start docker
sudo usermod -aG docker ec2-user

# Clone and run
git clone <your-repo>
cd task-management-api
docker-compose up -d
```

### ECS Deployment (Advanced)
- Create ECS cluster
- Push image to ECR
- Create task definition
- Configure service with ALB

---

## 📚 Technologies

- **Java 17** - Language
- **Spring Boot 3.2** - Framework
- **Spring Data JPA** - Data persistence
- **H2 / PostgreSQL** - Database
- **Swagger/OpenAPI** - API documentation
- **Docker** - Containerization
- **Maven** - Build tool
