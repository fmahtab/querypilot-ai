SCHEMA_DESCRIPTION = """
Database: PostgreSQL. Only these tables exist.

Table: orders
- id (integer, primary key)
- order_number (text, unique)
- store_id (integer) -> stores.id
- order_date (timestamp) - when the order was placed
- fulfillment_type (text) - allowed values: ecommerce
- status (text) - allowed values: completed, cancelled, or pending

Table: order_items
- id (integer, primary key)
- order_id (integer) -> orders.id
- product_id (integer) -> products.id
- quantity (integer)
- unit_price (numeric(10,2)) - price actually paid at the time of sale

Table: inventory
- id (integer, primary key)
- product_id (integer) -> products.id
- store_id (integer) -> stores.id
- quantity_on_hand (integer)
- reorder_threshold (integer)
- updated_at (timestamp)

Table: categories
- id (integer, primary_key)
- name (text)
- description (text)

Table: products
- id (integer, primary_key)
- name (text)
- sku (text)
- category_id (integer) -> categories.id
- unit_price (numeric(10,2)) - current list price
- cost_price (numeric(10,2)) - what RetailStar pays per unit (current cost).
- is_active (boolean)
- created_at (timestamp)

Table: stores
- id (integer, primary_key)
- store_code (text, unique)
- name (text)
- city (text)
- state (text) - Brazilian two-letter state code, e.g. SP, RJ
- is_active (boolean)


Business rules:
- Revenue = SUM(order_items.quantity * order_items.unit_price).
  Never use products.unit_price for revenue.
- Profit = SUM(order_items.quantity * (order_items.unit_price - products.cost_price)).
  Requires joining order_items to products.
- Low inventory: quantity_on_hand > 0 AND quantity_on_hand < reorder_threshold.
- Stockout: quantity_on_hand = 0.
- Revenue, profit, and sales counts include only orders with
  status = 'completed' unless the user asks about other statuses.
- Relative dates use CURRENT_DATE. Example for "last month":
  order_date >= date_trunc('month', CURRENT_DATE) - interval '1 month'
  AND order_date < date_trunc('month', CURRENT_DATE)
"""