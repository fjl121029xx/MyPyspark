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
startJVM(jvmPath, "-ea", jvm_cp)
# Path
os.environ['SPARK_HOME'] = "H:\workspaces\spark"

# Apperd pyspark to Python Path
sys.path.append("H:\workspaces\spark\python")
sys.path.append("H:\workspaces\spark\python\lib\py4j-0.10.7-src.zip")
SPARK_HOME = os.environ['SPARK_HOME']
sys.path.insert(0, os.path.join(SPARK_HOME, "python"))
sys.path.insert(0, os.path.join(SPARK_HOME, "python", "lib"))
sys.path.insert(0, os.path.join(SPARK_HOME, "python", "lib", "pyspark.zip"))
sys.path.insert(0, os.path.join(SPARK_HOME, "python", "lib", "py4j-0.10.7-src.zip"))

try:

    from pyspark.sql import SparkSession
    from pyspark.sql import Row

    if __name__ == '__main__':
        my_spark = SparkSession \
            .builder \
            .appName("write hbase") \
            .getOrCreate()

        sc = my_spark.sparkContext

        host = '192.168.100.68:2181,192.168.100.70:2181,192.168.100.72:2181'
        table = 'student'

        # keyConv = "org.apache.spark.examples.pythonconverters.StringToImmutableBytesWritableConverter"
        # valueConv = "org.apache.spark.examples.pythonconverters.StringListToPutConverter"

        keyConv = "org.apache.spark.api.python.JavaToWritableConverter"
        valueConv = "org.apache.spark.api.python.JavaToWritableConverter"

        conf = {"hbase.zookeeper.quorum": host, "hbase.mapred.outputtable": table,
                "hbase.zookeeper.property.clientPort": "2181",
                "mapreduce.outputformat.class": "org.apache.hadoop.hbase.mapreduce.TableOutputFormat",
                "mapreduce.job.output.key.class": "org.apache.hadoop.hbase.io.ImmutableBytesWritable",
                "mapreduce.job.output.value.class": "org.apache.hadoop.io.Writable"}

        rawData = ['3-info-name-Rongcheng', '4-info-name-Guanhua']
        # (rowkey, [row key, column family, column name, value])
        sc.parallelize(rawData).map(lambda x: (x[0], x.split('-'))).saveAsNewAPIHadoopDataset(conf, keyConv, valueConv)

except ImportError as e:
    print("Can not import Spark Modules", e)
