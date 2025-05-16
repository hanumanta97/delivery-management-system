# 🚚 Delivery Management System - Falcon Framework Assignment

## 📌 Objective

Design and build a **Delivery Management System** using the **Falcon** framework that allows admins to manage delivery orders, assign drivers, track statuses, and expose APIs for delivery operations.

---

## 📄 Description

This system streamlines the process of:

- Creating and managing delivery orders
- Assigning delivery personnel (drivers)
- Tracking order statuses (Pending, In-Transit, Delivered)
- Admin-level operations via APIs
- Exposing RESTful APIs for delivery updates and listings

---

## 🧩 Core Features

- 📦 **Order Management**: Create, update, and delete delivery orders with sender and receiver info.
- 👨‍✈️ **Driver Assignment**: Assign drivers to active delivery orders.
- 📍 **Delivery Tracking**: Track and update real-time delivery statuses.
- 🛠️ **Admin Interface**: Manage delivery system via database/admin tools (Falcon doesn't include built-in admin UI like Django).
- 🌐 **RESTful APIs**: API endpoints for creating orders, assigning drivers, updating statuses, and retrieving order info.

---

## 🗃️ Models Overview

- `DeliveryOrder`: Stores order details such as sender name, receiver name, address, etc.
- `Driver`: Stores driver information and availability.
- `OrderStatusLog`: Maintains a log of all status changes for each delivery order.
- (Optional) `City/Region`: For scalable city/region-based delivery zones.

---

## 📡 API Endpoints

> Base URL: `/api/`

| Endpoint                      | Method | Description                        |
|-------------------------------|--------|------------------------------------|
| `/orders/`                    | GET    | List all delivery orders           |
| `/orders/<id>/`               | GET    | Get specific order details         |
| `/orders/create/`             | POST   | Create a new delivery order        |
| `/orders/<id>/status/`        | POST   | Update delivery status             |
| `/orders/<id>/assign-driver/` | POST   | Assign a driver to an order        |

### 🔄 Sample Payload for Status Update

```json
{
  "status": "in_transit"
}
