from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("PysparkCount").getOrCreate()
print(spark)

sc = spark.sparkContext
print(sc)

rdd = sc.parallelize(range(10000))
cnt = rdd.count()
print(cnt)