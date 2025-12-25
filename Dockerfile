FROM apache/airflow:3.1.5

USER root

# Install Docker provider (and optional docker CLI tools)
RUN pip install --no-cache-dir \
    apache-airflow-providers-docker

# Optional but recommended: docker CLI for debugging
RUN apt-get update && \
    apt-get install -y docker.io && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER airflow