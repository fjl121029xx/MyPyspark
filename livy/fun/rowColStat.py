#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import json
import requests
from urllib import request
import time

headers = {
    'Content-Type': 'application/json',
    'X-Requested-By': 'admin'
}
data = {
    'code': """

    import java.util
    import java.util.Calendar
    import java.util.regex.Pattern
    
    import org.apache.spark.sql.Row
    import org.apache.spark.sql.expressions.{MutableAggregationBuffer, UserDefinedAggregateFunction}
    import org.apache.spark.sql.types.{DataType, DataTypes, StructType}
    
    import scala.collection.mutable
    spark.udf.register("row_col_stat", new UserDefinedAggregateFunction() {
   
  
  
  
  
    }
    )
    """
    # ,
    # 'kind': "sql"
}


def row_col_stat(sid, url):
    response = requests.post(url + str(sid) + '/statements', data=json.dumps(data),
                             headers=headers)
    time.sleep(10)
    id = response.json()['id']
    response = request.urlopen(url + '%d/statements/%d' % (sid, id))
    statements = json.loads(response.read())
    stmt = statements['state']
    if 'available' == stmt:
        print(statements)


url = "http://172.20.44.6:8999/sessions/"
# url ="http://bi-olap1.sm02:8999/sessions/"
row_col_stat(78628, url)
row_col_stat(78627, url)
