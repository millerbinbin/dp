__author__ = 'hubin6'
from pyspark.sql import SparkSession
import os, sys
from datetime import timedelta,date

if __name__=="__main__":
    print os.environ['PYTHONPATH']
    sys.path.append("{0}/python/pyspark".format(os.environ['SPARK_HOME']))
    spark = SparkSession.builder.master("local[2]").appName("cf-python").enableHiveSupport().getOrCreate()
    spark.sparkContext.setLogLevel('WARN')
    table_name = "dp.shops"
    #spark.sql("create database if not exists dp")
    createSql = "create table if not exists {0}(\n" \
                "  shop_name string,\n" \
                "  avg_price int,\n" \
                "  cmmt_num int,\n" \
                "  taste_score double,\n" \
                "  env_score double,\n" \
                "  ser_score double,\n" \
                "  addr string,\n" \
                "  link string)\n" \
                "ROW FORMAT DELIMITED FIELDS TERMINATED BY ','\n"\
                "STORED AS TEXTFILE".format(table_name)
    #spark.sql(createSql)
