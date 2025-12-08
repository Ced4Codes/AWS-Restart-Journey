package com.ecommerce.order;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class OrderServiceApplication {
    public static void main(String[] args) {
        System.out.println("""
            ╔══════════════════════════════════════════════════════════════╗
            ║              🛒 ORDER SERVICE                                ║
            ║           E-Commerce Microservices Demo                      ║
            ╠══════════════════════════════════════════════════════════════╣
            ║  API Docs: http://localhost:8082/swagger-ui.html             ║
            ║  Health:   http://localhost:8082/actuator/health             ║
            ╚══════════════════════════════════════════════════════════════╝
            """);
        SpringApplication.run(OrderServiceApplication.class, args);
    }
}
