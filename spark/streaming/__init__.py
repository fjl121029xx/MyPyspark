#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2020/7/9 10:10
__author__ = 'the king of north'

import time
import os
import sys
# pip install pyspark -i  https://pypi.tuna.tsinghua.edu.cn/simple/
# Path
os.environ['SPARK_HOME'] = "E:\env\spark-3.0.0-bin-hadoop3.2"

# Apperd spark to Python Path
sys.path.append("E:\env\spark-3.0.0-bin-hadoop3.2\python")
sys.path.append("E:\env\spark-3.0.0-bin-hadoop3.2\python\lib\py4j-0.10.9-src.zip")

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

try:


    from operator import add

    sc = SparkContext(master="local[1]", appName="PythonSparkStreamingRokidDtSnCount")
    ssc = StreamingContext(sc, 2)
    zkQuorum = 'localhost:2181'
    topic = {'rokid': 1}
    groupid = "test-consumer-group"
    lines = KafkaUtils.createStream(ssc, zkQuorum, groupid, topic)
    lines1 = lines.flatMap(lambda x: x.split("\n"))
    valuestr = lines1.map(lambda x: x.value.decode())
    valuedict = valuestr.map(lambda x: eval(x))
    message = valuedict.map(lambda x: x["message"])
    rdd2 = message.map(lambda x: (
        time.strftime("%Y-%m-%d", time.localtime(float(x.split("\u0001")[0].split("\u0002")[1]) / 1000)) + "|" +
        x.split("\u0001")[1].split("\u0002")[1], 1)).map(lambda x: (x[0], x[1]))
    rdd3 = rdd2.reduceByKey(add)
    rdd3.saveAsTextFiles("/tmp/wordcount")
    rdd3.pprint()
    ssc.start()
    ssc.awaitTermination()
except ImportError as e:
    print("Can not import Spark Modules", e)
