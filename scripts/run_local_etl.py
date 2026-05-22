from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from include.etl_logic import (
    build_orders_dataframe,
    dataframe_to_console_text,
    extract_orders_json,
    flatten_orders,
)


def main() -> None:
    nested_orders = extract_orders_json()
    flat_orders = flatten_orders(nested_orders)
    dataframe = build_orders_dataframe(flat_orders)

    print("EXTRACT: nested JSON records")
    print(nested_orders)
    print()
    print("TRANSFORM: flat JSON rows")
    print(flat_orders)
    print()
    print("LOAD: DataFrame")
    print(dataframe_to_console_text(dataframe))


if __name__ == "__main__":
    main()
