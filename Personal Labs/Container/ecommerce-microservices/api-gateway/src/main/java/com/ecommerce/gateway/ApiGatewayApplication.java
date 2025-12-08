package com.ecommerce.gateway;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class ApiGatewayApplication {
    public static void main(String[] args) {
        System.out.println("""
            ╔══════════════════════════════════════════════════════════════╗
            ║              🌐 API GATEWAY                                  ║
            ║           E-Commerce Microservices Demo                      ║
            ╠══════════════════════════════════════════════════════════════╣
            ║  Gateway:   http://localhost:8080                            ║
            ║  Products:  http://localhost:8080/api/products               ║
            ║  Orders:    http://localhost:8080/api/orders                 ║
            ║  Health:    http://localhost:8080/actuator/health            ║
            ╚══════════════════════════════════════════════════════════════╝
            """);
        SpringApplication.run(ApiGatewayApplication.class, args);
    }
}
