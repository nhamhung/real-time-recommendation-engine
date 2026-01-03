from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="spark_dag",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    run_spark = BashOperator(
        task_id="run_spark_job",
        bash_command="""
        docker exec spark-iceberg \
          /opt/spark/bin/spark-submit \
          --master local[*] \
          /home/iceberg/notebooks/notebooks/spark-batch-job.py
        """,
    )

    run_spark