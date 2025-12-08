package com.ecommerce.order.controller;

import com.ecommerce.order.dto.CreateOrderRequest;
import com.ecommerce.order.model.Order;
import com.ecommerce.order.model.OrderItem;
import com.ecommerce.order.repository.OrderRepository;
import com.ecommerce.order.service.ProductServiceClient;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.math.BigDecimal;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/orders")
@Tag(name = "Orders", description = "Order management endpoints")
@CrossOrigin(origins = "*")
public class OrderController {

    private final OrderRepository repository;
    private final ProductServiceClient productClient;

    public OrderController(OrderRepository repository, ProductServiceClient productClient) {
        this.repository = repository;
        this.productClient = productClient;
    }

    @GetMapping
    @Operation(summary = "Get all orders")
    public ResponseEntity<List<Order>> getAllOrders() {
        return ResponseEntity.ok(repository.findAll());
    }

    @GetMapping("/{id}")
    @Operation(summary = "Get order by ID")
    public ResponseEntity<Order> getOrder(@PathVariable Long id) {
        return repository.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @GetMapping("/number/{orderNumber}")
    @Operation(summary = "Get order by order number")
    public ResponseEntity<Order> getByOrderNumber(@PathVariable String orderNumber) {
        return repository.findByOrderNumber(orderNumber)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    @Operation(summary = "Create order")
    public ResponseEntity<?> createOrder(@Valid @RequestBody CreateOrderRequest request) {
        Order order = new Order();
        order.setCustomerEmail(request.getCustomerEmail());
        order.setCustomerName(request.getCustomerName());

        for (CreateOrderRequest.OrderItemRequest itemRequest : request.getItems()) {
            // Try to get product info from Product Service (inter-service call)
            ProductServiceClient.ProductInfo productInfo = 
                    productClient.getProduct(itemRequest.getProductId());

            OrderItem item = new OrderItem();
            item.setProductId(itemRequest.getProductId());
            item.setQuantity(itemRequest.getQuantity());

            if (productInfo != null) {
                item.setProductName(productInfo.name());
                item.setPrice(productInfo.price());
            } else {
                // Fallback when product service unavailable
                item.setProductName("Product #" + itemRequest.getProductId());
                item.setPrice(new BigDecimal("0.00"));
            }

            order.addItem(item);
        }

        Order savedOrder = repository.save(order);
        return ResponseEntity.status(HttpStatus.CREATED).body(savedOrder);
    }

    @PatchMapping("/{id}/status")
    @Operation(summary = "Update order status")
    public ResponseEntity<Order> updateStatus(@PathVariable Long id, 
                                               @RequestParam Order.OrderStatus status) {
        return repository.findById(id)
                .map(order -> {
                    order.setStatus(status);
                    return ResponseEntity.ok(repository.save(order));
                })
                .orElse(ResponseEntity.notFound().build());
    }

    @DeleteMapping("/{id}")
    @Operation(summary = "Cancel order")
    public ResponseEntity<Order> cancelOrder(@PathVariable Long id) {
        return repository.findById(id)
                .map(order -> {
                    order.setStatus(Order.OrderStatus.CANCELLED);
                    return ResponseEntity.ok(repository.save(order));
                })
                .orElse(ResponseEntity.notFound().build());
    }

    @GetMapping("/customer/{email}")
    @Operation(summary = "Get orders by customer email")
    public ResponseEntity<List<Order>> getByCustomer(@PathVariable String email) {
        return ResponseEntity.ok(repository.findByCustomerEmail(email));
    }

    @GetMapping("/stats")
    @Operation(summary = "Get order statistics")
    public ResponseEntity<Map<String, Object>> getStats() {
        Map<String, Object> stats = new HashMap<>();
        stats.put("total", repository.count());
        stats.put("pending", repository.findByStatus(Order.OrderStatus.PENDING).size());
        stats.put("processing", repository.findByStatus(Order.OrderStatus.PROCESSING).size());
        stats.put("shipped", repository.findByStatus(Order.OrderStatus.SHIPPED).size());
        stats.put("delivered", repository.findByStatus(Order.OrderStatus.DELIVERED).size());
        return ResponseEntity.ok(stats);
    }
}
