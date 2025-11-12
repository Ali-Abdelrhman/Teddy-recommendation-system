# Product Catalog & User Events Data Requirements

## Overview
This document specifies the exact CSV format required for the product catalog and user events datasets to build recommendation system models.

## Product Catalog CSV Format

### File Name
`product_catalog.csv`

### Required fields and filters

| Field Name | Description | Example |
|-------------|-------------|---------|
| `sku_id` | Unique SKU identifier | "SKU_12345" |
| `title` | Product name | "LEGO Batman Batmobile" |
| `availability` | Stock quantity | 25 |
| `description` | Product description | "Build the iconic Batmobile..." |
| `age_group` | Target age range | "6-8 years" |
| `category` | Main category | "Building Sets" |
| `sub_category` | Subcategory | "Superhero Sets" |
| `price` | Current price | 29.99 |
| `old_price` | Original price (null if no discount) | 39.99 |
| `currency` | Currency code | "USD" |
| `country` | Country code or ID  | "US" |
| `brand` | Brand name | "LEGO" |
| `brand_origin` | Brand origin country| "Denmark" |
| `color` | Primary color | "Black" |
| `features` | Key features (pipe-separated) | "Remote Control|LED Lights|Sound Effects" |
| `tags` | Search tags (pipe-separated) | "batman|superhero|vehicle|collectible" |
| `upc` | Universal Product Code | "123456789012" |
| `image_url` | Product image URL | "https://example.com/image.jpg" |
| `website_url` | Product page URL | "https://example.com/product/sku_12345" |
| `country_availability` | Available countries (pipe-separated) | "US/CA/UK" |

## User Events CSV Format

### File Name
`user_events.csv`

### Required Fields

| Field Name | Description | Example |
|-------------|-------------|---------|
| `event_type` | Type of interaction | "purchase" |
| `session_id` | Session identifier | "session_abc123" |
| `visitor_id` | User/visitor identifier | "visitor_xyz789" |
| `event_time` | Event timestamp | "2025-11-05T10:30:00Z" |
| `product_details` | SKU IDs (pipe-separated) | "SKU_12345|SKU_67890" |
| `country_id` | Country code | "US" |
| `event_quantity` | Quantity for purchases/cart | 2 |
| `order_total` | Total for purchase events | 59.98 |
| `search_query` | Search term for search events | "batman toys" |

