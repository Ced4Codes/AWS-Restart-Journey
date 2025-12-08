package com.notifications.kafka;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.notifications.model.NotificationEvent;
import com.notifications.service.NotificationDispatcher;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.support.Acknowledgment;
import org.springframework.kafka.support.KafkaHeaders;
import org.springframework.messaging.handler.annotation.Header;
import org.springframework.messaging.handler.annotation.Payload;
import org.springframework.stereotype.Service;

/**
 * Kafka Consumer Service
 * Consumes notification events from Kafka and dispatches them.
 * 
 * KAFKA CONCEPTS:
 * - Consumers read from topics
 * - Consumer groups enable parallel processing
 * - Offsets track what's been processed
 * - Manual ACK for reliability
 */
@Service
public class NotificationConsumer {

    private static final Logger log = LoggerFactory.getLogger(NotificationConsumer.class);

    private final ObjectMapper objectMapper;
    private final NotificationDispatcher dispatcher;
    private final NotificationProducer producer;

    public NotificationConsumer(ObjectMapper objectMapper, 
                                 NotificationDispatcher dispatcher,
                                 NotificationProducer producer) {
        this.objectMapper = objectMapper;
        this.dispatcher = dispatcher;
        this.producer = producer;
    }

    /**
     * Main notification consumer
     * Listens to the notifications topic and processes events
     */
    @KafkaListener(
        topics = "${app.kafka.topic.notifications:notifications}",
        groupId = "${app.kafka.consumer.group-id:notification-group}",
        containerFactory = "kafkaListenerContainerFactory"
    )
    public void consumeNotification(
            @Payload String message,
            @Header(KafkaHeaders.RECEIVED_PARTITION) int partition,
            @Header(KafkaHeaders.OFFSET) long offset,
            Acknowledgment ack) {

        log.info("📥 Received message from partition: {}, offset: {}", partition, offset);

        try {
            NotificationEvent event = objectMapper.readValue(message, NotificationEvent.class);
            log.info("📬 Processing notification: {} - type: {}, channel: {}",
                    event.getEventId(), event.getEventType(), event.getChannel());

            // Update status
            event.setStatus(NotificationEvent.EventStatus.PROCESSING);

            // Dispatch to appropriate channel
            boolean success = dispatcher.dispatch(event);

            if (success) {
                event.setStatus(NotificationEvent.EventStatus.SENT);
                log.info("✅ Notification processed successfully: {}", event.getEventId());
                ack.acknowledge(); // Commit offset
            } else {
                log.warn("⚠️ Notification dispatch failed, sending to DLQ: {}", event.getEventId());
                producer.sendToDeadLetterQueue(event);
                ack.acknowledge(); // Still commit to avoid infinite retry
            }

        } catch (JsonProcessingException e) {
            log.error("❌ Failed to deserialize message: {}", message, e);
            ack.acknowledge(); // Bad message, skip it
        } catch (Exception e) {
            log.error("❌ Error processing notification, will retry", e);
            // Don't acknowledge - message will be redelivered
        }
    }

    /**
     * Dead Letter Queue consumer
     * Processes failed notifications for analysis or retry
     */
    @KafkaListener(
        topics = "${app.kafka.topic.dlq:notifications-dlq}",
        groupId = "${app.kafka.consumer.group-id:notification-group}-dlq"
    )
    public void consumeDeadLetter(
            @Payload String message,
            @Header(KafkaHeaders.RECEIVED_PARTITION) int partition,
            Acknowledgment ack) {

        log.warn("☠️ Processing DLQ message from partition: {}", partition);

        try {
            NotificationEvent event = objectMapper.readValue(message, NotificationEvent.class);
            
            // Log for monitoring/alerting
            log.error("💀 DEAD LETTER: eventId={}, type={}, recipient={}, error={}",
                    event.getEventId(),
                    event.getEventType(),
                    event.getRecipient(),
                    event.getStatus());

            // In production: store to database for manual review
            // or trigger alerts to operations team
            
            ack.acknowledge();
        } catch (Exception e) {
            log.error("❌ Failed to process DLQ message", e);
            ack.acknowledge();
        }
    }
}
