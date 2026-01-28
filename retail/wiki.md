# Retail Order Management Database Wiki

## Overview

The Retail Order Management Database supports supplier management, product catalog, customer management, purchase order processing, sales order management, and shipping operations. The database interacts exclusively through provided APIs, ensuring secure and structured data management.

## Database Schema

### Suppliers

Stores supplier/vendor information.

* **Fields:** supplier_id, name, contact_email, address, city, state, zip_code, country

### Products

Maintains product catalog information.

* **Fields:** product_id, name, description, supplier_id, unit_price

### Users

Maintains customer profiles.

* **Fields:** user_id, first_name, last_name, email, address, city, state, zip_code, country

### Purchase Orders

Tracks orders placed with suppliers for inventory replenishment.

* **Fields:** purchase_order_id, supplier_id, order_date, status

### Purchase Order Items

Line items within purchase orders.

* **Fields:** po_item_id, purchase_order_id, product_id, quantity, unit_cost

### Sales Orders

Tracks customer orders.

* **Fields:** sales_order_id, user_id, order_date, status, payment_method, cancel_reason

### Sales Order Items

Line items within sales orders.

* **Fields:** so_item_id, sales_order_id, product_id, quantity

### Shipping

Tracks shipment information for sales orders.

* **Fields:** shipping_id, sales_order_id, address, estimate_deliver_date, real_deliver_date, method, tracking_number, status

## API Interactions

APIs provided are the exclusive means for the agent to interact with the database, managing suppliers, products, users, purchase orders, sales orders, and shipping.

### Key API Categories

* **Supplier Management:** View and manage supplier information.
* **Product Management:** View and manage product catalog.
* **User Management:** View and manage customer profiles.
* **Purchase Order Management:** Create and manage supplier orders.
* **Sales Order Management:** Create and manage customer orders.
* **Shipping Management:** Track and update shipment information.

## Retail Agent Policy

### General Guidelines

* Operate exclusively through APIs.
* Obtain explicit user-provided information for every database interaction.

### Authentication & Permissions

* Always authenticate user identity before performing actions.
* Verify user permissions through provided APIs.

### Order Management

* Validate product availability before order creation.
* Verify supplier-product relationships for purchase orders.
* Ensure proper order status transitions.

### Shipping Management

* Link shipments to valid sales orders.
* Track shipping status accurately.
* Update delivery information promptly.

### Data Integrity & Security

* Validate data explicitly through APIs.
* Adhere strictly to privacy standards and user consent.
