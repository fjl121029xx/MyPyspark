#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import json
import requests

read_dohkosessionConf = {
    "jars": ["hdfs://cluster/yqs/tools/engine-0.0.1-SNAPSHOT.jar"],
    "pyFiles": [],
    "files": [],
    "archives": [],
    "kind": 'spark',
    "driverMemory": '2g',
    "driverCores": 1,
    "executorMemory": '2g',
    "executorCores": 2,
    "numExecutors": 1,
    "queue": 'default',
    "heartbeatTimeoutInSecond": 86400,
    "proxyUser": None,
    'conf': {
        "spark.default.parallelism": 12,
        "spark.rdd.compress": True,
        "spark.io.compression.codec": "snappy"
    }
}

read_productsession = {"jars": ["hdfs://cluster/yqs/tools/engine-0.0.1-SNAPSHOT.jar"], "pyFiles": [], "files": [],
                       "archives": [], "kind": "spark",
                       "driverMemory": '11g',
                       "driverCores": 1,
                       "executorMemory": '11g',
                       "executorCores": 6,
                       "numExecutors": 17,
                       "queue": "default",
                       "heartbeatTimeoutInSecond": 86400,
                       "proxyUser": None,
                       "conf": {
                           "spark.default.parallelism": 200,
                           "spark.scheduler.mode": "FAIR",
                           "spark.serializer": "org.apache.spark.serializer.KryoSerializer",
                           "spark.rdd.compress": True, "spark.io.compression.codec": "snappy",
                           "spark.sql.files.maxPartitionBytes": 536870912,
                           "spark.sql.broadcastTimeout": 60,
                           "spark.sql.orc.enabled": True,
                           "spark.sql.orc.impl": "native"}}

write_productsession = {
    "jars": ["hdfs://cluster/yqs/tools/engine-0.0.1-SNAPSHOT.jar"],
    "pyFiles": [],
    "files": [],
    "archives": [],
    "kind": 'spark',
    "driverMemory": '10g',
    "driverCores": 1,
    "executorMemory": '10g',
    "executorCores": 3,
    "numExecutors": 3,
    "queue": 'default',
    "heartbeatTimeoutInSecond": 86400,
    "proxyUser": None,
    'conf': {
        "spark.default.parallelism": 400,
        "spark.scheduler.mode": "FAIR",
        "spark.serializer": "org.apache.spark.serializer.KryoSerializer",
        "spark.rdd.compress": True,
        "spark.io.compression.codec": "snappy",
        # "spark.sql.inMemoryColumnarStorage.batchSize": 300000,
        "spark.sql.files.maxPartitionBytes": 536870912,
        "spark.sql.broadcastTimeout": 60,
        "spark.sql.orc.enabled": True,
        "spark.sql.orc.impl": "native",
        "spark.sql.orc.enableVectorizedReader": True,
        "spark.sql.hive.convertMetastoreOrc": True,
        "spark.sql.orc.filterPushdown": True,
        "spark.sql.orc.char.enabled": True,
        # "spark.submit.deployMode": "cluster",
        "spark.driver.extraJavaOptions": "-Dhdp.version=3.0.1.0-187",
        "spark.executor.extraJavaOptions": "-Dhdp.version=3.0.1.0-187"
    }
}

sessionConf = {}
type = 0
if type == 0:
    sessionConf = read_dohkosessionConf
    sessionConf["name"] = 'YQS_Read_App'
else:   
    sessionConf = write_productsession
    # sessionConf["name"] = 'CESHIAO'
    sessionConf["name"] = 'YQS_Write_App'

headers = {'X-Requested-By': 'livy'}
try:
    # print(sessionConf)
    response = requests.post('http://172.20.44.6:8999/sessions/', data=json.dumps(sessionConf), headers=headers)
    # response = requests.post('http://172.26.25.148:8999/sessions/', data=json.dumps(sessionConf), headers=headers)
    # response = requests.post('http://192.168.101.39:8999/sessions/', data=json.dumps(sessionConf), headers=headers)
    print('createSession %s' % (response.text))
except Exception as e:
    print('createSession error: %s' % (repr(e)))
