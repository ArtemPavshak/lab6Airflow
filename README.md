
# Lab 6: Apache Airflow ETL Orchestration

This project implements a simple Apache Airflow ETL process for laboratory work 6.

## What Is Implemented

- `extract`: generates nested JSON-like order data.
- `transform`: reduces JSON nesting and creates one flat row per order item.
- `load`: creates a Pandas DataFrame and prints it to the Airflow task log.
- The DAG uses the Airflow TaskFlow API, so values are passed between tasks through XCom automatically.
- The DAG is scheduled to run every hour with `schedule="@hourly"`.

## Project Structure

- `dags/lab6_hourly_json_etl.py` - Airflow DAG and TaskFlow tasks.
- `include/etl_logic.py` - reusable ETL logic without Airflow dependencies.
- `tests/test_etl_logic.py` - local tests for extract, transform, and load logic.
- `requirements.txt` - Python dependency list for the Airflow image.
- `Dockerfile` and `.astro/config.yaml` - Astro project files.

## Local Logic Test

Run this from the project root:

```powershell
& 'C:\Users\Artem\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest discover -s tests
```

To run the ETL logic locally and print the final DataFrame:

```powershell
& 'C:\Users\Artem\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' scripts/run_local_etl.py
```

## Airflow Run With Astro

Use the Astro CLI from `C:\astro.exe`.

Run Airflow from the project root:

```powershell
& 'C:\astro.exe' dev start
```

Open the Airflow UI:

- URL: `http://localhost:8080`
- Username: `admin`
- Password: `admin`

Unpause the `lab6_hourly_json_etl` DAG and trigger it manually or wait for the hourly schedule.

Useful commands:

```powershell
& 'C:\astro.exe' dev restart
& 'C:\astro.exe' dev stop
& 'C:\astro.exe' dev logs
& 'C:\astro.exe' dev run dags list
& 'C:\astro.exe' dev run dags test lab6_hourly_json_etl 2026-05-22T19:15:00+00:00
```

## Expected Result

In the `load` task logs, Airflow prints a table with flattened order item rows. Each row contains order, customer, payment, and item fields in one flat DataFrame.
