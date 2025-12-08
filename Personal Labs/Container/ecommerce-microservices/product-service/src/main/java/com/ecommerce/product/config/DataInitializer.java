package com.ecommerce.product.config;

import com.ecommerce.product.model.Product;
import com.ecommerce.product.repository.ProductRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.math.BigDecimal;

@Configuration
public class DataInitializer {

    @Bean
    CommandLineRunner initProducts(ProductRepository repository) {
        return args -> {
            if (repository.count() == 0) {
                System.out.println("📦 Seeding product database...");

                repository.save(new Product("MacBook Pro 16\"", 
                    "Apple M3 Pro chip, 18GB RAM, 512GB SSD", 
                    new BigDecimal("2499.99"), 15, Product.Category.ELECTRONICS));

                repository.save(new Product("Sony WH-1000XM5", 
                    "Premium noise-cancelling headphones", 
                    new BigDecimal("349.99"), 50, Product.Category.ELECTRONICS));

                repository.save(new Product("Levi's 501 Jeans", 
                    "Classic straight fit denim", 
                    new BigDecimal("79.99"), 100, Product.Category.CLOTHING));

                repository.save(new Product("Clean Code", 
                    "A Handbook of Agile Software Craftsmanship by Robert C. Martin", 
                    new BigDecimal("39.99"), 75, Product.Category.BOOKS));

                repository.save(new Product("Instant Pot Duo", 
                    "7-in-1 Electric Pressure Cooker", 
                    new BigDecimal("89.99"), 30, Product.Category.HOME));

                repository.save(new Product("Nike Air Max 270", 
                    "Running shoes with Air cushioning", 
                    new BigDecimal("149.99"), 60, Product.Category.SPORTS));

                System.out.println("✅ Seeded " + repository.count() + " products");
            }
        };
    }
}
