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
    spark.udf.register("suma", new UserDefinedAggregateFunction() {

      override def inputSchema: StructType =
    DataTypes.createStructType(util.Arrays.asList(
      DataTypes.createStructField("dimension", DataTypes.createArrayType(DataTypes.StringType), true),
      DataTypes.createStructField("measure", DataTypes.DoubleType, true),
      DataTypes.createStructField("dimen_mode", DataTypes.StringType, true)
    ))

  override def bufferSchema: StructType = DataTypes.createStructType(util.Arrays.asList(
    DataTypes.createStructField(
      "mid_result",
      DataTypes.createMapType(DataTypes.StringType, DataTypes.DoubleType, true),
      true)
  )
  )

  override def dataType: DataType = DataTypes.createMapType(DataTypes.StringType, DataTypes.DoubleType)

  override def deterministic: Boolean = true

  override def initialize(buffer: MutableAggregationBuffer): Unit = {
    buffer.update(0, Map())
  }

  def dayformat(day: String, dimen_mode: String): String = {
    val ca = Calendar.getInstance()
    ca.set(day.substring(0, 4).toInt, day.substring(5, 7).toInt - 1, day.substring(8, 10).toInt)
    dimen_mode match {
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
      case "ym" => ca.get(Calendar.YEAR).toString + "年" + (ca.get(Calendar.MONTH) + 1) + "月"
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
      case _ =>
        throw new RuntimeException("nonexistent dimen_mode. [y,yq,ym,yw,ymd]]")
    }
  }

  def hasRD(input: String): Boolean = {
    val s = "\\d+-\\d+-\\d+ \\d+:\\d+:\\d+"
    val pattern = Pattern.compile(s)
    val ma = pattern.matcher(input)
    ma.find()
  }

  override def update(buffer: MutableAggregationBuffer, input: Row): Unit = {

    var cat = buffer.getAs[Map[String, Double]](0)

    var r1 = input.getAs[Seq[String]](0)
    val value = input.getAs[Double](1)
    val dimen_mode = input.getAs[String](2)


    val report_date = r1.filter(hasRD(_)).map(dayformat(_, dimen_mode))
    r1 = r1.filter(!hasRD(_))
    val key = report_date.mkString("△") + "△" + r1.mkString("△")
    val cat_v = cat.getOrElse(key, 0.00)
    cat += (key -> (cat_v + value))
    buffer.update(0,cat)
  }

  override def merge(buffer1: MutableAggregationBuffer, buffer2: Row): Unit = {

    val cat1 = buffer1.getAs[Map[String, Double]](0)

    val cat2 = buffer2.getAs[Map[String, Double]](0)

    val dog = cat1 ++ cat2.map(t => t._1 -> (t._2 + cat1.getOrElse(t._1, 0.00)))
    buffer1.update(0, dog)
  }

  override def evaluate(buffer: Row): Any = {
    buffer.getAs[Map[String, Double]](0)
  }
    }
    )
    """
    # ,
    # 'kind': "sql"
}
# 172.20.44.6
# bi-olap1.sm02

sid = 77903
response = requests.post("http://172.20.44.6:8999/sessions/" + str(sid) + '/statements', data=json.dumps(data),
                         headers=headers)
# response = requests.post("http://192.168.101.39:8999:8999/sessions/" + str(sid) + '/statements', data=json.dumps(data),
#                          headers=headers)
print(response.text)
id = response.json()['id']
print(id)
time.sleep(10)
response = request.urlopen('http://172.20.44.6:8999/sessions/%d/statements/%d' % (sid, id))
statements = json.loads(response.read())
print(statements)
stmt = statements['state']
print('getStatements %s' % (statements['state']))
if 'available' == stmt:
    print(111)
