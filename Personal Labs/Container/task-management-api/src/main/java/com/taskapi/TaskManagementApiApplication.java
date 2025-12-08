package com.taskapi;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Task Management API - Spring Boot Application
 * ==============================================
 * 
 * A fully functional RESTful API for managing tasks with categories and priorities.
 * 
 * FEATURES:
 * - Full CRUD operations for tasks
 * - Categories and priority levels
 * - Search and filter capabilities
 * - API documentation with Swagger/OpenAPI
 * - Health check endpoints for container orchestration
 * 
 * ARCHITECTURE:
 * - Spring Boot 3.2+ with Java 17
 * - Spring Data JPA for persistence
 * - H2 Database for development
 * - PostgreSQL for production (Docker)
 * 
 * YOUR DOCKER CHALLENGE:
 * 1. Create a multi-stage Dockerfile for this app
 * 2. Create a docker-compose.yml with PostgreSQL
 * 3. Implement health checks
 * 4. Add Nginx as a reverse proxy
 * 5. Configure for AWS ECS deployment
 * 
 * API DOCUMENTATION: http://localhost:8080/swagger-ui.html
 * HEALTH CHECK: http://localhost:8080/actuator/health
 * 
 * Good luck! 🐳
 */
@SpringBootApplication
public class TaskManagementApiApplication {

    public static void main(String[] args) {
        System.out.println("""
            
            ╔══════════════════════════════════════════════════════════════╗
            ║                 📋 TASK MANAGEMENT API                       ║
            ╠══════════════════════════════════════════════════════════════╣
            ║  API Docs:    http://localhost:8080/swagger-ui.html          ║
            ║  Health:      http://localhost:8080/actuator/health          ║
            ║  API Base:    http://localhost:8080/api/v1                   ║
            ╠══════════════════════════════════════════════════════════════╣
            ║  DOCKER CHALLENGE:                                           ║
            ║  1. Create a multi-stage Dockerfile                          ║
            ║  2. Add PostgreSQL with docker-compose                       ║
            ║  3. Configure health checks                                  ║
            ║  4. Deploy to AWS EC2/ECS                                    ║
            ╚══════════════════════════════════════════════════════════════╝
            """);
        SpringApplication.run(TaskManagementApiApplication.class, args);
    }
}
