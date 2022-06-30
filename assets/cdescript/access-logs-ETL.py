from pyspark.sql import SparkSession
from pyspark.sql.functions import split, regexp_extract, regexp_replace, col
import sys
import time

spark = SparkSession \
    .builder \
    .appName("Pyspark Tokenize") \
    .getOrCreate()

input_path ='hdfs:///tmp/access-logs.txt'
base_df=spark.read.text(input_path)

split_df = base_df.select(regexp_extract('value', r'([^ ]*)', 1).alias('ip'),
                          regexp_extract('value', r'(\d\d\/\w{3}\/\d{4}:\d{2}:\d{2}:\d{2} -\d{4})', 1).alias('date'),
                          regexp_extract('value', r'^(?:[^ ]*\ ){6}([^ ]*)', 1).alias('url'),
                          regexp_extract('value', r'(?<=product\/).*?(?=\s|\/)', 0).alias('productstring')
                         )

filtered_products_df = split_df.filter("productstring != ''")
cleansed_products_df=filtered_products_df.select(regexp_replace("productstring", "%20", " ").alias('product'), "ip", "date", "url")

print(f"Creating retail Database \n")
spark.sql("CREATE DATABASE IF NOT EXISTS retail")

print(f"Inserting Data into retail.tokenized_access_logs table \n")
cleansed_products_df.\
  write.\
  mode("overwrite").\
  saveAsTable("retail"+'.'+"tokenized_access_logs", format="parquet")

print(f"Count number of records inserted \n")
spark.sql("Select count(*) as RecordCount from retail.tokenized_access_logs").show()

print(f"Retrieve 15 records for validation \n")
spark.sql("Select * from retail.tokenized_access_logs limit 15").show()
