# SSH

- Using gcloud CLI

```
gcloud compute ssh --zone "asia-northeast1-a" "instance-20251210-071922" --project "bi-dev-429601"
```

- Using openSSH

```
ssh -i ~/.ssh/id_rsa ocean@34.146.63.73
```

# Docker and Docker Compose

```
# Add Docker's official GPG key:
sudo apt update
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Signed-By: /etc/apt/keyrings/docker.asc
EOF

sudo apt update
```

```
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

sudo systemctl status docker

sudo docker run hello-world
```

```
sudo apt-get update
sudo apt-get install docker-compose-plugin

docker compose version
```

# Kafka

https://hub.docker.com/r/apache/kafka

- Set up Kafka through docker compose

```
touch docker-compose.yml

sudo usermod -aG docker $USER
newgrp docker
groups

docker compose up -d

sudo ss -tulnp | grep 9092
curl -v telnet://localhost:9092
```

- Set up Kafka client CLI

```
wget https://dlcdn.apache.org/kafka/4.1.1/kafka_2.13-4.1.1.tgz
tar -xzf kafka_2.13-4.1.1.tgz
cd kafka_2.13-4.1.1

sudo apt install -y openjdk-17-jre
java -version

kafka_2.13-4.1.1/bin/kafka-topics.sh --list --bootstrap-server localhost:9092

kafka_2.13-4.1.1/bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic test-topic

kafka_2.13-4.1.1/bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic events
```

# MinIO

- Set up docker compose

https://docs.min.io/enterprise/aistor-object-store/installation/container/install/

```
mkdir -p $HOME/minio/data
vim $HOME/minio/config

docker compose up -d
docker logs minio
netstat -an | grep "LISTEN "
```

- Port forwarding

```
gcloud compute ssh --zone "asia-northeast1-a" "instance-20251210-071922" --project "bi-dev-429601" -- -L 9001:localhost:9001 -L 8889:localhost:8888

http://localhost:9001 # minioadmin:minioadmin
```

- MinIO CLI

```
curl --progress-bar -L https://dl.min.io/aistor/mc/release/linux-arm64/mc -o mc
chmod +x ./mc

sudo mv ./mc /usr/local/bin
mc --version

mc alias set myaistor http://localhost:9000 minioadmin minioadmin

mc mb myaistor/data
mc cp ~/somefile.txt myaistor/data
```

# Redis

```
sudo apt install redis-tools

redis-cli
```

# Spark + Iceberg

```
docker exec -it spark-iceberg spark-sql

CREATE TABLE demo.nyc.taxis
(
  vendor_id bigint,
  trip_id bigint,
  trip_distance float,
  fare_amount double,
  store_and_fwd_flag string
)
PARTITIONED BY (vendor_id);
INSERT INTO demo.nyc.taxis

VALUES (1, 1000371, 1.8, 15.32, 'N'), (2, 1000372, 2.5, 22.15, 'N'), (2, 1000373, 0.9, 9.01, 'N'), (1, 1000374, 8.4, 42.13, 'Y');

SELECT * FROM demo.nyc.taxis;
```

- Selecting catalogs and namespaces

```
SHOW CATALOGS;

USE ...;

SHOW NAMESPACES;
```

# Spark

```
docker cp scripts/kafka_to_iceberg.py spark-iceberg:/home/iceberg/notebooks/kafka_to_iceberg.py

docker exec -it spark-iceberg /opt/spark/bin/spark-submit --master local[2] --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.5 /home/iceberg/notebooks/kafka_to_iceberg.py

docker exec -it spark-iceberg /opt/spark/bin/spark-submit --master local[2] /home/iceberg/notebooks/notebooks/airflow_spark_job.py
```

# Kafka JMX Exporter and Prometheus

- View Kafka JMX metrics

```
curl http://localhost:7071/metrics
```

# Airflow

- If using Airflow on Docker

```
docker compose -f docker-compose-airflow.yaml run --rm airflow-init
docker compose -f docker-compose.yml -f docker-compose-airflow.yaml down
docker compose -f docker-compose.yml -f docker-compose-airflow.yaml up -d

gcloud compute ssh --zone "asia-northeast1-a" "instance-20251210-071922" --project "bi-dev-429601" -- -L 9001:localhost:9001 -L 8889:localhost:8888 -L 9090:localhost:9090 -L 3000:localhost:3000 -L 8082:localhost:8082
```

- If using Airflow PyPi

```
airflow standalone
airflow dags list
airflow dags test spark_dag
```