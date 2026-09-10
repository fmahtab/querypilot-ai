# Data ingestion

## Overview

QueryPilot includes an importer for the
[Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).

The dataset provides anonymized e-commerce activity, including:

- orders
- order items
- products
- product categories
- sellers
- prices
- timestamps
- order statuses

QueryPilot uses this data to demonstrate natural-language analysis over
relational business data.

The raw dataset is not committed to this repository.

## Download the dataset

Download and extract the Olist dataset from Kaggle.

The data can be stored outside the repository or under:

```text
data/raw/olist/
```

The repository ignores `data/raw/`, preventing the downloaded CSV files from
being committed.

The importer requires these files:

```text
olist_orders_dataset.csv
olist_order_items_dataset.csv
olist_products_dataset.csv
product_category_name_translation.csv
olist_sellers_dataset.csv
```

Other files included in the Olist download are not currently required.

## Prepare the database

Start the local PostgreSQL container:

```bash
docker compose up -d db
```

Apply the database migrations:

```bash
alembic upgrade head
```

The default local connection is:

```text
postgresql+psycopg://postgres:testdb@localhost:5433/querypilot
```

The importer uses the `DATABASE_URL` environment variable when it is defined.
Otherwise, it uses the default local Docker connection.

## Run the importer

Import the default deterministic sample:

```bash
python -m scripts.import_olist data/raw/olist
```

The default sample contains a maximum of 10,000 orders.

Import a different number of orders:

```bash
python -m scripts.import_olist data/raw/olist --orders 20000
```

Use a different database:

```bash
python -m scripts.import_olist data/raw/olist \
  --database-url postgresql+psycopg://user:password@host:5432/database
```

## Existing data protection

By default, the importer refuses to run when any target transactional table
already contains records.

This protects existing data from accidental duplication.

To replace existing imported transactional data:

```bash
python -m scripts.import_olist data/raw/olist --reset
```

The reset operation affects:

- `order_items`
- `orders`
- `inventory`
- `products`
- `stores`
- `categories`

It does not delete:

- RAG chunks
- user memories

Always review the selected database connection before using `--reset`.

## Order selection

An Olist order can contain products from multiple sellers.

QueryPilot currently stores one `store_id` on each order:

```text
orders.store_id
```

That schema cannot accurately represent one order fulfilled by multiple
sellers. The importer therefore selects only orders associated with exactly one
Olist seller.

This is a per-order restriction. The final `stores` table still contains
multiple seller records because different imported orders belong to different
sellers.

A fixed random seed is used when sampling orders, so repeated imports with the
same source files and options select the same records.

## Date handling

Olist contains historical transactions.

By default, the importer shifts the selected dataset forward so that its latest
order occurs on the current date. Every timestamp is shifted by the same
duration.

This preserves:

- chronological order
- intervals between orders
- weekly and seasonal patterns within the selected sample

It also keeps relative demo questions useful:

- Which seller generated the most revenue last month?
- Which category performed best during the previous quarter?
- How many orders were completed this month?

To retain the original Olist timestamps:

```bash
python -m scripts.import_olist data/raw/olist --preserve-dates
```

Shifted dates are transformed demonstration values and should not be described
as original Olist timestamps.

## Field mapping

### Categories

| QueryPilot field | Source |
|---|---|
| `name` | English Olist category translation |
| `description` | `NULL` |

Olist provides category names but not meaningful descriptions. The importer
leaves the nullable description field empty rather than repeating provenance
text in every row.

### Products

| QueryPilot field | Source or transformation |
|---|---|
| `name` | Generated from category and shortened product ID |
| `sku` | Olist product ID with an `OL-` prefix |
| `category_id` | Mapped translated category |
| `unit_price` | Median observed selling price |
| `cost_price` | Deterministically estimated from selling price |
| `is_active` | Set to `true` |

Olist does not provide readable product names or actual cost prices.

A generated product name resembles:

```text
Art Product A1B2C3D4
```

This name is useful for demonstration but is not an original product name.

### Stores

| QueryPilot field | Source or transformation |
|---|---|
| `store_code` | Shortened seller ID with an `OL-` prefix |
| `name` | Seller city plus shortened seller ID |
| `city` | Olist seller city |
| `state` | Olist seller state |
| `is_active` | Set to `true` |

Olist sellers are mapped to QueryPilot stores because sellers are the
fulfillment entities available in the source data.

A generated store name resembles:

```text
Sao Paulo Seller A1B2C3D4
```

These rows represent marketplace sellers, not verified physical RetailStar
locations.

### Orders

| QueryPilot field | Source or transformation |
|---|---|
| `order_number` | Olist order ID with an `OL-` prefix |
| `store_id` | The order’s single seller |
| `order_date` | Original or shifted purchase timestamp |
| `fulfillment_type` | Set to `ecommerce` |
| `status` | Simplified Olist order status |

Status mapping:

| Olist status | QueryPilot status |
|---|---|
| `delivered` | `completed` |
| `shipped` | `completed` |
| `canceled` | `cancelled` |
| `unavailable` | `cancelled` |
| Other statuses | `pending` |

### Order items

