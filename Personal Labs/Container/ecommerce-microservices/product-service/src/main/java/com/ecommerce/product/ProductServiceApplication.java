package com.ecommerce.product;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class ProductServiceApplication {
    public static void main(String[] args) {
        System.out.println("""
            ╔══════════════════════════════════════════════════════════════╗
            ║              📦 PRODUCT SERVICE                              ║
            ║           E-Commerce Microservices Demo                      ║
            ╠══════════════════════════════════════════════════════════════╣
            ║  API Docs: http://localhost:8081/swagger-ui.html             ║
            ║  Health:   http://localhost:8081/actuator/health             ║
            ╚══════════════════════════════════════════════════════════════╝
            """);
        SpringApplication.run(ProductServiceApplication.class, args);
    }
}
