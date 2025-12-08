package com.ecommerce.order.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

import java.math.BigDecimal;
import java.util.Map;

/**
 * Client for communicating with Product Service
 * Demonstrates inter-service communication in microservices
 */
@Service
public class ProductServiceClient {

    private final WebClient webClient;

    public ProductServiceClient(
            @Value("${services.product.url:http://localhost:8081}") String productServiceUrl) {
        this.webClient = WebClient.builder()
                .baseUrl(productServiceUrl)
                .build();
    }

    public ProductInfo getProduct(Long productId) {
        try {
            Map<String, Object> response = webClient.get()
                    .uri("/api/products/{id}", productId)
                    .retrieve()
                    .bodyToMono(Map.class)
                    .block();

            if (response != null) {
                return new ProductInfo(
                        Long.valueOf(response.get("id").toString()),
                        (String) response.get("name"),
                        new BigDecimal(response.get("price").toString()),
                        response.get("quantity") != null ? 
                            Integer.valueOf(response.get("quantity").toString()) : 0
                );
            }
        } catch (Exception e) {
            // In production, implement circuit breaker pattern
            System.err.println("⚠️ Failed to fetch product " + productId + ": " + e.getMessage());
        }
        return null;
    }

    public record ProductInfo(Long id, String name, BigDecimal price, int quantity) {}
}
