from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from utils.tags import Tag

def print_hello():
    return "Hello from Airflow!"

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="hello_world",
    default_args=default_args,
    description="A simple hello world DAG",
    schedule_interval=None,  # Only run manually
    start_date=datetime(2025, 4, 19),
    catchup=False,
    tags=[Tag.ImpactTier.tier_3],
) as dag:

    python_task = PythonOperator(
        task_id="python_hello",
        python_callable=print_hello,
    )

    bash_task = BashOperator(
        task_id="bash_hello",
        bash_command="echo 'Hello from Bash!'" 
    )

    python_task >> bash_task
