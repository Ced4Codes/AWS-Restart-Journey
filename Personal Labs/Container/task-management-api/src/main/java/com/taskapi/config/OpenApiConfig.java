package com.taskapi.config;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.License;
import io.swagger.v3.oas.models.servers.Server;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.List;

/**
 * OpenAPI/Swagger Configuration
 * Configures API documentation available at /swagger-ui.html
 */
@Configuration
public class OpenApiConfig {

    @Bean
    public OpenAPI taskManagementOpenAPI() {
        return new OpenAPI()
            .info(new Info()
                .title("Task Management API")
                .description("""
                    A RESTful API for managing tasks with categories and priorities.
                    
                    ## Features
                    - Full CRUD operations for tasks
                    - Filter by status, priority, and category
                    - Search tasks by title
                    - Track overdue and due-today tasks
                    - Task statistics
                    
                    ## Docker Challenge
                    This API is designed for Docker containerization practice.
                    Check the README for progressive Docker challenges!
                    """)
                .version("1.0.0")
                .contact(new Contact()
                    .name("AWS Restart Journey")
                    .url("https://github.com/yourusername/AWS-Restart-Journey"))
                .license(new License()
                    .name("CC BY-NC-ND 4.0")
                    .url("https://creativecommons.org/licenses/by-nc-nd/4.0/")))
            .servers(List.of(
                new Server().url("http://localhost:8080").description("Development Server"),
                new Server().url("http://localhost:80").description("Docker (behind Nginx)")
            ));
    }
}
