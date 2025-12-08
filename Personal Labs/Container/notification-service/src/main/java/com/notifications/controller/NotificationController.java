package com.notifications.controller;

import com.notifications.kafka.NotificationProducer;
import com.notifications.model.NotificationEvent;
import com.notifications.model.NotificationRequest;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.atomic.AtomicLong;

/**
 * Notification REST Controller
 * API endpoints for sending notifications and checking service status.
 */
@RestController
@RequestMapping("/api/v1/notifications")
@Tag(name = "Notifications", description = "Notification management endpoints")
@CrossOrigin(origins = "*")
public class NotificationController {

    private final NotificationProducer producer;
    private final AtomicLong totalSent = new AtomicLong(0);
    private final AtomicLong totalFailed = new AtomicLong(0);

    public NotificationController(NotificationProducer producer) {
        this.producer = producer;
    }

    @PostMapping
    @Operation(summary = "Send notification", description = "Publish a notification event to Kafka")
    @ApiResponse(responseCode = "202", description = "Notification accepted for processing")
    @ApiResponse(responseCode = "400", description = "Invalid request")
    public ResponseEntity<Map<String, Object>> sendNotification(
            @Valid @RequestBody NotificationRequest request) {
        
        NotificationEvent event = request.toEvent();
        
        producer.sendNotification(event)
                .whenComplete((result, ex) -> {
                    if (ex == null) {
                        totalSent.incrementAndGet();
                    } else {
                        totalFailed.incrementAndGet();
                    }
                });

        Map<String, Object> response = new HashMap<>();
        response.put("status", "accepted");
        response.put("eventId", event.getEventId());
        response.put("message", "Notification queued for processing");
        response.put("channel", event.getChannel());
        response.put("priority", event.getPriority());

        return ResponseEntity.status(HttpStatus.ACCEPTED).body(response);
    }

    @PostMapping("/batch")
    @Operation(summary = "Send batch notifications", description = "Send multiple notifications at once")
    public ResponseEntity<Map<String, Object>> sendBatchNotifications(
            @Valid @RequestBody NotificationRequest[] requests) {
        
        int count = 0;
        for (NotificationRequest request : requests) {
            NotificationEvent event = request.toEvent();
            producer.sendNotification(event);
            count++;
        }

        Map<String, Object> response = new HashMap<>();
        response.put("status", "accepted");
        response.put("count", count);
        response.put("message", count + " notifications queued for processing");

        return ResponseEntity.status(HttpStatus.ACCEPTED).body(response);
    }

    @GetMapping("/stats")
    @Operation(summary = "Get notification statistics", description = "Get stats about sent notifications")
    public ResponseEntity<Map<String, Object>> getStats() {
        Map<String, Object> stats = new HashMap<>();
        stats.put("totalSent", totalSent.get());
        stats.put("totalFailed", totalFailed.get());
        stats.put("successRate", calculateSuccessRate());
        return ResponseEntity.ok(stats);
    }

    @GetMapping("/channels")
    @Operation(summary = "Get available channels", description = "List all available notification channels")
    public ResponseEntity<NotificationEvent.NotificationChannel[]> getChannels() {
        return ResponseEntity.ok(NotificationEvent.NotificationChannel.values());
    }

    @GetMapping("/event-types")
    @Operation(summary = "Get event types", description = "List all available event types")
    public ResponseEntity<NotificationEvent.EventType[]> getEventTypes() {
        return ResponseEntity.ok(NotificationEvent.EventType.values());
    }

    private double calculateSuccessRate() {
        long total = totalSent.get() + totalFailed.get();
        if (total == 0) return 100.0;
        return (double) totalSent.get() / total * 100;
    }
}
