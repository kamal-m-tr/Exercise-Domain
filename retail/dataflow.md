# Dataflow — Retail Order Management

**Rules enforced:**
- Instructions(...) = human-provided values only (names, emails, free-text, quantities, prices)
- No identifiers (any field ending with `_id`) inside Instructions(...)
- Dataflow is a strict mirror of Policy steps
- Validations are inline with the tool call that provides the data

---

## SOP 1 — Sales Order Creation

```
Instructions(email) -> get_user_info(email)
Instructions(product_name) -> get_product_info(name)
get_user_info(user_id) + Instructions(payment_method) -> create_sales_order(user_id, payment_method)
create_sales_order(sales_order_id) + get_product_info(product_id) + Instructions(quantity) -> add_sales_order_item(sales_order_id, product_id, quantity)
create_sales_order(sales_order_id) + get_user_info(address) + Instructions(shipping_method) -> create_shipping(sales_order_id, address, method)
```

---

## SOP 2 — Sales Order Cancellation

```
Instructions(email) -> get_user_info(email)
get_user_info(user_id) -> get_sales_order_info(user_id)
get_sales_order_info(sales_order_id) + Instructions(cancel_reason) -> update_sales_order(sales_order_id, cancel_reason)
get_sales_order_info(sales_order_id) -> get_shipping_info(sales_order_id)
get_shipping_info(shipping_id) -> update_shipping(shipping_id)
```

---

## SOP 3 — Order Tracking

```
Instructions(email) -> get_user_info(email)
get_user_info(user_id) -> get_sales_order_info(user_id)
get_sales_order_info(sales_order_id) -> get_sales_order_items(sales_order_id)
get_sales_order_info(sales_order_id) -> get_shipping_info(sales_order_id)
```

---

## SOP 4 — Purchase Order Creation

```
Instructions(email) -> get_user_info(email)
Instructions(supplier_name) -> get_supplier_info(name)
Instructions(product_name) -> get_product_info(name)
get_supplier_info(supplier_id) -> create_purchase_order(supplier_id)
create_purchase_order(purchase_order_id) + get_product_info(product_id) + Instructions(quantity, unit_cost) -> add_purchase_order_item(purchase_order_id, product_id, quantity, unit_cost)
```

---

## SOP 5 — Purchase Order Receiving

```
Instructions(email) -> get_user_info(email)
Instructions(supplier_name) -> get_supplier_info(name)
get_supplier_info(supplier_id) -> get_purchase_order_info(supplier_id)
get_purchase_order_info(purchase_order_id) -> get_purchase_order_items(purchase_order_id)
get_purchase_order_info(purchase_order_id) -> update_purchase_order(purchase_order_id)
```

---

## SOP 6 — Shipping Status Update

```
Instructions(email) -> get_user_info(email)
get_user_info(user_id) -> get_sales_order_info(user_id)
get_sales_order_info(sales_order_id) -> get_shipping_info(sales_order_id)
get_shipping_info(shipping_id) -> update_shipping(shipping_id)
get_sales_order_info(sales_order_id) -> update_sales_order(sales_order_id)
```

---

## SOP 7 — Supplier Management

**Scenario A: New Supplier**
```
Instructions(email) -> get_user_info(email)
Instructions(supplier_name) -> get_supplier_info(name) [not found]
Instructions(name, contact_email, address, city, state, zip_code, country) -> create_supplier(...)
```

**Scenario B: Update Existing Supplier**
```
Instructions(email) -> get_user_info(email)
Instructions(supplier_name) -> get_supplier_info(name) [found]
get_supplier_info(supplier_id) + Instructions(name, contact_email, address, city, state, zip_code, country) -> update_supplier(supplier_id, ...)
```

---

## SOP 8 — Product Catalog Management

**Scenario A: New Product**
```
Instructions(email) -> get_user_info(email)
Instructions(supplier_name) -> get_supplier_info(name)
Instructions(product_name) -> get_product_info(name) [not found]
get_supplier_info(supplier_id) + Instructions(name, description, unit_price) -> create_product(supplier_id, ...)
```

**Scenario B: Update Existing Product**
```
Instructions(email) -> get_user_info(email)
Instructions(supplier_name) -> get_supplier_info(name)
Instructions(product_name) -> get_product_info(name) [found]
get_product_info(product_id) + Instructions(name, description, unit_price) -> update_product(product_id, ...)
```

---

## SOP 9 — User Onboarding

```
Instructions(email) -> get_user_info(email) [not found]
Instructions(first_name, last_name, email, address, city, state, zip_code, country) -> create_user(...)
```

**Note:** If get_user_info returns a user, halt execution.
