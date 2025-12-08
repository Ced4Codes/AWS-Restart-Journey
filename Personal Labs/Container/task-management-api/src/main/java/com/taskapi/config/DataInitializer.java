package com.taskapi.config;

import com.taskapi.model.Task;
import com.taskapi.repository.TaskRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.time.LocalDateTime;

/**
 * Data Initializer
 * Loads sample data for development and demonstration.
 */
@Configuration
public class DataInitializer {

    @Bean
    CommandLineRunner initDatabase(TaskRepository repository) {
        return args -> {
            // Only seed if database is empty
            if (repository.count() == 0) {
                System.out.println("📋 Seeding database with sample tasks...");
                
                // Work tasks
                Task task1 = new Task(
                    "Complete Docker documentation",
                    "Write comprehensive Docker documentation for the project including Dockerfile best practices",
                    Task.Priority.HIGH,
                    Task.Category.WORK
                );
                task1.setDueDate(LocalDateTime.now().plusDays(3));
                repository.save(task1);

                Task task2 = new Task(
                    "Review pull requests",
                    "Review and merge pending pull requests from team members",
                    Task.Priority.MEDIUM,
                    Task.Category.WORK
                );
                task2.setDueDate(LocalDateTime.now().plusDays(1));
                repository.save(task2);

                Task task3 = new Task(
                    "Set up CI/CD pipeline",
                    "Configure GitHub Actions for automated testing and deployment",
                    Task.Priority.CRITICAL,
                    Task.Category.WORK
                );
                task3.setDueDate(LocalDateTime.now().plusDays(7));
                repository.save(task3);

                // Learning tasks
                Task task4 = new Task(
                    "Study AWS ECS",
                    "Complete AWS ECS tutorial and practice deploying containers",
                    Task.Priority.HIGH,
                    Task.Category.LEARNING
                );
                task4.setDueDate(LocalDateTime.now().plusDays(5));
                repository.save(task4);

                Task task5 = new Task(
                    "Practice Kubernetes basics",
                    "Go through Kubernetes fundamentals course",
                    Task.Priority.MEDIUM,
                    Task.Category.LEARNING
                );
                task5.setDueDate(LocalDateTime.now().plusDays(14));
                repository.save(task5);

                // Personal tasks
                Task task6 = new Task(
                    "Update portfolio website",
                    "Add new projects and update skills section",
                    Task.Priority.LOW,
                    Task.Category.PERSONAL
                );
                task6.setDueDate(LocalDateTime.now().plusDays(10));
                repository.save(task6);

                // Health tasks
                Task task7 = new Task(
                    "Morning workout routine",
                    "30 minutes exercise every morning",
                    Task.Priority.MEDIUM,
                    Task.Category.HEALTH
                );
                task7.setStatus(Task.Status.IN_PROGRESS);
                repository.save(task7);

                System.out.println("✅ Database seeded with " + repository.count() + " sample tasks");
            }
        };
    }
}
