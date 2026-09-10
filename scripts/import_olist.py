"""Import a reproducible subset of the Olist dataset into QueryPilot.

Download and extract the Kaggle "Brazilian E-Commerce Public Dataset by Olist",
https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
then run this script from the repository root. The importer uses only
single-seller orders because QueryPilot currently assigns one store to an order.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import math
import os
import random
from collections import defaultdict
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

from sqlalchemy import create_engine, delete, func, select
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.inventory import Inventory
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from app.models.store import Store


DEFAULT_DATABASE_URL = "postgresql+psycopg://postgres:testdb@localhost:5433/querypilot"
RANDOM_SEED = 20260910
REQUIRED_FILES = {
    "orders": "olist_orders_dataset.csv",
    "items": "olist_order_items_dataset.csv",
    "products": "olist_products_dataset.csv",
    "categories": "product_category_name_translation.csv",
    "sellers": "olist_sellers_dataset.csv",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data_dir", type=Path, help="Directory containing the extracted CSV files")
    parser.add_argument("--orders", type=int, default=10_000, help="Maximum orders to import")
    parser.add_argument(
        "--database-url",
        default=os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL),
        help="SQLAlchemy URL; defaults to QueryPilot's local Docker PostgreSQL",
    )
    parser.add_argument(
        "--preserve-dates",
        action="store_true",
        help="Keep Olist's original dates instead of aligning the latest order to today",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Replace transactional data; RAG chunks and user memories are preserved",
    )
    return parser.parse_args()


def csv_rows(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        yield from csv.DictReader(handle)


def resolve_files(data_dir: Path) -> dict[str, Path]:
    paths = {key: data_dir / name for key, name in REQUIRED_FILES.items()}
    missing = [str(path) for path in paths.values() if not path.is_file()]
    if missing:
        raise SystemExit("Missing Olist files:\n  " + "\n  ".join(missing))
    return paths


def parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value)


def stable_fraction(value: str) -> float:
    number = int(hashlib.sha256(value.encode()).hexdigest()[:8], 16)
    return number / 0xFFFFFFFF


def display_category(source_name: str | None, translations: dict[str, str]) -> str:
    if not source_name:
        return "Uncategorized"
    translated = translations.get(source_name, source_name)
    return translated.replace("_", " ").title()


def mapped_status(source_status: str) -> str:
    if source_status in {"delivered", "shipped"}:
        return "completed"
    if source_status in {"canceled", "unavailable"}:
        return "cancelled"
    return "pending"


def reset_transactional_data(db: Session) -> None:
    for model in (OrderItem, Order, Inventory, Product, Store, Category):
        db.execute(delete(model))
    db.commit()


def ensure_empty(db: Session) -> None:
    populated = []
    for model in (Category, Product, Store, Inventory, Order, OrderItem):
        count = db.scalar(select(func.count()).select_from(model)) or 0
        if count:
            populated.append(f"{model.__tablename__}={count}")
    if populated:
        raise SystemExit(
            "Transactional tables are not empty ("
            + ", ".join(populated)
            + "). Use --reset to replace them."
        )


def choose_orders(paths: dict[str, Path], limit: int) -> tuple[list[dict], dict[str, list[dict]]]:
    items_by_order: dict[str, list[dict]] = defaultdict(list)
    sellers_by_order: dict[str, set[str]] = defaultdict(set)
    for row in csv_rows(paths["items"]):
        items_by_order[row["order_id"]].append(row)
        sellers_by_order[row["order_id"]].add(row["seller_id"])

    eligible = [
        row
        for row in csv_rows(paths["orders"])
        if row["order_purchase_timestamp"]
        and row["order_id"] in items_by_order
        and len(sellers_by_order[row["order_id"]]) == 1
    ]
    rng = random.Random(RANDOM_SEED)
    if len(eligible) > limit:
        eligible = rng.sample(eligible, limit)
    eligible.sort(key=lambda row: (row["order_purchase_timestamp"], row["order_id"]))
    return eligible, items_by_order


def import_data(db: Session, paths: dict[str, Path], limit: int, preserve_dates: bool) -> None:
    translations = {
        row["product_category_name"]: row["product_category_name_english"]
        for row in csv_rows(paths["categories"])
    }
    source_products = {row["product_id"]: row for row in csv_rows(paths["products"])}
    source_sellers = {row["seller_id"]: row for row in csv_rows(paths["sellers"])}
    chosen_orders, items_by_order = choose_orders(paths, limit)
    if not chosen_orders:
        raise SystemExit("No eligible single-seller orders were found.")

    chosen_order_ids = {row["order_id"] for row in chosen_orders}
    chosen_items = [item for oid in chosen_order_ids for item in items_by_order[oid]]
    product_ids = sorted({row["product_id"] for row in chosen_items})
    seller_ids = sorted({row["seller_id"] for row in chosen_items})

    category_for_product = {
        product_id: display_category(
            source_products.get(product_id, {}).get("product_category_name"), translations
        )
        for product_id in product_ids
    }
    category_names = sorted(set(category_for_product.values()))
    # Olist provides category names but no descriptions. Leave the nullable
    # field empty instead of storing repetitive dataset-provenance text.
    categories = [Category(name=name, description=None) for name in category_names]
    db.add_all(categories)
    db.flush()
    category_ids = {row.name: row.id for row in categories}

    price_samples: dict[str, list[Decimal]] = defaultdict(list)
    for row in chosen_items:
        price_samples[row["product_id"]].append(Decimal(row["price"]))

    products = []
    for product_id in product_ids:
        prices = sorted(price_samples[product_id])
        unit_price = prices[len(prices) // 2]
        category_name = category_for_product[product_id]
        cost_ratio = Decimal("0.55") + Decimal(str(stable_fraction(product_id) * 0.2))
        products.append(
            Product(
                # Olist does not publish product display names. This neutral,
                # deterministic label remains readable and unique.
                name=f"{category_name} Product {product_id[:8].upper()}",
                sku=f"OL-{product_id.upper()}",
                category_id=category_ids[category_name],
                unit_price=unit_price.quantize(Decimal("0.01")),
                cost_price=(unit_price * cost_ratio).quantize(Decimal("0.01")),
                is_active=True,
            )
        )
    db.add_all(products)
    db.flush()
    product_db_ids = {row.sku[3:].lower(): row.id for row in products}

    stores = []
    for seller_id in seller_ids:
        source = source_sellers[seller_id]
        city = source["seller_city"].replace("_", " ").title()
        stores.append(
            Store(
                store_code=f"OL-{seller_id[:12].upper()}",
                # Olist does not publish seller business names. Include the
                # location plus a short stable identifier without branding the row.
                name=f"{city} Seller {seller_id[:8].upper()}",
                city=city,
                state=source["seller_state"].upper(),
                is_active=True,
            )
        )
    db.add_all(stores)
    db.flush()
    store_db_ids = {seller_id: store.id for seller_id, store in zip(seller_ids, stores)}

    latest_source_date = max(parse_timestamp(row["order_purchase_timestamp"]) for row in chosen_orders)
    date_shift = datetime.now(UTC).replace(tzinfo=None) - latest_source_date
    sales_by_product_store: dict[tuple[int, int], int] = defaultdict(int)

    for index, source_order in enumerate(chosen_orders, start=1):
        source_items = items_by_order[source_order["order_id"]]
        seller_id = source_items[0]["seller_id"]
        order_date = parse_timestamp(source_order["order_purchase_timestamp"])
        if not preserve_dates:
            order_date += date_shift
        order = Order(
            order_number=f"OL-{source_order['order_id']}",
            store_id=store_db_ids[seller_id],
            order_date=order_date,
            fulfillment_type="ecommerce",
            status=mapped_status(source_order["order_status"]),
        )
        db.add(order)
        db.flush()

        grouped: dict[str, list[Decimal]] = defaultdict(list)
        for source_item in source_items:
            grouped[source_item["product_id"]].append(Decimal(source_item["price"]))
        for product_id, prices in grouped.items():
            product_db_id = product_db_ids[product_id]
            store_db_id = store_db_ids[seller_id]
            quantity = len(prices)
            db.add(
                OrderItem(
                    order_id=order.id,
                    product_id=product_db_id,
                    quantity=quantity,
                    unit_price=(sum(prices) / quantity).quantize(Decimal("0.01")),
                )
            )
            sales_by_product_store[(product_db_id, store_db_id)] += quantity
        if index % 1_000 == 0:
            print(f"Prepared {index:,}/{len(chosen_orders):,} orders...")

    now = datetime.now(UTC).replace(tzinfo=None)
    inventory = []
    for (product_id, store_id), units_sold in sorted(sales_by_product_store.items()):
        threshold = max(3, min(25, round(math.sqrt(units_sold) * 2)))
        scenario = stable_fraction(f"{product_id}:{store_id}")
        if scenario < 0.05:
            quantity = 0
        elif scenario < 0.17:
            quantity = max(1, threshold - 1)
        else:
            quantity = threshold + round(scenario * threshold * 2)
        inventory.append(
            Inventory(
                product_id=product_id,
                store_id=store_id,
                quantity_on_hand=quantity,
                reorder_threshold=threshold,
                updated_at=now,
            )
        )
    db.add_all(inventory)
    db.commit()


def print_summary(db: Session) -> None:
    print("Olist import complete:")
    for model in (Category, Product, Store, Inventory, Order, OrderItem):
        count = db.scalar(select(func.count()).select_from(model)) or 0
        print(f"  {model.__tablename__:12} {count:>7,}")


def main() -> None:
    args = parse_args()
    if args.orders < 100:
        raise SystemExit("--orders must be at least 100.")
    paths = resolve_files(args.data_dir)
    engine = create_engine(args.database_url, pool_pre_ping=True)
    with Session(engine) as db:
        reset_transactional_data(db) if args.reset else ensure_empty(db)
        import_data(db, paths, args.orders, args.preserve_dates)
        print_summary(db)


if __name__ == "__main__":
    main()
