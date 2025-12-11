from pyspark.sql import SparkSession
from pyspark.sql.functions import col


def create_spark_session():
    """Initializes and returns a Spark session."""
    spark = SparkSession.builder \
        .getOrCreate()
    return spark


def work():
    spark = create_spark_session()

    # Create a sample DataFrame (replace with your actual data source)
    data = [{"name": "John Doe", "age": 30, "id": "1"}, 
            {"name": "Jane Doe", "age": 25, "id": "2"}]
    df = spark.createDataFrame(data)

    # Configuration options for Elasticsearch
    es_config = {
        "es.nodes": "http://<your-elasticsearch-host>", 
        "es.port": "9200", # Use 443 for HTTPS, or 9200 if configured
        "es.resource": "your_index/_doc", # Target index and type
        "es.mapping.id": "id",            # Use 'id' field as Elasticsearch doc ID
        "es.index.auto.create": "true",
        "es.batch.size.bytes": "4mb",     # Adjust bulk size for performance
        "es.batch.size.entries": "1000",
        "es.nodes.wan.only": "true"       # Use if connecting to a cloud ES instance
    }

    # Write the DataFrame to Elasticsearch
    df.write.format("org.elasticsearch.spark.sql").options(**es_config).mode("append").save()


if __name__ == '__main__':
    work()