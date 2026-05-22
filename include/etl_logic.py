from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import pandas as pd


def extract_orders_json() -> list[dict[str, Any]]:
    """Generate nested JSON-like data for the extract step."""
    extracted_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

    return [
        {
            "order": {
                "id": "ORD-1001",
                "created_at": extracted_at,
                "status": "paid",
                "customer": {
                    "id": 501,
                    "name": "Olena Kovalenko",
                    "city": "Kyiv",
                    "segment": "retail",
                },
                "payment": {
                    "method": "card",
                    "currency": "UAH",
                    "total": 1849.50,
                },
                "items": [
                    {"sku": "BK-DS-01", "name": "Data Systems Book", "qty": 1, "price": 899.50},
                    {"sku": "USB-C-2M", "name": "USB-C Cable", "qty": 2, "price": 475.00},
                ],
            }
        },
        {
            "order": {
                "id": "ORD-1002",
                "created_at": extracted_at,
                "status": "processing",
                "customer": {
                    "id": 502,
                    "name": "Andrii Shevchenko",
                    "city": "Lviv",
                    "segment": "business",
                },
                "payment": {
                    "method": "invoice",
                    "currency": "UAH",
                    "total": 3299.00,
                },
                "items": [
                    {"sku": "SSD-1TB", "name": "SSD 1TB", "qty": 1, "price": 3299.00},
                ],
            }
        },
        {
            "order": {
                "id": "ORD-1003",
                "created_at": extracted_at,
                "status": "paid",
                "customer": {
                    "id": 503,
                    "name": "Maksym Bondar",
                    "city": "Odesa",
                    "segment": "retail",
                },
                "payment": {
                    "method": "card",
                    "currency": "UAH",
                    "total": 1299.00,
                },
                "items": [
                    {"sku": "HDMI-4K", "name": "HDMI Cable 4K", "qty": 3, "price": 249.00},
                    {"sku": "MOUSE-WL", "name": "Wireless Mouse", "qty": 1, "price": 552.00},
                ],
            }
        },
    ]


def flatten_orders(nested_orders: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Reduce JSON nesting by converting each order item into a flat row."""
    rows: list[dict[str, Any]] = []

    for entry in nested_orders:
        order = entry["order"]
        customer = order["customer"]
        payment = order["payment"]

        for item in order["items"]:
            item_total = round(item["qty"] * item["price"], 2)
            rows.append(
                {
                    "order_id": order["id"],
                    "created_at": order["created_at"],
                    "status": order["status"],
                    "customer_id": customer["id"],
                    "customer_name": customer["name"],
                    "customer_city": customer["city"],
                    "customer_segment": customer["segment"],
                    "payment_method": payment["method"],
                    "currency": payment["currency"],
                    "order_total": payment["total"],
                    "sku": item["sku"],
                    "item_name": item["name"],
                    "quantity": item["qty"],
                    "unit_price": item["price"],
                    "item_total": item_total,
                }
            )

    return rows


def build_orders_dataframe(flat_orders: list[dict[str, Any]]) -> pd.DataFrame:
    """Create a DataFrame for the load step."""
    columns = [
        "order_id",
        "created_at",
        "status",
        "customer_id",
        "customer_name",
        "customer_city",
        "customer_segment",
        "payment_method",
        "currency",
        "order_total",
        "sku",
        "item_name",
        "quantity",
        "unit_price",
        "item_total",
    ]
    return pd.DataFrame(flat_orders, columns=columns)


def dataframe_to_console_text(dataframe: pd.DataFrame) -> str:
    """Render the load result as readable console output."""
    if dataframe.empty:
        return "No rows to load."

    return dataframe.to_string(index=False)
