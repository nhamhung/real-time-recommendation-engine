from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("PrintSimpleDataFrame")
    .getOrCreate()
)

data = [
    (1, "Alice"),
    (2, "Bob"),
    (3, "Charlie"),
]

df = spark.createDataFrame(data, ["id", "name"])

df.show(truncate=False)

spark.stop()