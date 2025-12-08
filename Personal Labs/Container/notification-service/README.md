# Notification Service 📬

An **event-driven notification service** with Apache Kafka, demonstrating asynchronous messaging patterns for Docker containerization practice.

## 🎯 What You'll Learn

| Skill | Technology |
|-------|------------|
| Event-Driven Architecture | Apache Kafka, Spring Kafka |
| Message Streaming | Producers, Consumers, Topics |
| Async Processing | CompletableFuture, @Async |
| Multi-Container Setup | Kafka + Zookeeper + App |
| Observability | Kafka UI, Actuator |

## 🚀 Quick Start

### Run Locally (Development)
```bash
# Start Kafka first (requires Docker)
docker-compose up -d kafka kafka-ui

# Then run the service
./mvnw spring-boot:run
```

### Access Points
| Endpoint | Description |
|----------|-------------|
| http://localhost:8081/swagger-ui.html | API Documentation |
| http://localhost:8081/api/v1/notifications | Notification endpoints |
| http://localhost:8081/actuator/health | Health check |
| http://localhost:8082 | Kafka UI Dashboard |

## 📡 API Endpoints

### Send Notifications
```
POST /api/v1/notifications           - Send single notification
POST /api/v1/notifications/batch     - Send batch notifications
GET  /api/v1/notifications/stats     - Get statistics
GET  /api/v1/notifications/channels  - List channels
GET  /api/v1/notifications/event-types - List event types
```

### Example Request
```json
{
    "eventType": "USER_REGISTERED",
    "recipient": "user@example.com",
    "subject": "Welcome!",
    "message": "Thanks for signing up!",
    "channel": "EMAIL",
    "priority": "NORMAL"
}
```

---

## 🐳 Docker Challenges

### Level 1: Basic Dockerfile ⭐
Create a Dockerfile for the Spring Boot service.

<details>
<summary>💡 Hints</summary>

- Use multi-stage build
- Expose port 8081
- Set Kafka bootstrap servers via env var

</details>

### Level 2: Kafka with Docker Compose ⭐⭐
Set up Kafka and Zookeeper alongside the app.

<details>
<summary>💡 Hints</summary>

- Use `confluentinc/cp-kafka` image
- Configure internal and external listeners
- Wait for Kafka to be healthy before starting app

</details>

### Level 3: Consumer Scaling ⭐⭐⭐
Scale consumers horizontally.

<details>
<summary>💡 Hints</summary>

- Use `docker-compose up --scale app=3`
- Ensure partition count >= consumer count
- Watch rebalancing in Kafka UI

</details>

### Level 4: Monitoring Stack ⭐⭐⭐⭐
Add Prometheus and Grafana.

<details>
<summary>💡 Hints</summary>

- Expose `/actuator/prometheus` endpoint
- Add Prometheus service to scrape metrics
- Create Grafana dashboards

</details>

### Level 5: Production Deployment ⭐⭐⭐⭐⭐
Deploy to AWS with proper infrastructure.

<details>
<summary>💡 Hints</summary>

- Use Amazon MSK for managed Kafka
- Deploy to ECS with task definitions
- Set up CloudWatch for logging

</details>

---

## 🏗️ Project Structure

```
notification-service/
├── src/main/java/com/notifications/
│   ├── NotificationServiceApplication.java
│   ├── config/
│   │   └── KafkaConfig.java
│   ├── controller/
│   │   └── NotificationController.java
│   ├── kafka/
│   │   ├── NotificationProducer.java
│   │   └── NotificationConsumer.java
│   ├── model/
│   │   ├── NotificationEvent.java
│   │   └── NotificationRequest.java
│   └── service/
│       └── NotificationDispatcher.java
├── src/main/resources/
│   └── application.yml
├── Dockerfile
├── docker-compose.yml
├── pom.xml
└── README.md
```

## 🔧 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka brokers | localhost:9092 |
| `SERVER_PORT` | Service port | 8081 |

---

## 📚 Kafka Concepts

### Topics
- `notifications` - Main notification events
- `notifications-dlq` - Dead letter queue for failures

### Consumer Groups
Events are processed by consumer groups, allowing horizontal scaling.

### Dead Letter Queue (DLQ)
Failed messages are automatically sent to DLQ for later analysis.

---

## ☁️ AWS Deployment

### Using Amazon MSK (Managed Kafka)
```bash
# Set Kafka brokers to MSK endpoints
export KAFKA_BOOTSTRAP_SERVERS=b-1.mymsk.xxx.kafka.us-east-1.amazonaws.com:9092
```

### ECS Deployment
- Create task definition with container
- Configure security groups for Kafka access
- Set up ALB for the service

---

## 📚 Technologies

- **Java 17** - Language
- **Spring Boot 3.2** - Framework
- **Spring Kafka** - Kafka integration
- **Apache Kafka** - Message streaming
- **Docker** - Containerization
