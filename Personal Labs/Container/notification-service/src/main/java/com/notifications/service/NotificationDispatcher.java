package com.notifications.service;

import com.notifications.model.NotificationEvent;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;

/**
 * Notification Dispatcher
 * Routes notifications to appropriate channels (email, SMS, webhook, etc.)
 * 
 * Note: This is a mock implementation for learning purposes.
 * In production, you would integrate with real notification providers.
 */
@Service
public class NotificationDispatcher {

    private static final Logger log = LoggerFactory.getLogger(NotificationDispatcher.class);

    /**
     * Dispatch notification to the appropriate channel
     */
    public boolean dispatch(NotificationEvent event) {
        return switch (event.getChannel()) {
            case EMAIL -> sendEmail(event);
            case SMS -> sendSms(event);
            case WEBHOOK -> sendWebhook(event);
            case PUSH -> sendPush(event);
            case SLACK -> sendSlack(event);
            default -> {
                log.warn("⚠️ Unknown channel: {}", event.getChannel());
                yield false;
            }
        };
    }

    /**
     * Mock Email Sender
     */
    @Async
    public boolean sendEmail(NotificationEvent event) {
        log.info("📧 [EMAIL] Sending to: {}", event.getRecipient());
        log.info("   Subject: {}", event.getSubject());
        log.info("   Message: {}", truncate(event.getMessage(), 100));
        
        // Simulate processing time
        simulateLatency(100);
        
        // Mock success (95% success rate for demo)
        boolean success = Math.random() > 0.05;
        
        if (success) {
            log.info("📧 [EMAIL] ✅ Sent successfully to: {}", event.getRecipient());
        } else {
            log.error("📧 [EMAIL] ❌ Failed to send to: {}", event.getRecipient());
        }
        
        return success;
    }

    /**
     * Mock SMS Sender
     */
    @Async
    public boolean sendSms(NotificationEvent event) {
        log.info("📱 [SMS] Sending to: {}", event.getRecipient());
        log.info("   Message: {}", truncate(event.getMessage(), 160));
        
        simulateLatency(50);
        
        boolean success = Math.random() > 0.05;
        
        if (success) {
            log.info("📱 [SMS] ✅ Sent successfully to: {}", event.getRecipient());
        } else {
            log.error("📱 [SMS] ❌ Failed to send to: {}", event.getRecipient());
        }
        
        return success;
    }

    /**
     * Mock Webhook Sender
     */
    @Async
    public boolean sendWebhook(NotificationEvent event) {
        log.info("🔗 [WEBHOOK] Posting to: {}", event.getRecipient());
        log.info("   Payload: {}", truncate(event.getMessage(), 200));
        
        simulateLatency(200);
        
        boolean success = Math.random() > 0.1;
        
        if (success) {
            log.info("🔗 [WEBHOOK] ✅ Posted successfully to: {}", event.getRecipient());
        } else {
            log.error("🔗 [WEBHOOK] ❌ Failed to post to: {}", event.getRecipient());
        }
        
        return success;
    }

    /**
     * Mock Push Notification Sender
     */
    @Async
    public boolean sendPush(NotificationEvent event) {
        log.info("🔔 [PUSH] Sending to device: {}", event.getRecipient());
        log.info("   Title: {}", event.getSubject());
        log.info("   Body: {}", truncate(event.getMessage(), 100));
        
        simulateLatency(150);
        
        log.info("🔔 [PUSH] ✅ Sent successfully");
        return true;
    }

    /**
     * Mock Slack Sender
     */
    @Async
    public boolean sendSlack(NotificationEvent event) {
        log.info("💬 [SLACK] Sending to channel: {}", event.getRecipient());
        log.info("   Message: {}", event.getMessage());
        
        simulateLatency(100);
        
        log.info("💬 [SLACK] ✅ Sent successfully to: {}", event.getRecipient());
        return true;
    }

    /**
     * Simulate network latency
     */
    private void simulateLatency(int maxMs) {
        try {
            Thread.sleep((long) (Math.random() * maxMs));
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    /**
     * Truncate string for logging
     */
    private String truncate(String str, int maxLength) {
        if (str == null) return "";
        if (str.length() <= maxLength) return str;
        return str.substring(0, maxLength) + "...";
    }
}
