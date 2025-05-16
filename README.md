# 🚚 Delivery Management System - Django Assignment

## 📌 Objective

Design and build a Django-based **Delivery Management System** that allows admins to manage delivery orders, assign drivers, track statuses, and handle basic reporting.

---

## 📄 Description

This system aims to streamline the process of:

- Creating and managing delivery orders
- Assigning delivery personnel (drivers)
- Tracking order status (Pending, In-Transit, Delivered)
- Admin-level operations via Django Admin
- Exposing APIs for delivery updates and listings

---

## 🧩 Core Features

- 📦 **Order Management**: Create, update, and delete delivery orders with sender/receiver info.
- 👨‍✈️ **Driver Assignment**: Assign drivers to active orders.
- 📍 **Delivery Tracking**: Update and view real-time delivery status.
- 🛠️ **Admin Interface**: Django Admin to manage orders, drivers, and status changes.
- 🌐 **RESTful APIs**: API endpoints for order status updates and listing.

---

## 🗃️ Models Overview

- `DeliveryOrder`: Stores order details, sender, receiver, and delivery address.
- `Driver`: Delivery personnel with availability and name.
- `OrderStatusLog`: Tracks order status changes over time.
- Additional models for cities/regions can be added for scalability.

---

## 📡 API Endpoints

> Base URL: `/api/`

| Endpoint                   | Method | Description                    |
|----------------------------|--------|--------------------------------|
| `/orders/`                 | GET    | List all orders                |
| `/orders/<id>/`           | GET    | Get specific order             |
| `/orders/create/`          | POST   | Create a new delivery order    |
| `/orders/<id>/status/`    | POST   | Update order status            |

Sample payload for status update:

```json
{
  "status": "in_transit"
}
