from pyspark.sql import SparkSession

def create_spark_session():
    """Initializes and returns a Spark session."""
    spark = SparkSession.builder \
        .getOrCreate()
    return spark


def work():
    # Initialize Spark Session (ensure elasticsearch-spark connector is in classpath)
    spark = create_spark_session()

    # Define your Elasticsearch bool query as a JSON string
    # This query finds documents where 'status' is 'publish' AND 'authors' is '104'
    es_query = """
    {
        "query": {
            "bool": {
            "filter": [
                {
                "match": {
                    "status": "publish"
                }
                },
                {
                "match": {
                    "authors": "104"
                }
                }
            ]
            }
        }
    }
    """

    # Read data from Elasticsearch into a Spark DataFrame using the es.query option
    """
    df = spark.read \
        .format("org.elasticsearch.spark.sql") \
        .option("es.nodes", "your_es_host") \
        .option("es.port", "9200") \
        .option("es.net.http.auth.user", "your_user") \
        .option("es.net.http.auth.pass", "your_password") \
        .option("es.query", es_query) \
        .load("your_index_name") # Specify the index to load from
    """
    # Define connection properties
    config = {
        # "es.nodes": "https://<your-elasticsearch-host>", 
        # "es.port": "443", # Use 443 for HTTPS, or 9200 if configured
        "es.nodes": "http://<your-elasticsearch-host>", 
        "es.port": "9200", # Use 443 for HTTPS, or 9200 if configured
        # "es.net.ssl": "true",
        # "es.net.http.auth.user": "your_username",
        # "es.net.http.auth.pass": "your_password",
        # "es.nodes.wan.only": "true", # Use if needed for cloud/remote clusters
        "es.resource": "index_name/_doc",
        "es.query" : es_query
    }

    # Read data from Elasticsearch
    df = spark.read.format("org.elasticsearch.spark.sql").options(**config).load()

    # Show the resulting DataFrame
    df.show()


if __name__ == '__main__':
    work()