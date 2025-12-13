from pyspark.sql import SparkSession

def create_spark_session():
    """Initializes and returns a Spark session."""
    spark = SparkSession.builder \
        .getOrCreate()
    return spark


def work():
    ''' You need to include the elasticsearch-hadoop connector JAR in your Spark environment when running spark-submit or pyspark '''
    ''' 
    # Example command using spark-submit with the connector JAR
    spark-submit --jars /path/to/elasticsearch-hadoop-*.jar your_spark_script.py

    Download ES-Hadoop: https://www.elastic.co/downloads/past-releases?product=es-hadoop
    '''
    # Initialize Spark Session (ensure elasticsearch-spark connector is in classpath)
    spark = create_spark_session()

    # Define your Elasticsearch bool query as a JSON string
    # This query finds documents where 'status' is 'publish' AND 'authors' is '104'
    # es_query = """
    # {
    #     "query": {
    #         "bool": {
    #         "filter": [
    #             {
    #             "match": {
    #                 "status": "publish"
    #             }
    #             },
    #             {
    #             "match": {
    #                 "authors": "104"
    #             }
    #             }
    #         ]
    #         }
    #     }
    # }
    # """
    es_query = """
    {
        "query" : {
            "match_all" : {}
        },
        "size": 1
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
        "es.resource": "test",
        "es.query" : es_query
    }

    # Read data from Elasticsearch
    df = spark.read.format("org.elasticsearch.spark.sql").options(**config).load()

    # Show the resulting DataFrame
    # df.show()
    df.printSchema()
    print(df.count())



if __name__ == '__main__':
    work()