from __future__ import annotations

import pendulum
from airflow.decorators import dag, task

from include.etl_logic import (
    build_orders_dataframe,
    dataframe_to_console_text,
    extract_orders_json,
    flatten_orders,
)


@dag(
    dag_id="lab6_hourly_json_etl",
    description="Laboratory work 6: simple hourly JSON ETL with TaskFlow API.",
    schedule="@hourly",
    start_date=pendulum.datetime(2026, 5, 22, tz="Europe/Kyiv"),
    catchup=False,
    tags=["lab6", "etl", "taskflow"],
)
def lab6_hourly_json_etl():
    @task
    def extract() -> list[dict]:
        data = extract_orders_json()
        print("Extracted nested JSON:")
        print(data)
        return data

    @task
    def transform(nested_orders: list[dict]) -> list[dict]:
        flat_orders = flatten_orders(nested_orders)
        print("Transformed flat JSON rows:")
        print(flat_orders)
        return flat_orders

    @task
    def load(flat_orders: list[dict]) -> int:
        dataframe = build_orders_dataframe(flat_orders)
        print("Loaded DataFrame:")
        print(dataframe_to_console_text(dataframe))
        return len(dataframe)

    load(transform(extract()))


lab6_hourly_json_etl()
