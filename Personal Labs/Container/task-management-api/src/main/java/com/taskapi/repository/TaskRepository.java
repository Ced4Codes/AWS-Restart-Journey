package com.taskapi.repository;

import com.taskapi.model.Task;
import com.taskapi.model.Task.Category;
import com.taskapi.model.Task.Priority;
import com.taskapi.model.Task.Status;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

/**
 * Task Repository
 * Spring Data JPA repository for Task entity operations.
 */
@Repository
public interface TaskRepository extends JpaRepository<Task, Long> {

    // Find by status
    List<Task> findByStatus(Status status);

    // Find by priority
    List<Task> findByPriority(Priority priority);

    // Find by category
    List<Task> findByCategory(Category category);

    // Find by status and priority
    List<Task> findByStatusAndPriority(Status status, Priority priority);

    // Search by title (case-insensitive)
    List<Task> findByTitleContainingIgnoreCase(String title);

    // Find overdue tasks
    @Query("SELECT t FROM Task t WHERE t.dueDate < :now AND t.status != 'COMPLETED'")
    List<Task> findOverdueTasks(@Param("now") LocalDateTime now);

    // Find tasks due today
    @Query("SELECT t FROM Task t WHERE t.dueDate >= :startOfDay AND t.dueDate < :endOfDay")
    List<Task> findTasksDueToday(@Param("startOfDay") LocalDateTime startOfDay, 
                                  @Param("endOfDay") LocalDateTime endOfDay);

    // Count by status
    long countByStatus(Status status);

    // Count by priority
    long countByPriority(Priority priority);

    // Find completed tasks in date range
    @Query("SELECT t FROM Task t WHERE t.completedAt >= :start AND t.completedAt <= :end")
    List<Task> findCompletedTasksInRange(@Param("start") LocalDateTime start, 
                                          @Param("end") LocalDateTime end);
}
