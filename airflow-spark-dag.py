from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime
from docker.types import Mount

with DAG(
    dag_id="spark_docker_iceberg_test",
    start_date=datetime(2024, 1, 1),
    schedule=None,          # ✅ Airflow 3.x replacement
    catchup=False,
    tags=["spark", "docker", "iceberg"],
) as dag:

    spark_job = DockerOperator(
        task_id="run_spark_test",
        image="tabulario/spark-iceberg:latest",
        auto_remove="never",
        docker_url="unix://var/run/docker.sock",
        network_mode="project_iceberg_net",
        command=[
            "spark-submit",
            "--master",
            "local[*]",
            "/opt/spark/examples/src/main/python/pi.py",
            "10"
        ],
        # mount_tmp_dir=False,
        # mounts=[
        #     Mount(
        #         source="/home/nhamquochung/project/notebooks",   # HOST
        #         target="/opt/spark/jobs",     # CONTAINER
        #         type="bind",
        #         read_only=True
        #     )
        # ],
        # environment={
        #     "SPARK_LOCAL_IP": "127.0.0.1",
        # },
    )

    spark_job