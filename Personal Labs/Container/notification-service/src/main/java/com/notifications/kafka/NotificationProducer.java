package com.notifications.kafka;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.notifications.model.NotificationEvent;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.support.SendResult;
import org.springframework.stereotype.Service;

import java.util.concurrent.CompletableFuture;

/**
 * Kafka Producer Service
 * Publishes notification events to Kafka topics.
 * 
 * KAFKA CONCEPTS:
 * - Producers send messages to topics
 * - Messages are partitioned for scalability
 * - Acknowledgments ensure delivery
 */
@Service
public class NotificationProducer {

    private static final Logger log = LoggerFactory.getLogger(NotificationProducer.class);

    private final KafkaTemplate<String, String> kafkaTemplate;
    private final ObjectMapper objectMapper;

    @Value("${app.kafka.topic.notifications:notifications}")
    private String notificationsTopic;

    @Value("${app.kafka.topic.dlq:notifications-dlq}")
    private String dlqTopic;

    public NotificationProducer(KafkaTemplate<String, String> kafkaTemplate, ObjectMapper objectMapper) {
        this.kafkaTemplate = kafkaTemplate;
        this.objectMapper = objectMapper;
    }

    /**
     * Send notification event to Kafka
     */
    public CompletableFuture<SendResult<String, String>> sendNotification(NotificationEvent event) {
        try {
            String eventJson = objectMapper.writeValueAsString(event);
            
            log.info("📤 Sending notification event: {} to topic: {}", event.getEventId(), notificationsTopic);
            
            CompletableFuture<SendResult<String, String>> future = 
                kafkaTemplate.send(notificationsTopic, event.getEventId(), eventJson);

            future.whenComplete((result, ex) -> {
                if (ex == null) {
                    log.info("✅ Event sent successfully: {} - partition: {}, offset: {}",
                            event.getEventId(),
                            result.getRecordMetadata().partition(),
                            result.getRecordMetadata().offset());
                } else {
                    log.error("❌ Failed to send event: {}", event.getEventId(), ex);
                    sendToDeadLetterQueue(event);
                }
            });

            return future;
        } catch (JsonProcessingException e) {
            log.error("❌ Failed to serialize event: {}", event.getEventId(), e);
            throw new RuntimeException("Failed to serialize notification event", e);
        }
    }

    /**
     * Send to Dead Letter Queue (DLQ) for failed messages
     */
    public void sendToDeadLetterQueue(NotificationEvent event) {
        try {
            event.setStatus(NotificationEvent.EventStatus.FAILED);
            String eventJson = objectMapper.writeValueAsString(event);
            kafkaTemplate.send(dlqTopic, event.getEventId(), eventJson);
            log.warn("☠️ Event moved to DLQ: {}", event.getEventId());
        } catch (JsonProcessingException e) {
            log.error("❌ Failed to send to DLQ: {}", event.getEventId(), e);
        }
    }

    /**
     * Send with specific partition (for ordered processing)
     */
    public CompletableFuture<SendResult<String, String>> sendToPartition(
            NotificationEvent event, int partition) {
        try {
            String eventJson = objectMapper.writeValueAsString(event);
            return kafkaTemplate.send(notificationsTopic, partition, event.getEventId(), eventJson);
        } catch (JsonProcessingException e) {
            throw new RuntimeException("Failed to serialize notification event", e);
        }
    }
}
