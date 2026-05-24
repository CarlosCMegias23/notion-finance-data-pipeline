from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Añadimos la ruta de la carpeta scripts al path del sistema 
# para que Airflow pueda encontrar e importar tu función run_etl
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))
from extract_load import run_etl

default_args = {
    'owner': 'data_engineer',
    'depends_on_past': False,
    'start_date': datetime(2023, 10, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'notion_to_snowflake_finance',
    default_args=default_args,
    description='Pipeline diario: Extrae finanzas personales de Notion y las carga en Snowflake',
    schedule_interval='@daily', # Se ejecutará todos los días
    catchup=False,
    tags=['finance', 'etl', 'notion', 'snowflake'],
) as dag:

    # Tarea principal que ejecuta el proceso ETL en Python
    run_etl_task = PythonOperator(
        task_id='extract_and_load_task',
        python_callable=run_etl
    )

    # Si tuvieras más tareas (ej. transformaciones con dbt, alertas), se enlazarían aquí
    run_etl_task