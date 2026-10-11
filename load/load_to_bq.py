import sys

from google.cloud import bigquery

from extract.extract_weather import fetch_all

PROJECT_ID = "weather-elt-portfolio-4809"
TABLE = f"{PROJECT_ID}.raw.weather_daily"

SCHEMA = [
    bigquery.SchemaField("city", "STRING"),
    bigquery.SchemaField("date", "DATE"),
    bigquery.SchemaField("temp_max_c", "FLOAT"),
    bigquery.SchemaField("temp_min_c", "FLOAT"),
    bigquery.SchemaField("precip_mm", "FLOAT"),
    bigquery.SchemaField("loaded_at", "TIMESTAMP"),
]


def load_rows(rows, table=TABLE):
    client = bigquery.Client(project=PROJECT_ID)
    job = client.load_table_from_json(
        rows,
        table,
        job_config=bigquery.LoadJobConfig(
            schema=SCHEMA,
            write_disposition="WRITE_APPEND",
        ),
    )
    job.result()
    print(f"Loaded {len(rows)} rows into {table}")


def run(start, end):
    rows = fetch_all(start, end)
    load_rows(rows)


if __name__ == "__main__":
    # usage: python -m load.load_to_bq 2025-01-01 2025-12-31
    run(sys.argv[1], sys.argv[2])