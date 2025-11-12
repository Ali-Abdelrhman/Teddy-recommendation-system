# User Events Fields for Recommended For You Model

## Executive Summary
This document outlines the essential user event fields required for building an effective "Recommended for You" recommendation system for a multi-country toys e-commerce platform.

---

## 🎯 **CORE USER EVENT FIELDS**

### **User Identification**
- `user_id` -- Unique user identifier for linking all user activities

### **Event Classification**
- `event_type` -- Type of interaction (purchase, view, favorite, cart_add, search)
- `event_timestamp` -- When the event occurred for recency weighting

### **Product Information**
- `sku_id` -- Specific SKU for precise item tracking


### **Geographic Context**
- `country_id` -- User's country for geo-specific recommendations

### **Event Details**
- `quantity` -- Number of items (for purchases/cart additions)
- `order_total` -- Total order value (for purchase events)
- `search_query` -- Search term (for search events)

---

## � **EVENT TYPE WEIGHTS**

### **Primary Events (High Signal)**
- `purchase` -- Weight: 5.0 (strongest positive signal)
- `add_to_cart` -- Weight: 3.0 (strong purchase intent)
- `add_to_wishlist` -- Weight: 3.5 (explicit preference)
- `favorite` -- Weight: 3.5 (explicit positive feedback)

### **Secondary Events (Medium Signal)**
- `product_view` -- Weight: 1.0 (basic interest signal)
- `search_click` -- Weight: 1.5 (search-driven interest)
- `category_browse` -- Weight: 0.8 (general browsing)
- `review_read` -- Weight: 1.2 (research behavior)

### **Negative Events**
- `remove_from_cart` -- Weight: -2.0 (negative signal)
- `return_product` -- Weight: -3.0 (dissatisfaction)
- `low_rating` -- Weight: -1.5 (product dislike)

---

## 🚀 **SAMPLE USER EVENT RECORD**

```json
{
  "user_id": "user_12345",
  "device_id": "device_abc789",
  "session_id": "session_xyz456",
  "event_type": "purchase",
  "event_timestamp": "2025-11-04T10:30:00Z",
  "event_weight": 5.0,
  "product_id": "prod_789",
  "sku_id": "sku_456123",
  "category": "Action Figures",
  "brand": "LEGO",
  "price": 29.99,
  "country_id": "US",
  "currency": "USD",
  "quantity": 2,
  "order_total": 59.98,
  "age_group": "6-8 years",
  "page_source": "search_results"
}
```

---

## 💡 **KEY IMPLEMENTATION NOTES**

### **Data Collection Priority**
1. **Essential**: user_id, event_type, product_id, timestamp, country_id
2. **Important**: sku_id, category, brand, price, event_weight
3. **Nice-to-have**: behavioral metadata, time_spent, page_source

### **Event Processing Rules**
1. **Real-time collection** for immediate recommendation updates
2. **Deduplication** to avoid counting same action multiple times
3. **Country filtering** to ensure geo-appropriate recommendations
4. **Age validation** for toy safety compliance

### **Privacy Considerations**
- Use hashed user IDs for privacy protection
- Implement data retention policies (e.g., 2 years)
- Allow user opt-out and data deletion
- Comply with GDPR/CCPA requirements

This structure provides the foundation for building personalized "Recommended for You" models that understand user preferences while maintaining privacy and safety standards.

