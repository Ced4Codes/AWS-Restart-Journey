package com.taskapi.controller;

import com.taskapi.model.Task;
import com.taskapi.model.Task.Category;
import com.taskapi.model.Task.Priority;
import com.taskapi.model.Task.Status;
import com.taskapi.service.TaskService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

/**
 * Task REST Controller
 * Handles all HTTP requests for task operations.
 * 
 * API Documentation available at: /swagger-ui.html
 */
@RestController
@RequestMapping("/api/v1/tasks")
@Tag(name = "Tasks", description = "Task management endpoints")
@CrossOrigin(origins = "*")
public class TaskController {

    private final TaskService taskService;

    public TaskController(TaskService taskService) {
        this.taskService = taskService;
    }

    // ========== CRUD Operations ==========

    @GetMapping
    @Operation(summary = "Get all tasks", description = "Retrieve a list of all tasks")
    public ResponseEntity<List<Task>> getAllTasks() {
        return ResponseEntity.ok(taskService.getAllTasks());
    }

    @GetMapping("/{id}")
    @Operation(summary = "Get task by ID", description = "Retrieve a specific task by its ID")
    @ApiResponse(responseCode = "200", description = "Task found")
    @ApiResponse(responseCode = "404", description = "Task not found")
    public ResponseEntity<Task> getTaskById(
            @Parameter(description = "Task ID") @PathVariable Long id) {
        return ResponseEntity.ok(taskService.getTaskById(id));
    }

    @PostMapping
    @Operation(summary = "Create a new task", description = "Create a new task with the provided details")
    @ApiResponse(responseCode = "201", description = "Task created successfully")
    @ApiResponse(responseCode = "400", description = "Invalid input")
    public ResponseEntity<Task> createTask(@Valid @RequestBody Task task) {
        Task createdTask = taskService.createTask(task);
        return ResponseEntity.status(HttpStatus.CREATED).body(createdTask);
    }

    @PutMapping("/{id}")
    @Operation(summary = "Update a task", description = "Update an existing task by ID")
    @ApiResponse(responseCode = "200", description = "Task updated successfully")
    @ApiResponse(responseCode = "404", description = "Task not found")
    public ResponseEntity<Task> updateTask(
            @Parameter(description = "Task ID") @PathVariable Long id,
            @Valid @RequestBody Task task) {
        return ResponseEntity.ok(taskService.updateTask(id, task));
    }

    @DeleteMapping("/{id}")
    @Operation(summary = "Delete a task", description = "Delete a task by ID")
    @ApiResponse(responseCode = "204", description = "Task deleted successfully")
    @ApiResponse(responseCode = "404", description = "Task not found")
    public ResponseEntity<Void> deleteTask(
            @Parameter(description = "Task ID") @PathVariable Long id) {
        taskService.deleteTask(id);
        return ResponseEntity.noContent().build();
    }

    // ========== Status Operations ==========

    @PatchMapping("/{id}/complete")
    @Operation(summary = "Mark task as completed", description = "Update task status to COMPLETED")
    public ResponseEntity<Task> completeTask(@PathVariable Long id) {
        return ResponseEntity.ok(taskService.completeTask(id));
    }

    @PatchMapping("/{id}/archive")
    @Operation(summary = "Archive a task", description = "Update task status to ARCHIVED")
    public ResponseEntity<Task> archiveTask(@PathVariable Long id) {
        return ResponseEntity.ok(taskService.archiveTask(id));
    }

    // ========== Filter Operations ==========

    @GetMapping("/status/{status}")
    @Operation(summary = "Get tasks by status", description = "Filter tasks by their status")
    public ResponseEntity<List<Task>> getTasksByStatus(
            @Parameter(description = "Task status") @PathVariable Status status) {
        return ResponseEntity.ok(taskService.getTasksByStatus(status));
    }

    @GetMapping("/priority/{priority}")
    @Operation(summary = "Get tasks by priority", description = "Filter tasks by their priority level")
    public ResponseEntity<List<Task>> getTasksByPriority(
            @Parameter(description = "Priority level") @PathVariable Priority priority) {
        return ResponseEntity.ok(taskService.getTasksByPriority(priority));
    }

    @GetMapping("/category/{category}")
    @Operation(summary = "Get tasks by category", description = "Filter tasks by their category")
    public ResponseEntity<List<Task>> getTasksByCategory(
            @Parameter(description = "Task category") @PathVariable Category category) {
        return ResponseEntity.ok(taskService.getTasksByCategory(category));
    }

    @GetMapping("/search")
    @Operation(summary = "Search tasks", description = "Search tasks by title (case-insensitive)")
    public ResponseEntity<List<Task>> searchTasks(
            @Parameter(description = "Search query") @RequestParam String q) {
        return ResponseEntity.ok(taskService.searchTasks(q));
    }

    @GetMapping("/overdue")
    @Operation(summary = "Get overdue tasks", description = "Get all tasks past their due date")
    public ResponseEntity<List<Task>> getOverdueTasks() {
        return ResponseEntity.ok(taskService.getOverdueTasks());
    }

    @GetMapping("/due-today")
    @Operation(summary = "Get tasks due today", description = "Get all tasks due today")
    public ResponseEntity<List<Task>> getTasksDueToday() {
        return ResponseEntity.ok(taskService.getTasksDueToday());
    }

    // ========== Statistics ==========

    @GetMapping("/stats")
    @Operation(summary = "Get task statistics", description = "Get statistics about all tasks")
    public ResponseEntity<Map<String, Object>> getTaskStatistics() {
        return ResponseEntity.ok(taskService.getTaskStatistics());
    }
}
