package com.taskapi.exception;

/**
 * Custom exception for when a task is not found.
 */
public class TaskNotFoundException extends RuntimeException {
    
    public TaskNotFoundException(String message) {
        super(message);
    }
    
    public TaskNotFoundException(Long id) {
        super("Task not found with id: " + id);
    }
}
