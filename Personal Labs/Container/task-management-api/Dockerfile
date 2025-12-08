# =============================================================================
# DOCKERFILE - Task Management API (Spring Boot)
# =============================================================================
# This is a multi-stage Dockerfile for building and running the Spring Boot app.
# 
# DOCKER CONCEPTS DEMONSTRATED:
# - Multi-stage builds for smaller images
# - Layer caching optimization
# - Non-root user for security
# - Health checks for orchestration
#
# BUILD:   docker build -t task-management-api .
# RUN:     docker run -p 8080:8080 task-management-api
# =============================================================================

# -----------------------------------------------------------------------------
# Stage 1: Build the application
# -----------------------------------------------------------------------------
FROM eclipse-temurin:17-jdk-alpine AS builder

WORKDIR /app

# Copy Maven wrapper and pom.xml first (for layer caching)
COPY mvnw .
COPY .mvn .mvn
COPY pom.xml .

# Download dependencies (cached if pom.xml unchanged)
RUN chmod +x mvnw && ./mvnw dependency:go-offline -B

# Copy source code
COPY src src

# Build the application
RUN ./mvnw clean package -DskipTests

# -----------------------------------------------------------------------------
# Stage 2: Create the runtime image
# -----------------------------------------------------------------------------
FROM eclipse-temurin:17-jre-alpine AS runtime

WORKDIR /app

# Create non-root user for security
# SECURITY TIP: Never run containers as root in production!
RUN addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup

# Copy the JAR from builder stage
COPY --from=builder /app/target/*.jar app.jar

# Change ownership to non-root user
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8080

# Health check
# DOCKER TIP: Health checks are critical for orchestration (Docker Compose, ECS, K8s)
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/actuator/health || exit 1

# JVM optimization for containers
# DOCKER TIP: These settings help the JVM work better in containers
ENV JAVA_OPTS="-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0"

# Run the application
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]
