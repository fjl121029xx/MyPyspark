#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'wsc'

import os
import sys

# Path
os.environ['SPARK_HOME'] = "H:\workspaces\spark"

# Apperd spark to Python Path
sys.path.append("H:\workspaces\spark\python")
sys.path.append("H:\workspaces\spark\python\lib\py4j-0.10.7-src.zip")

try:
    from spark import SparkContext
    from spark import SparkConf

    print("Successfully imported Spark Modules")
except ImportError as e:
    print("Can not import Spark Modules", e)
sys.exit(1)
