package com.notifications.model;

import java.time.LocalDateTime;
import java.util.Map;
import java.util.UUID;

/**
 * Notification Event
 * Represents an event that triggers notifications.
 */
public class NotificationEvent {

    private String eventId;
    private EventType eventType;
    private String source;
    private String recipient;
    private String subject;
    private String message;
    private NotificationChannel channel;
    private Priority priority;
    private Map<String, Object> metadata;
    private LocalDateTime timestamp;
    private EventStatus status;

    // Enums
    public enum EventType {
        USER_REGISTERED,
        PASSWORD_RESET,
        ORDER_PLACED,
        ORDER_SHIPPED,
        PAYMENT_RECEIVED,
        ALERT_TRIGGERED,
        SYSTEM_NOTIFICATION,
        CUSTOM
    }

    public enum NotificationChannel {
        EMAIL,
        SMS,
        WEBHOOK,
        PUSH,
        SLACK
    }

    public enum Priority {
        LOW,
        NORMAL,
        HIGH,
        URGENT
    }

    public enum EventStatus {
        PENDING,
        PROCESSING,
        SENT,
        DELIVERED,
        FAILED,
        RETRYING
    }

    // Constructors
    public NotificationEvent() {
        this.eventId = UUID.randomUUID().toString();
        this.timestamp = LocalDateTime.now();
        this.status = EventStatus.PENDING;
        this.priority = Priority.NORMAL;
    }

    public NotificationEvent(EventType eventType, String recipient, String subject, String message) {
        this();
        this.eventType = eventType;
        this.recipient = recipient;
        this.subject = subject;
        this.message = message;
    }

    // Builder pattern for fluent API
    public static Builder builder() {
        return new Builder();
    }

    public static class Builder {
        private final NotificationEvent event = new NotificationEvent();

        public Builder eventType(EventType eventType) {
            event.eventType = eventType;
            return this;
        }

        public Builder source(String source) {
            event.source = source;
            return this;
        }

        public Builder recipient(String recipient) {
            event.recipient = recipient;
            return this;
        }

        public Builder subject(String subject) {
            event.subject = subject;
            return this;
        }

        public Builder message(String message) {
            event.message = message;
            return this;
        }

        public Builder channel(NotificationChannel channel) {
            event.channel = channel;
            return this;
        }

        public Builder priority(Priority priority) {
            event.priority = priority;
            return this;
        }

        public Builder metadata(Map<String, Object> metadata) {
            event.metadata = metadata;
            return this;
        }

        public NotificationEvent build() {
            return event;
        }
    }

    // Getters and Setters
    public String getEventId() { return eventId; }
    public void setEventId(String eventId) { this.eventId = eventId; }

    public EventType getEventType() { return eventType; }
    public void setEventType(EventType eventType) { this.eventType = eventType; }

    public String getSource() { return source; }
    public void setSource(String source) { this.source = source; }

    public String getRecipient() { return recipient; }
    public void setRecipient(String recipient) { this.recipient = recipient; }

    public String getSubject() { return subject; }
    public void setSubject(String subject) { this.subject = subject; }

    public String getMessage() { return message; }
    public void setMessage(String message) { this.message = message; }

    public NotificationChannel getChannel() { return channel; }
    public void setChannel(NotificationChannel channel) { this.channel = channel; }

    public Priority getPriority() { return priority; }
    public void setPriority(Priority priority) { this.priority = priority; }

    public Map<String, Object> getMetadata() { return metadata; }
    public void setMetadata(Map<String, Object> metadata) { this.metadata = metadata; }

    public LocalDateTime getTimestamp() { return timestamp; }
    public void setTimestamp(LocalDateTime timestamp) { this.timestamp = timestamp; }

    public EventStatus getStatus() { return status; }
    public void setStatus(EventStatus status) { this.status = status; }

    @Override
    public String toString() {
        return "NotificationEvent{" +
                "eventId='" + eventId + '\'' +
                ", eventType=" + eventType +
                ", recipient='" + recipient + '\'' +
                ", channel=" + channel +
                ", status=" + status +
                '}';
    }
}
