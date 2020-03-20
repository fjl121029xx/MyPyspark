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
    import java.text.SimpleDateFormat
    import java.util
    import java.util.Calendar
    import java.util.regex.Pattern
    
    import org.apache.spark.sql.Row
    import org.apache.spark.sql.expressions.{MutableAggregationBuffer, UserDefinedAggregateFunction}
    import org.apache.spark.sql.types.{DataType, DataTypes, StructType} 
    
    import java.sql.Timestamp
    
    import org.apache.spark.sql.api.java.UDF2
    
     spark.udf.register("report_date_format", new UDF2[String, String, String]() {
        //  yyyy-MM-dd HH:mm:ss
      @throws[Exception]
 override def call(reportdate: String, format: String): String = {

    val ca = Calendar.getInstance()

    if (reportdate.length == 19) {
      ca.set(reportdate.substring(0, 4).toInt,
        reportdate.substring(5, 7).toInt - 1,
        reportdate.substring(8, 10).toInt,
        reportdate.substring(11, 13).toInt,
        reportdate.substring(14, 16).toInt,
        reportdate.substring(17, 19).toInt
      )
    } else if (reportdate.length == 10) {
      ca.set(reportdate.substring(0, 4).toInt,
        reportdate.substring(5, 7).toInt - 1,
        reportdate.substring(8, 10).toInt
      )
    } else {
      ca.set(reportdate.substring(0, 4).toInt,
        reportdate.substring(4, 6).toInt - 1,
        reportdate.substring(6, 8).toInt
      )
    }

    format match {
      case "y" => ca.get(Calendar.YEAR).toString + "年"
      case "yq" =>
        val m = ca.get(Calendar.MONTH)
        if (m >= 0 && m < 3) {
          ca.get(Calendar.YEAR).toString + "年1季度"
        } else if (m >= 3 && m < 6) {
          ca.get(Calendar.YEAR).toString + "年2季度"
        } else if (m >= 6 && m < 9) {
          ca.get(Calendar.YEAR).toString + "年3季度"
        } else {
          ca.get(Calendar.YEAR).toString + "年4季度"
        }
      case "ym" => {
        var mint = (ca.get(Calendar.MONTH) + 1).toString
        if (mint.length < 2) {
          mint = "0" + mint
        }

        ca.get(Calendar.YEAR).toString + "年" + mint + "月"
      }
      case "yw" => ca.get(Calendar.YEAR).toString + "年" + (ca.get(Calendar.WEEK_OF_YEAR)) + "周"
      case "ymd" =>
        var m = (ca.get(Calendar.MONTH) + 1).toString
        var d = ca.get(Calendar.DAY_OF_MONTH).toString
        if (m.length < 2) {
          m = "0" + m
        }
        if (d.length < 2) {
          d = "0" + d
        }
        ca.get(Calendar.YEAR) + "年" + m + "月" + d + "日"
      case "ymdh" =>
        var m = (ca.get(Calendar.MONTH) + 1).toString
        var d = ca.get(Calendar.DAY_OF_MONTH).toString
        if (m.length < 2) {
          m = "0" + m
        }
        if (d.length < 2) {
          d = "0" + d
        }
        ca.get(Calendar.YEAR) + "年" + m + "月" + d + "日" + ca.get(Calendar.HOUR_OF_DAY) + "时"
      case _ =>
        throw new RuntimeException("nonexistent dimen_mode. [y,yq,ym,yw,ymd,ymdh]]")

    }

  }
    }, DataTypes.StringType)
    
    
    """
    # ,
    # 'kind': "sql"
}


# 172.20.44.6
# bi-olap1.sm02

def report_date_format(sid, url):
    response = requests.post(url + str(sid) + '/statements', data=json.dumps(data),
                             headers=headers)
    # reg()
    id = response.json()['id']
    time.sleep(10)
    response = request.urlopen(url + '%d/statements/%d' % (sid, id))
    statements = json.loads(response.read())
    stmt = statements['state']
    if 'available' == stmt:
        print(statements)
