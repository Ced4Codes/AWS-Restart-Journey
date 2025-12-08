package com.notifications;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableAsync;

/**
 * Notification Service - Spring Boot Application
 * ===============================================
 * 
 * An event-driven notification service demonstrating Kafka messaging patterns.
 * 
 * FEATURES:
 * - Event publishing to Kafka topics
 * - Event consumption with multiple consumers
 * - Multiple notification channels (email mock, webhook mock, SMS mock)
 * - Retry mechanisms and dead letter queues
 * - Health monitoring with Spring Actuator
 * 
 * ARCHITECTURE:
 * - Spring Boot 3.2+ with Java 17
 * - Apache Kafka for message streaming
 * - Event-driven architecture
 * 
 * YOUR DOCKER CHALLENGE:
 * 1. Create a Dockerfile for this service
 * 2. Set up Kafka and Zookeeper with Docker Compose
 * 3. Configure multiple consumer instances
 * 4. Add monitoring with Prometheus and Grafana
 * 5. Deploy to AWS with container orchestration
 * 
 * API DOCUMENTATION: http://localhost:8081/swagger-ui.html
 * HEALTH CHECK: http://localhost:8081/actuator/health
 * 
 * Good luck! 🐳
 */
@SpringBootApplication
@EnableAsync
public class NotificationServiceApplication {

    public static void main(String[] args) {
        System.out.println("""
            
            ╔══════════════════════════════════════════════════════════════╗
            ║              📬 NOTIFICATION SERVICE                         ║
            ╠══════════════════════════════════════════════════════════════╣
            ║  API Docs:    http://localhost:8081/swagger-ui.html          ║
            ║  Health:      http://localhost:8081/actuator/health          ║
            ║  Kafka:       http://localhost:8081/api/v1/notifications     ║
            ╠══════════════════════════════════════════════════════════════╣
            ║  DOCKER CHALLENGE:                                           ║
            ║  1. Containerize this service                                ║
            ║  2. Add Kafka + Zookeeper with docker-compose                ║
            ║  3. Scale consumers horizontally                             ║
            ║  4. Add Prometheus + Grafana monitoring                      ║
            ╚══════════════════════════════════════════════════════════════╝
            """);
        SpringApplication.run(NotificationServiceApplication.class, args);
    }
}
