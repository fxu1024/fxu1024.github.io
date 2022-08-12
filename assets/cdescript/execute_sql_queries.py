"""
A simple Spark Application Which Executes the List of Queries Sequentially from the Arguments

DISCLAIMER: It is the user’s responsibility to pass the VALID SQL statement to avoid failures.
and It is meant for DEX ease of use.

Run with:
  ./bin/spark-submit $PWD/resources/python/execute_sql_queries.py "query_string1" ["query_string2", ..]
"""
from __future__ import print_function

import sys
from time import sleep
from pyspark.sql import SparkSession

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: execute_sql_queries.py <"query_string1"> ["query_string2", ..]', file=sys.stderr)
        sys.exit(-1)

    spark = SparkSession.builder.getOrCreate()

    for cur_query in sys.argv[1:]:
        print('Running >> spark.sql("{query}")'.format(query=cur_query))
        spark.sql(cur_query).show(truncate=False)

    print("All SQL Queries are Executed Successfully!", file=sys.stdout)
    print("Sleeping for 5sec before Stopping Session")
    sleep(5)
    spark.stop()
