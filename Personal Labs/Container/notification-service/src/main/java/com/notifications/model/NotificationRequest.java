package com.notifications.model;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

/**
 * DTO for creating notification requests via API
 */
public class NotificationRequest {

    @NotNull(message = "Event type is required")
    private NotificationEvent.EventType eventType;

    @NotBlank(message = "Recipient is required")
    private String recipient;

    @NotBlank(message = "Subject is required")
    private String subject;

    @NotBlank(message = "Message is required")
    private String message;

    private NotificationEvent.NotificationChannel channel = NotificationEvent.NotificationChannel.EMAIL;
    
    private NotificationEvent.Priority priority = NotificationEvent.Priority.NORMAL;

    // Constructors
    public NotificationRequest() {}

    public NotificationRequest(NotificationEvent.EventType eventType, String recipient, 
                                String subject, String message) {
        this.eventType = eventType;
        this.recipient = recipient;
        this.subject = subject;
        this.message = message;
    }

    // Convert to event
    public NotificationEvent toEvent() {
        return NotificationEvent.builder()
                .eventType(eventType)
                .recipient(recipient)
                .subject(subject)
                .message(message)
                .channel(channel)
                .priority(priority)
                .build();
    }

    // Getters and Setters
    public NotificationEvent.EventType getEventType() { return eventType; }
    public void setEventType(NotificationEvent.EventType eventType) { this.eventType = eventType; }

    public String getRecipient() { return recipient; }
    public void setRecipient(String recipient) { this.recipient = recipient; }

    public String getSubject() { return subject; }
    public void setSubject(String subject) { this.subject = subject; }

    public String getMessage() { return message; }
    public void setMessage(String message) { this.message = message; }

    public NotificationEvent.NotificationChannel getChannel() { return channel; }
    public void setChannel(NotificationEvent.NotificationChannel channel) { this.channel = channel; }

    public NotificationEvent.Priority getPriority() { return priority; }
    public void setPriority(NotificationEvent.Priority priority) { this.priority = priority; }
}
