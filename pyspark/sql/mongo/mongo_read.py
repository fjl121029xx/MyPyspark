#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'wsc'

import os
import sys

# Path
os.environ['SPARK_HOME'] = "H:\workspaces\spark"

# Apperd pyspark to Python Path
sys.path.append("H:\workspaces\spark\python")
sys.path.append("H:\workspaces\spark\python\lib\py4j-0.10.7-src.zip")

# mongodb://username:password@ip:port
# ip:port或者域名
uri = "mongodb://huatu_ztk:wEXqgk2Q6LW8UzSjvZrs@192.168.100.153:27017,192.168.100.154:27017,192.168.100.155:27017/"
# database name
database = "huatu_ztk."
# collection name
collection = "ztk_question_new"

try:
    from pyspark.sql import SparkSession

    my_spark = SparkSession \
        .builder \
        .appName("mongo read") \
        .config("spark.mongodb.input.uri", uri + database + collection) \
        .getOrCreate()

    df = my_spark.read.format("com.mongodb.spark.sql.DefaultSource").load()
    df.printSchema()

except ImportError as e:
    print("Can not import Spark Modules", e)
