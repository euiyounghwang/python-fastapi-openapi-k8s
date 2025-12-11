# my_spark_job.py
import argparse
from pyspark.sql import SparkSession
import logging
import sys

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def create_spark_session_app_name(app_name="My Spark Job"):
    """Initializes and returns a Spark session."""
    spark = SparkSession.builder.appName(app_name).getOrCreate()
    return spark


def create_spark_session():
    """Initializes and returns a Spark session."""
    spark = SparkSession.builder.getOrCreate()
    return spark


def main():
    # 1. Create the parser
    parser = argparse.ArgumentParser(description="A PySpark job with command-line arguments.")
    
    # 2. Add arguments
    parser.add_argument('--input_path', type=str, required=True, help="The input data path (e.g., S3 or HDFS location).")
    parser.add_argument('--output_path', type=str, required=True, help="The output data path.")
    parser.add_argument('--process_date', type=str, default="2025-01-01", help="The processing date in YYYY-MM-DD format.")
    
    # 3. Parse the arguments from sys.argv
    args = parser.parse_args()
    
    # Access arguments using dot notation
    input_path = args.input_path
    output_path = args.output_path
    process_date = args.process_date
    
    # Use Spark
    spark = create_spark_session()
    logging.info(f"Starting job for date: {process_date}, reading from {input_path} and writing to {output_path}")

    # Your Spark logic goes here, e.g.,
    # df = spark.read.parquet(input_path)
    # ...
    
    spark.stop()

if __name__ == "__main__":
    main()