# E-Commerce Microservices 🛒

A **microservices architecture** demonstrating containerized multi-service systems with Spring Boot for Docker orchestration practice.

## 🎯 What You'll Learn

| Skill | Technology |
|-------|------------|
| Microservices Architecture | Spring Boot, Spring Cloud |
| API Gateway Pattern | Spring Cloud Gateway |
| Inter-Service Communication | WebClient, REST APIs |
| Container Orchestration | Docker Compose |
| Service Networking | Docker Networks |

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         CLIENT                               │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    API GATEWAY (:8080)                       │
│              Spring Cloud Gateway                            │
│         Routes: /api/products → Product Service              │
│                 /api/orders → Order Service                  │
└─────────────────────────────┬───────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
┌─────────────────────────┐   ┌─────────────────────────┐
│   PRODUCT SERVICE       │   │    ORDER SERVICE        │
│      (:8081)            │◄──│       (:8082)           │
│   - Product catalog     │   │   - Order management    │
│   - Inventory           │   │   - Calls product svc   │
│   - H2 Database         │   │   - H2 Database         │
└─────────────────────────┘   └─────────────────────────┘
```

## 🚀 Quick Start

### Run with Docker Compose
```bash
# Build and start all services
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

### Access Points (via Gateway)
| Endpoint | Description |
|----------|-------------|
| http://localhost:8080/api/products | Product catalog |
| http://localhost:8080/api/orders | Order management |
| http://localhost:8080/actuator/health | Gateway health |

### Direct Service Access
| Service | URL |
|---------|-----|
| API Gateway | http://localhost:8080 |
| Product Service | http://localhost:8081 |
| Order Service | http://localhost:8082 |

---

## 📡 API Endpoints

### Products (via Gateway)
```
GET  /api/products               - List all products
GET  /api/products/{id}          - Get product by ID
POST /api/products               - Create product
GET  /api/products/category/{cat} - Filter by category
GET  /api/products/search?q=     - Search products
```

### Orders (via Gateway)
```
GET  /api/orders                 - List all orders
POST /api/orders                 - Create order
GET  /api/orders/{id}            - Get order by ID
PATCH /api/orders/{id}/status    - Update status
GET  /api/orders/customer/{email} - Orders by customer
```

### Create Order Example
```json
POST /api/orders
{
    "customerEmail": "john@example.com",
    "customerName": "John Doe",
    "items": [
        { "productId": 1, "quantity": 2 },
        { "productId": 3, "quantity": 1 }
    ]
}
```

---

## 🐳 Docker Challenges

### Level 1: Containerize Each Service ⭐
Create Dockerfiles for each microservice.

<details>
<summary>💡 Hints</summary>

- Use multi-stage builds
- Each service has its own Dockerfile
- Expose correct ports (8080, 8081, 8082)

</details>

### Level 2: Docker Compose Orchestration ⭐⭐
Create docker-compose.yml to run all services together.

<details>
<summary>💡 Hints</summary>

- Define three services
- Use `depends_on` for startup order
- Configure environment variables for service URLs

</details>

### Level 3: Service Networking ⭐⭐⭐
Configure proper networking between services.

<details>
<summary>💡 Hints</summary>

- Create a custom bridge network
- Use service names as hostnames
- Configure health checks with `condition: service_healthy`

</details>

### Level 4: Add Databases ⭐⭐⭐⭐
Add PostgreSQL for each service.

<details>
<summary>💡 Hints</summary>

- One database per service (microservices pattern)
- Use volumes for persistence
- Configure connection strings via env vars

</details>

### Level 5: Production Deployment ⭐⭐⭐⭐⭐
Deploy to AWS ECS.

<details>
<summary>💡 Hints</summary>

- Push images to ECR
- Create ECS task definitions
- Use ALB for the API Gateway
- Set up CloudWatch logging

</details>

---

## 🏗️ Project Structure

```
ecommerce-microservices/
├── api-gateway/
│   ├── src/main/java/com/ecommerce/gateway/
│   │   ├── ApiGatewayApplication.java
│   │   └── FallbackController.java
│   ├── src/main/resources/application.yml
│   ├── Dockerfile
│   └── pom.xml
│
├── product-service/
│   ├── src/main/java/com/ecommerce/product/
│   │   ├── ProductServiceApplication.java
│   │   ├── controller/ProductController.java
│   │   ├── model/Product.java
│   │   └── repository/ProductRepository.java
│   ├── Dockerfile
│   └── pom.xml
│
├── order-service/
│   ├── src/main/java/com/ecommerce/order/
│   │   ├── OrderServiceApplication.java
│   │   ├── controller/OrderController.java
│   │   ├── model/Order.java, OrderItem.java
│   │   └── service/ProductServiceClient.java
│   ├── Dockerfile
│   └── pom.xml
│
├── docker-compose.yml
└── README.md
```

---

## 🔧 Environment Variables

### API Gateway
| Variable | Description | Default |
|----------|-------------|---------|
| `PRODUCT_SERVICE_URL` | Product service URL | http://localhost:8081 |
| `ORDER_SERVICE_URL` | Order service URL | http://localhost:8082 |

### Order Service
| Variable | Description | Default |
|----------|-------------|---------|
| `PRODUCT_SERVICE_URL` | Product service for lookups | http://localhost:8081 |

---

## 📚 Microservices Concepts

### API Gateway Pattern
Single entry point for all client requests, handling:
- Routing to appropriate services
- Cross-cutting concerns (CORS, auth)
- Circuit breaker for fault tolerance

### Inter-Service Communication
Order service calls Product service to get product details:
- Uses WebClient (reactive HTTP client)
- Graceful fallback when service unavailable

### Database Per Service
Each microservice owns its data:
- Product Service → Product Database
- Order Service → Order Database

---

## ☁️ AWS Deployment

### Architecture on AWS
```
                    ┌─────────────────┐
                    │      ALB        │
                    └────────┬────────┘
                             │
              ┌──────────────┴──────────────┐
              ▼                             ▼
     ┌────────────────┐           ┌────────────────┐
     │  ECS Service   │           │  ECS Service   │
     │  (Gateway)     │           │  (Products)    │
     └────────────────┘           └────────────────┘
                                          │
                                  ┌───────┴───────┐
                                  ▼               ▼
                           ┌──────────┐    ┌──────────┐
                           │   RDS    │    │   RDS    │
                           └──────────┘    └──────────┘
```

---

## 📚 Technologies

- **Java 17** - Language
- **Spring Boot 3.2** - Framework
- **Spring Cloud Gateway** - API Gateway
- **Spring Data JPA** - Data persistence
- **Spring WebFlux** - Reactive HTTP client
- **H2 / PostgreSQL** - Databases
- **Docker** - Containerization
