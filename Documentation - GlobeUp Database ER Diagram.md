# GlobeUp ER Diagram

# 🌐 GlobeUp E-commerce Platform Documentation
Welcome to the official documentation for **GlobeUp**, a modern and scalable e-commerce platform designed to support customers, suppliers, resellers, and administrators. This guide provides a comprehensive overview of the database schema, data flow, and how core features are structured.

---

## 📘 Table of Contents
1. [﻿Introduction](https://#introduction) 
2. [﻿User System](https://#user-system) 
3. [﻿Product Catalog](https://#product-catalog) 
4. [﻿User Interactions](https://#user-interactions) 
5. [﻿Shopping Cart & Wishlist](https://#shopping-cart--wishlist) 
6. [﻿Orders & Payments](https://#orders--payments) 
7. [﻿System Settings](https://#system-settings) 
8. [﻿Entity Relationships](https://#entity-relationships) 
9. [﻿Notes & Enums](https://#notes--enums) 
---

## 🧭 Introduction
**GlobeUp** is a full-featured e-commerce platform with support for:

- Role-based user types (customers, suppliers, admins, etc.)
- Product catalog with categories, brands, and variants
- Shopping cart and wishlist
- Orders and secure payments
- Reviews and ratings
- Admin-level configurations for mail, fraud, IP blocks, and more
---

## 👤 User System
### `user` 
Stores login and identification details.

| Field | Type | Description |
| ----- | ----- | ----- |
| id | string | Primary Key |
| email | string | Unique, indexed |
| phone_number | string | Unique, indexed |
| is_verified | boolean | Whether the account is verified |
| date_joined | timestamp | Indexed |
### `user_profile` 
Holds personal and role-based information.

| Field | Type | Description |
| ----- | ----- | ----- |
| id | string | Primary Key |
| user_id | string | FK to  |
| user_type | string | <p>Enum: </p><p>, </p><p>, </p><p>, </p> |
| first_name, last_name | string | Indexed |
| date_of_birth, gender | date, string | <p>Gender enum: </p><p>, </p><p>, </p> |
| profile_image | string | URL/path to image |
| default_shipping_address | text | Default address |
| modified_at | timestamp | Last profile update |
---

## 📦 Product Catalog
### `category` 
Organizes products hierarchically.

| Field | Type | Notes |
| ----- | ----- | ----- |
| id | string | Primary Key |
| name, slug | string | Unique, indexed |
| parent_id | string | <p>FK to </p><p> (self-ref)</p> |
| created_at | timestamp |  |
### `brand` 
Groups products by brand.

| Field | Type | Notes |
| ----- | ----- | ----- |
| id | string | Primary Key |
| name, slug | string | Unique or indexed |
| created_at | timestamp |  |
### `product` 
Core product information.

| Field | Type | Notes |
| ----- | ----- | ----- |
| id | string | PK |
| name, slug | string | Indexed, unique |
| category_id | string | FK to  |
| brand_id | string | FK to  |
| description | text |  |
| is_active | boolean | Indicates product availability |
| created_at | timestamp |  |
### `product_variant` 
Different variations of a product (e.g. size/color).

| Field | Type | Description |
| ----- | ----- | ----- |
| id | string | PK |
| product_id | string | FK to  |
| sku | string | Unique SKU |
| price | decimal | Indexed current price |
| old_price | decimal | Optional previous price |
| stock | int | Must be positive |
| color | string | Indexed |
| size | string | <p>Enum: </p><p>, </p><p>, </p><p>, etc.</p> |
| is_active | boolean | Is this variant available |
| created_at, updated_at | timestamp |  |
---

## ⭐ User Interactions
### `review` 
User-generated product reviews.

| Field | Type | Description |
| ----- | ----- | ----- |
| id | string | PK |
| product_id | string | FK to  |
| user_id | string | FK to  |
| rating | smallint | Indexed (e.g. 1 to 5) |
| comment | text | Optional |
| status | string | <p>Enum: </p><p>, </p> |
| created_at | timestamp |  |
### `wishlist` 
Tracks products users want to save.

| Field | Type | Description |
| ----- | ----- | ----- |
| id | string | PK |
| user_id | string | FK to  |
| product_id | string | FK to  |
---

## 🛒 Shopping Cart & Wishlist
### `cart` 
User’s shopping cart.

| Field | Type | Notes |
| ----- | ----- | ----- |
| id | string | PK |
| user_id | string | FK to  |
| created_at | timestamp |  |
### `cart_item` 
Products inside a cart.

| Field | Type | Notes |
| ----- | ----- | ----- |
| id | string | PK |
| cart_id | string | FK to  |
| product_variant_id | string | FK to  |
| quantity | int | Must be positive |
---

## 📦 Orders & Payments
### `order` 
Tracks placed orders.

| Field | Type | Description |
| ----- | ----- | ----- |
| id | string | PK |
| user_id | string | FK to  |
| status | string | <p>Enum: </p><p>, </p><p>, etc.</p> |
| total_amount | decimal | Total cost |
| shipping_address | text | Destination address |
| created_at | timestamp |  |
### `order_item` 
Items within an order.

| Field | Type | Notes |
| ----- | ----- | ----- |
| id | string | PK |
| order_id | string | FK to  |
| product_variant_id | string | FK to  |
| quantity | int | Must be positive |
| price | decimal | Price per item |
### `payment` 
Payment records for orders.

| Field | Type | Description |
| ----- | ----- | ----- |
| id | string | PK |
| order_id | string | FK to  |
| provider | string | e.g., Stripe, PayPal |
| transaction_id | string | Unique transaction reference |
| amount | decimal | Paid amount |
| status | string | <p>Enum: </p><p>, </p><p>, etc.</p> |
| created_at | timestamp |  |
---

## ⚙️ System Settings
### `smtp_mail` 
Email service settings.

| Field | Type | Description |
| ----- | ----- | ----- |
| id | string | PK |
| host, username, password | string | Mail credentials |
| from_address, from_name | string | Sender details |
### `fraud_api` 
Third-party fraud detection.

| Field | Type | Description |
| ----- | ----- | ----- |
| id | string | PK |
| type | string | API name/provider |
| api_url | string | URL |
| api_key | string | Key/token |
### `ip_block` 
Block malicious IPs.

| Field | Type | Notes |
| ----- | ----- | ----- |
| id | string | PK |
| ip_address | string | Unique, up to 45 chars |
| reason | text | Why it was blocked |
### `contact` 
Public contact info.

| Field | Type | Description |
| ----- | ----- | ----- |
| id | string | PK |
| hotline_number | string |  |
| email | string |  |
| phone_number | string |  |
| whatsapp_number | string |  |
| address | text |  |
| google_map | string | Map URL |
| status | string | Indexed |
### `shipping_charge` 
Charges by delivery area.

| Field | Type | Description |
| ----- | ----- | ----- |
| id | string | PK |
| area | string | Unique location |
| amount | decimal | Cost |
---

## 🔗 Entity Relationships
- One-to-One:
`user_profile.user_id`  → `user.id` 
- One-to-Many:
    - `category.parent_id`  → `category.id` 
    - `product.category_id`  → `category.id` 
    - `product.brand_id`  → `brand.id` 
    - `product_variant.product_id`  → `product.id` 
    - `review.product_id`  → `product.id` 
    - `review.user_id`  → `user.id` 
    - `wishlist.user_id`  → `user.id` 
    - `wishlist.product_id`  → `product.id` 
    - `cart.user_id`  → `user.id` 
    - `cart_item.cart_id`  → `cart.id` 
    - `cart_item.product_variant_id`  → `product_variant.id` 
    - `order.user_id`  → `user.id` 
    - `order_item.order_id`  → `order.id` 
    - `order_item.product_variant_id`  → `product_variant.id` 
    - `payment.order_id`  → `order.id` 
---

## 📌 Notes & Enums
### User Types:
- `customer` 
- `supplier` 
- `reseller` 
- `admin` 
### Gender Enum:
- `M`  (Male)
- `F`  (Female)
- `O`  (Other)
### Product Variant Sizes:
- `s` , `m` , `l` , `xl` , `xxl` 
### Review Status:
- `pending` , `published` 
### Order Status:
- `pending` , `processing` , `shipped` , `delivered` , `cancelled` 
### Payment Status:
- `successful` , `failed` , `refunded` 
---

>  📍 This documentation serves as the foundation for building, scaling, and maintaining **GlobeUp**. Make sure to sync it with database migrations and business rule updates as needed. 



