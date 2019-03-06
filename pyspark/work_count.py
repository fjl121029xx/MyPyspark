#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'wsc'

import os
import sys

# Path
os.environ['SPARK_HOME'] = "D:\work\spark"

# Apperd pyspark to Python Path
sys.path.append("D:\work\spark\python")
sys.path.append("D:\work\spark\python\lib\py4j-0.10.7-src.zip")

try:
    from pyspark import SparkContext
    from pyspark import SparkConf

    print("Successfully imported Spark Modules")

    if __name__ == '__main__':

        # if len(sys.argv) != 3:
        #     print("Usaee:python input_name output_name")
        #     exit(1)

        inputFile = "hello_pyspark.py"
        outputFile = "1.txt"

        sc = SparkContext()

        text_file = sc.textFile(inputFile)
        counts = text_file.flatMap(lambda line: line.split(' ')).map(lambda word: (word, 1)).reduceByKey(
            lambda a, b: a + b)
        counts.saveAsTextFile(outputFile)

except ImportError as e:
    print("Can not import Spark Modules", e)

##