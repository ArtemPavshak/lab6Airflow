from __future__ import annotations

import unittest

from include.etl_logic import (
    build_orders_dataframe,
    dataframe_to_console_text,
    extract_orders_json,
    flatten_orders,
)


class EtlLogicTest(unittest.TestCase):
    def test_extract_returns_nested_orders(self) -> None:
        data = extract_orders_json()

        self.assertEqual(len(data), 3)
        self.assertIn("order", data[0])
        self.assertIn("customer", data[0]["order"])
        self.assertIn("items", data[0]["order"])

    def test_transform_flattens_one_row_per_item(self) -> None:
        nested = extract_orders_json()
        flat = flatten_orders(nested)

        expected_item_count = sum(len(entry["order"]["items"]) for entry in nested)
        self.assertEqual(len(flat), expected_item_count)
        self.assertEqual(flat[0]["order_id"], "ORD-1001")
        self.assertEqual(flat[0]["customer_city"], "Kyiv")
        self.assertEqual(flat[0]["item_total"], 899.50)
        self.assertNotIn("customer", flat[0])
        self.assertNotIn("payment", flat[0])
        self.assertNotIn("items", flat[0])

    def test_load_builds_dataframe_and_console_text(self) -> None:
        flat = flatten_orders(extract_orders_json())
        dataframe = build_orders_dataframe(flat)
        console_text = dataframe_to_console_text(dataframe)

        self.assertEqual(len(dataframe), 5)
        self.assertIn("order_id", dataframe.columns)
        self.assertIn("customer_name", dataframe.columns)
        self.assertIn("ORD-1002", console_text)
        self.assertIn("SSD 1TB", console_text)


if __name__ == "__main__":
    unittest.main()