| QueryPilot field | Source or transformation |
|---|---|
| `order_id` | Imported QueryPilot order |
| `product_id` | Imported QueryPilot product |
| `quantity` | Number of matching source lines |
| `unit_price` | Average price of grouped matching lines |

When an order contains repeated lines for the same product, the importer groups
them into one QueryPilot order item and records the number of lines as the
quantity.

### Inventory

Olist does not provide current inventory.

The importer creates an inventory record for each imported product-and-seller
combination observed in the selected orders.

| QueryPilot field | Transformation |
|---|---|
| `product_id` | Imported product |
| `store_id` | Imported seller/store |
| `reorder_threshold` | Derived from observed sales volume |
| `quantity_on_hand` | Deterministically generated scenario |
| `updated_at` | Import time |

The generated inventory intentionally includes:

- products with no stock
- products below their reorder threshold
- products with normal stock levels

This allows QueryPilot to demonstrate inventory questions. These values must
not be presented as original Olist inventory data.

## Technical identifiers

The importer adds an `OL-` prefix to:

- SKUs
- store codes
- order numbers

These prefixes are technical namespaces. They:

- reduce the risk of collisions with records from other sources
- make imported records traceable to their source
- are not intended as user-facing descriptions

## Source data versus derived data

Source-backed fields include:

- Olist order relationships
- product identifiers
- category assignments
- seller identifiers and locations
- selling prices
- purchase timestamps
- order statuses

Derived or transformed fields include:

- product display names
- store display names
- product cost prices
- inventory quantities
- reorder thresholds
- fulfillment type
- simplified statuses
- shifted order dates, unless `--preserve-dates` is used

QueryPilot’s answers should distinguish source-backed facts from demonstration
values when that distinction affects the meaning of the result.

## Dataset limitations

The Olist source does not contain:

- physical RetailStar locations
- in-store transactions
- genuine BOPIS transactions
- readable product names
- seller business names
- actual product costs
- current inventory quantities
- reorder thresholds

As a result, the demonstration database supports analysis of:

- e-commerce orders
- sellers represented as stores
- categories
- products
- selling prices
- order statuses
- generated inventory scenarios

It cannot provide factual analysis of real RetailStar physical stores, in-store
sales, or BOPIS performance.

RetailStar documents can explain BOPIS policies, but the imported database
cannot measure actual BOPIS activity.

## Production data requirements

The Olist dataset and derived fields are demonstration data. They are not a
replacement for an organization’s operational records.

In a production deployment, the organization must supply or authorize access
to its authoritative data for the features QueryPilot is expected to support.

This may include:

- categories and products
- stores, branches, warehouses, or sellers
- current inventory and reorder thresholds
- orders and order line items
- customers
- returns and refunds
- actual selling prices and costs
- fulfillment types
- order statuses

The organization does not necessarily need to enter records manually. Data can
be loaded from existing systems such as:

- e-commerce platforms
- point-of-sale systems
- ERP systems
- warehouse-management systems
- order-management systems
- existing databases
- APIs
- scheduled CSV exports

### Production integration requirements

Each source requires a documented mapping to QueryPilot’s schema.

Before QueryPilot is allowed to query the imported data, the integration should
validate:

- completeness
- accuracy
- freshness
- referential integrity
- duplicate handling
- metric definitions
- access permissions
- personally identifiable information
- retention requirements

Production database access should use:

- least-privilege credentials
- read-only query permissions where appropriate
- authenticated users
- organization-level data isolation
- query limits and timeouts
- audit logging

RetailStar’s fictional documentation must also be replaced with the
organization’s approved policies, terminology, and business definitions.

In production, the connected operational systems and approved documents become
QueryPilot’s sources of truth.

## Verify an import

After importing, inspect the table counts:

```sql
SELECT COUNT(*) FROM categories;
SELECT COUNT(*) FROM products;
SELECT COUNT(*) FROM stores;
SELECT COUNT(*) FROM inventory;
SELECT COUNT(*) FROM orders;
SELECT COUNT(*) FROM order_items;
```

Check that every imported order has one store:

```sql
SELECT COUNT(*)
FROM orders
WHERE store_id IS NULL;
```

Expected result:

```text
0
```

Inspect order coverage:

```sql
SELECT
    MIN(order_date) AS earliest_order,
    MAX(order_date) AS latest_order,
    COUNT(*) AS order_count
FROM orders;
```

Inspect fulfillment types:

```sql
SELECT
    fulfillment_type,
    COUNT(*) AS order_count
FROM orders
GROUP BY fulfillment_type;
```

For the Olist import, the fulfillment type should be `ecommerce`.

Inspect generated inventory scenarios:

```sql
SELECT
    COUNT(*) FILTER (
        WHERE quantity_on_hand = 0
    ) AS out_of_stock,
    COUNT(*) FILTER (
        WHERE quantity_on_hand > 0
          AND quantity_on_hand < reorder_threshold
    ) AS below_threshold,
    COUNT(*) FILTER (
        WHERE quantity_on_hand >= reorder_threshold
    ) AS adequately_stocked
FROM inventory;
```

## Removing local raw files

After a successful import, the downloaded CSV files can be deleted. PostgreSQL
retains the imported records in its Docker volume.

The data will need to be imported again if the database volume is deleted, for
example:

```bash
docker compose down -v
```