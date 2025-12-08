package com.taskapi.service;

import com.taskapi.exception.TaskNotFoundException;
import com.taskapi.model.Task;
import com.taskapi.model.Task.Category;
import com.taskapi.model.Task.Priority;
import com.taskapi.model.Task.Status;
import com.taskapi.repository.TaskRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Task Service
 * Business logic layer for task operations.
 */
@Service
@Transactional
public class TaskService {

    private final TaskRepository taskRepository;

    public TaskService(TaskRepository taskRepository) {
        this.taskRepository = taskRepository;
    }

    // CRUD Operations
    public List<Task> getAllTasks() {
        return taskRepository.findAll();
    }

    public Task getTaskById(Long id) {
        return taskRepository.findById(id)
                .orElseThrow(() -> new TaskNotFoundException("Task not found with id: " + id));
    }

    public Task createTask(Task task) {
        return taskRepository.save(task);
    }

    public Task updateTask(Long id, Task taskDetails) {
        Task task = getTaskById(id);
        
        task.setTitle(taskDetails.getTitle());
        task.setDescription(taskDetails.getDescription());
        task.setPriority(taskDetails.getPriority());
        task.setStatus(taskDetails.getStatus());
        task.setCategory(taskDetails.getCategory());
        task.setDueDate(taskDetails.getDueDate());
        
        return taskRepository.save(task);
    }

    public void deleteTask(Long id) {
        Task task = getTaskById(id);
        taskRepository.delete(task);
    }

    // Status Operations
    public Task completeTask(Long id) {
        Task task = getTaskById(id);
        task.setStatus(Status.COMPLETED);
        return taskRepository.save(task);
    }

    public Task archiveTask(Long id) {
        Task task = getTaskById(id);
        task.setStatus(Status.ARCHIVED);
        return taskRepository.save(task);
    }

    // Filter Operations
    public List<Task> getTasksByStatus(Status status) {
        return taskRepository.findByStatus(status);
    }

    public List<Task> getTasksByPriority(Priority priority) {
        return taskRepository.findByPriority(priority);
    }

    public List<Task> getTasksByCategory(Category category) {
        return taskRepository.findByCategory(category);
    }

    public List<Task> searchTasks(String query) {
        return taskRepository.findByTitleContainingIgnoreCase(query);
    }

    public List<Task> getOverdueTasks() {
        return taskRepository.findOverdueTasks(LocalDateTime.now());
    }

    public List<Task> getTasksDueToday() {
        LocalDate today = LocalDate.now();
        return taskRepository.findTasksDueToday(
                today.atStartOfDay(),
                today.plusDays(1).atStartOfDay()
        );
    }

    // Statistics
    public Map<String, Object> getTaskStatistics() {
        Map<String, Object> stats = new HashMap<>();
        
        stats.put("total", taskRepository.count());
        stats.put("todo", taskRepository.countByStatus(Status.TODO));
        stats.put("inProgress", taskRepository.countByStatus(Status.IN_PROGRESS));
        stats.put("completed", taskRepository.countByStatus(Status.COMPLETED));
        stats.put("archived", taskRepository.countByStatus(Status.ARCHIVED));
        
        stats.put("lowPriority", taskRepository.countByPriority(Priority.LOW));
        stats.put("mediumPriority", taskRepository.countByPriority(Priority.MEDIUM));
        stats.put("highPriority", taskRepository.countByPriority(Priority.HIGH));
        stats.put("criticalPriority", taskRepository.countByPriority(Priority.CRITICAL));
        
        stats.put("overdue", getOverdueTasks().size());
        stats.put("dueToday", getTasksDueToday().size());
        
        return stats;
    }
}
