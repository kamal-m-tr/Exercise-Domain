# Tool Inventory - Retail Domain

**Total:** 23 tools (8 Getters, 15 Setters) — Ratio: 65/35

---

## Getter Tools

| Tool | Parameters | Description |
|------|------------|-------------|
| `get_user_info` | user_id?, email? | Retrieves user records by ID or email |
| `get_supplier_info` | supplier_id?, name? | Retrieves supplier records by ID or name |
| `get_product_info` | product_id?, name?, supplier_id? | Retrieves product records with filters |
| `get_purchase_order_info` | purchase_order_id?, supplier_id?, status? | Retrieves purchase orders with filters |
| `get_purchase_order_items` | purchase_order_id, product_id? | Retrieves purchase order line items |
| `get_sales_order_info` | sales_order_id?, user_id?, status? | Retrieves sales orders with filters |
| `get_sales_order_items` | sales_order_id, product_id? | Retrieves sales order line items |
| `get_shipping_info` | shipping_id?, sales_order_id?, status? | Retrieves shipping records |

---

## Setter Tools

| Tool | Parameters | Description |
|------|------------|-------------|
| `create_supplier` | name, contact_email, address, city, state, zip_code, country | Creates a new supplier |
| `update_supplier` | supplier_id, name?, contact_email?, address?, city?, state?, zip_code?, country? | Updates supplier information |
| `create_product` | name, description, supplier_id, unit_price | Creates a new product |
| `update_product` | product_id, name?, description?, supplier_id?, unit_price? | Updates product information |
| `create_user` | first_name, last_name, email, address, city, state, zip_code, country | Creates a new user account |
| `update_user` | user_id, first_name?, last_name?, email?, address?, city?, state?, zip_code?, country? | Updates user information |
| `create_purchase_order` | supplier_id, order_date?, status? | Creates a new purchase order |
| `update_purchase_order` | purchase_order_id, status | Updates purchase order status |
| `add_purchase_order_item` | purchase_order_id, product_id, quantity, unit_cost | Adds item to purchase order |
| `create_sales_order` | user_id, payment_method, order_date?, status? | Creates a new sales order |
| `update_sales_order` | sales_order_id, status?, cancel_reason? | Updates sales order status |
| `add_sales_order_item` | sales_order_id, product_id, quantity | Adds item to sales order |
| `create_shipping` | sales_order_id, address, estimate_deliver_date, method | Creates shipping record |
| `update_shipping` | shipping_id, status?, tracking_number?, real_deliver_date? | Updates shipping information |
| `transfer_to_human` | reason | Escalates to human support |

---

*Legend: `?` = optional parameter*
