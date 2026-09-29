from pyspark.sql import SparkSession
import os

# Create Spark session
spark = SparkSession.builder \
    .appName("MediaPulse Bronze Layer") \
    .master("local[*]") \
    .getOrCreate()

# Project paths
RAW_PATH = "/opt/airflow/mediapulse/data/raw"
BRONZE_PATH = "/opt/airflow/mediapulse/data/bronze"

# Source files
files = [
    "users.csv",
    "content.csv",
    "views.csv",
    "ads.csv",
    "subscriptions.csv",
    "support.csv"
]

print("====================================")
print("   MEDIAPULSE BRONZE INGESTION")
print("====================================")

for file in files:

    input_path = os.path.join(RAW_PATH, file)

    print(f"\nProcessing: {file}")

    df = spark.read \
        .option("header", True) \
        .option("inferSchema", True) \
        .csv(input_path)

    output_name = file.replace(".csv", "")
    output_path = os.path.join(BRONZE_PATH, output_name)

    df.write \
        .mode("overwrite") \
        .parquet(output_path)

    print(f"Rows: {df.count()}")
    print(f"Bronze location: {output_path}")

print("\nBronze ingestion completed successfully!")

spark.stop()