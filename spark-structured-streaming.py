from doctest import DocFileSuite
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, to_timestamp
from pyspark.sql.types import StructType, StringType
from pyspark import SparkContext
from pyspark import SparkConf

conf = SparkConf()

conf.set('spark.hadoop.fs.s3a.endpoint', "http://minio:9000")
conf.set('spark.hadoop.fs.s3a.access.key', "admin")
conf.set('spark.hadoop.fs.s3a.secret.key', "password")
conf.set('spark.hadoop.fs.s3a.impl', 'org.apache.hadoop.fs.s3a.S3AFileSystem')
conf.set('spark.hadoop.fs.s3a.path.style.access', 'true')

spark = SparkSession.builder \
    .config(conf=conf) \
    .getOrCreate()

print(f'spark version: {spark.version}')
print(spark._jsc.hadoopConfiguration().get('fs.s3a.endpoint'))

schema = (
    StructType()
    .add("event_time", StringType())
    .add("user_id", StringType())
    .add("item_id", StringType())
    .add("action", StringType())
)

spark.sql("""
DROP TABLE IF EXISTS demo.nyc.events;
""")

spark.sql("""
CREATE TABLE IF NOT EXISTS demo.nyc.events (
  event_time TIMESTAMP,
  user_id STRING,
  item_id STRING,
  action STRING
) USING iceberg;
"""
)

kafka_df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "events") \
    .option("startingOffsets", "latest") \
    .load()

parsed_df = (
    kafka_df
    .select(from_json(col("value").cast("string"), schema).alias("data"))
    .select("data.*")
    .withColumn("event_time", to_timestamp("event_time"))
)

query = (
    parsed_df
    .writeStream
    .format("iceberg")
    .outputMode("append")
    .option("checkpointLocation", "s3a://warehouse/wh/checkpoints/events")
    .toTable("nyc.events")
)

query.awaitTermination()