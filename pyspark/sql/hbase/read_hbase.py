#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'wsc'

import os
import mh
import jpype
from jpype import *

jvmPath = jpype.getDefaultJVMPath()

# jars_dir = 'H:/pp/'
# jars = [os.path.join(jars_dir, 'myspark.jar'), os.path.join(jars_dir, 'spark-core_2.11-2.3.2.jar'),
#         os.path.join(jars_dir, 'spark-sql_2.11-2.3.2.jar')]
# jvm_cp = "-Djava.class.path={}".format(':'.join(jars))
# dependency = "-Djava.ext.dirs={}".format(':'.join(jars))
jvm_cp = "-Djava.class.path=H:/pp/pjava-1.0-SNAPSHOT-jar-with-dependencies.jar"
print(jvm_cp)
startJVM(jvmPath, "-ea", jvm_cp)
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

hbaseconf = {"hbase.zookeeper.quorum": "192.168.100.68,192.168.100.70,192.168.100.72",
             "hbase.mapreduce.inputtable": "student"}

keyConv = "org.apache.spark.examples.pythonconverters.ImmutableBytesWritableToStringConverter"

valueConv = "org.apache.spark.examples.pythonconverters.HBaseResultToStringConverter"

try:
    from pyspark.sql import SparkSession
    from pyspark.sql import Row

    my_spark = SparkSession \
        .builder \
        .appName("mongo read") \
        .config("spark.mongodb.input.uri", uri + database + collection) \
        .getOrCreate()

    hbase_rdd = my_spark.sparkContext.newAPIHadoopRDD( \
        "org.apache.hadoop.hbase.mapreduce.TableInputFormat", \
        "org.apache.hadoop.hbase.io.ImmutableBytesWritable", \
        "org.apache.hadoop.hbase.client.Result", \
        keyConv, valueConv, hbaseconf)
    print(hbase_rdd.count())

# question = my_spark.createDataFrame(df)
# question.show
# for i in df.take(100):
#     print(i)

except ImportError as e:
    print("Can not import Spark Modules", e)
