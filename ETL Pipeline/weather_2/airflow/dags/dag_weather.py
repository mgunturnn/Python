from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
from google.cloud import bigquery
from datetime import datetime
import requests

def extract_transform_weather_data(ti):
    # Fetch weather data from Open-Meteo API for Bandung, Indonesia
    url = "https://api.open-meteo.com/v1/forecast?latitude=-6.9147&longitude=107.6098&daily=temperature_2m_max,temperature_2m_min&timezone=Asia%2FJakarta"
    response = requests.get(url)
    data = response.json()

    # Fetch 'daily' data from the API response
    daily_data = data['daily']

    # Extract the data
    dates = daily_data['time']
    max_temps = daily_data['temperature_2m_max']
    min_temps = daily_data['temperature_2m_min']

    weather_data = []

    # Combine the extracted data into a list of dictionaries
    for date, max_t, min_t in zip(dates, max_temps, min_temps):
        weather_data.append({
            'date': date,
            'max_temp': max_t,
            'min_temp': min_t
        })

    ti.xcom_push(key = 'weather', value = weather_data)

def load_weather_data(ti):
    weather_data = ti.xcom_pull(key = 'weather', task_ids = 'extract_transform_weather_data')

    bigquery_hook = BigQueryHook(gcp_conn_id = 'gcp_conn')
    client = bigquery_hook.get_client()

    table_id = 'weather-pipeline-506703.weather_dataset.weather_daily_report'

    job_config = bigquery.LoadJobConfig(
        write_disposition = bigquery.WriteDisposition.WRITE_APPEND,
    )

    load_job = client.load_table_from_json(
        weather_data,
        table_id,
        job_config = job_config
    )

    load_job.result()

    print(f"Sukses! {load_job.output_rows} baris data berhasil mendarat di BigQuery.")

    # table_id = 'weather-pipeline-506703.weather_dataset.weather_daily_report'

    # errors = client.insert_rows_json(table_id, weather_data)

    # if errors == []:
    #     print("Data loaded successfully into BigQuery.")
    # else:
    #     print(f"Errors occurred while loading data into BigQuery:{errors}")


    # insert_query = """
    #     INSERT INTO weather (date, max_temp, min_temp) VALUES
    #     (%s, %s, %s)
    # """

    # for weather in weather_data:
    #     params_weather = (weather['date'], weather['max_temp'], weather['min_temp'])
    #     bigquery_hook.run(insert_query, parameters = params_weather)

default_args = {
    'owner': 'guntur',
    'start_date': datetime(2026, 6, 1),
    'retries': 0
}

dag = DAG(
    dag_id = 'weather_data_pipeline_v5',
    start_date = datetime(2026, 8, 25),
    default_args = default_args,
    schedule_interval = '@daily',
    catchup = False
)

task1 = PythonOperator(
    task_id = 'extract_transform_weather_data',
    python_callable = extract_transform_weather_data,
    dag = dag
)

# task2 = PostgresOperator(
#     task_id = 'create_table_weather',
#     postgres_conn_id = 'weather_conn',
#     sql = './database/create_table.sql',
#     dag = dag
# )

task3 = PythonOperator(
    task_id = 'load_weather_data',
    python_callable = load_weather_data,
    dag = dag
)

task1 >> task3