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

try:

    from pyspark.sql import SparkSession
    from pyspark.sql import Row

    my_spark = SparkSession \
        .builder \
        .appName("mongo read") \
        .config("spark.mongodb.input.uri", uri + database + collection) \
        .getOrCreate()
    my_spark.udf.registerJavaUDAF("summation", 'com.Test')

    df = my_spark.read.format("com.mongodb.spark.sql.DefaultSource").load()
    df.registerTempTable("question")

    pq = my_spark.sql("""
        select _id,points from question
    """).rdd.filter(mh.myfile).mapPartitions(mh.mypartiton).toDF()

    pq.registerTempTable("abc")
    my_spark.sql("select pid,summation(qid) from abc group by pid").show()


    # question = my_spark.createDataFrame(df)
    # question.show
    # for i in df.take(100):
    #     print(i)

except ImportError as e:
    print("Can not import Spark Modules", e)
