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
    
    import scala.collection.mutable
    
    spark.udf.register("compare_sum", new UserDefinedAggregateFunction() {
    
    def getTime(date: String, date_type: String, count: Int): String = {
    val ca = Calendar.getInstance()
    ca.set(date.substring(0, 4).toInt,
      date.substring(4, 6).toInt - 1,
      date.substring(6, 8).toInt)
    date_type match {
      case "year" => ca.add(Calendar.YEAR, count)
      case "month" => ca.add(Calendar.MONTH, count)
      case "week" => ca.add(Calendar.WEEK_OF_YEAR, count)
      case "day" => ca.add(Calendar.DAY_OF_YEAR, count)
      case "hour" => ca.add(Calendar.HOUR_OF_DAY, count)
      case _ => throw new Exception
    }

    var m = (ca.get(Calendar.MONTH)).toString
    var d = ca.get(Calendar.DAY_OF_MONTH).toString
    if (m.length < 2) {
      m = "0" + m
    }
    if (d.length < 2) {
      d = "0" + d
    }

    ca.get(Calendar.YEAR) + "" + m + "" + d
  }

  def getTime(ca: Calendar): String = {
    var m = (ca.get(Calendar.MONTH) + 1).toString
    var d = ca.get(Calendar.DAY_OF_MONTH).toString
    if (m.length < 2) {
      m = "0" + m
    }
    if (d.length < 2) {
      d = "0" + d
    }

    ca.get(Calendar.YEAR) + "" + m + "" + d
  }

  override def inputSchema: StructType =
    DataTypes.createStructType(util.Arrays.asList(
      DataTypes.createStructField("dimension", DataTypes.createArrayType(DataTypes.StringType), true),
      DataTypes.createStructField("compare", DataTypes.createArrayType(DataTypes.StringType), true),
      DataTypes.createStructField("measure", DataTypes.createArrayType(DataTypes.StringType), true),
      DataTypes.createStructField("measure_name", DataTypes.StringType, true),
      DataTypes.createStructField("rowcol", DataTypes.StringType, true)
    ))

  override def bufferSchema: StructType =
    DataTypes.createStructType(util.Arrays.asList(
      DataTypes.createStructField(
        "buffer_measure",
        DataTypes.createMapType(
          DataTypes.StringType,
          DataTypes.createMapType(DataTypes.StringType, DataTypes.DoubleType, true),
          true),
        true),
      DataTypes.createStructField("measure_func", DataTypes.StringType, true),
      DataTypes.createStructField(
        "buffer_dimension",
        DataTypes.createMapType(
          DataTypes.StringType,
          DataTypes.DoubleType,
          true),
        true),
      DataTypes.createStructField("rowcol", DataTypes.StringType, true),
      DataTypes.createStructField("dimension_length", DataTypes.IntegerType, true),
      DataTypes.createStructField("compare_length", DataTypes.IntegerType, true),
      DataTypes.createStructField("measure_length", DataTypes.IntegerType, true)
    )
    )

  //  val dimension_length = 2
  //  val compare_length = 1
  //  val measure_length = 2
  override def dataType: DataType =
    DataTypes.createMapType(DataTypes.StringType, DataTypes.DoubleType)

  override def deterministic: Boolean = true

  override def initialize(buffer: MutableAggregationBuffer): Unit = {
    buffer.update(0, Map())
    buffer.update(1, "")
    buffer.update(2, Map())
    buffer.update(3, "7")
    buffer.update(4, 0)
    buffer.update(5, 0)
    buffer.update(6, 0)
  }

  def dayformat(day: String, dimen_mode: String): String = {
    val ca = Calendar.getInstance()
    ca.set(day.substring(0, 4).toInt, day.substring(4, 6).toInt - 1, day.substring(6, 8).toInt)
    dimen_mode match {
      case "y" => ca.get(Calendar.YEAR).toString + "y"
      case "yq" =>
        val m = ca.get(Calendar.MONTH)
        if (m >= 0 && m < 3) {
          ca.get(Calendar.YEAR).toString + "1"
        } else if (m >= 3 && m < 6) {
          ca.get(Calendar.YEAR).toString + "2"
        } else if (m >= 6 && m < 9) {
          ca.get(Calendar.YEAR).toString + "3"
        } else {
          ca.get(Calendar.YEAR).toString + "4"
        }
      case "ym" => ca.get(Calendar.YEAR).toString + "" + (ca.get(Calendar.MONTH) + 1) + ""
      case "yw" => ca.get(Calendar.YEAR).toString + "" + (ca.get(Calendar.WEEK_OF_YEAR)) + ""
      case "ymd" =>
        var m = (ca.get(Calendar.MONTH) + 1).toString
        var d = ca.get(Calendar.DAY_OF_MONTH).toString
        if (m.length < 2) {
          m = "0" + m
        }
        if (d.length < 2) {
          d = "0" + d
        }
        ca.get(Calendar.YEAR) + "" + m + "" + d + ""
      case _ =>
        throw new RuntimeException("nonexistent dimen_mode. [y,yq,ym,yw,ymd]]")
    }
  }


  // 判断是否存在reportdate
  def hasRD(input: String): Boolean = {
    val s = "\\\\d+-\\\\d+-\\\\d+"
    val pattern = Pattern.compile(s)
    val ma = pattern.matcher(input)
    ma.find()
  }

  def generateKey(s: Seq[AnyRef]): String = {
    s.mkString("_")
  }

  override def update(buffer: MutableAggregationBuffer, input: Row): Unit = {
    // 1 2行 3列
    // 7 行列 3行 1
    buffer.update(3, input.getAs[String](4))

    //
    var cat = buffer.getAs[Map[String, Map[String, Double]]](0)

    // dimensions
    val dimensions = input.getAs[Seq[AnyRef]](0)
    buffer.update(4, dimensions.length)

    // compare
    val compare = input.getAs[Seq[AnyRef]](1)
    buffer.update(5, compare.length)


    // measure_value
    val measure_value = input.getAs[Seq[AnyRef]](2)
    buffer.update(6, measure_value.length)

    // measure_name
    val measure_name = input.getAs[String](3)
    buffer.update(1, measure_name)


    val measure_arr = measure_name.split(",")
    val measure = measure_arr.zip(measure_value).toMap


    val dimension_key = dimensions.mkString("△")
    val compare_key = dimension_key + "△" + compare.mkString("△")
    var subCat = cat.getOrElse(dimension_key, Map())

    measure.foreach(mea => {
      val key = mea._1
      val value = mea._2.toString.toDouble
      val key_arr = key.split("-")

      val mea_key = compare_key + "△" + key
      var v = subCat.getOrElse(mea_key, 0.00)
      key_arr(1) match {
        case "sum" => v = v + value
        case "count" => v = v + 1
        case "max" =>
          if (value > v) v = value
        case "min" =>
          if (value < v) v = value
        case _ => throw new RuntimeException("sum")
      }
      subCat += (mea_key -> v)
    })

    cat += (dimension_key -> subCat)
    buffer.update(0, cat)

    //====
    var dog = buffer.getAs[Map[String, Double]](2)
    measure_arr.zip(measure_value).foreach(m => {
      val dimension_tmp_key = dimension_key + "△" + m._1
      val m_value = m._2.toString.toDouble
      var v = dog.getOrElse(dimension_tmp_key, 0.00)
      if (m._1.endsWith("sum")) {
        v = v + m_value
      } else if (m._1.endsWith("count")) {
        v = v + 1
      }
      dog += (dimension_tmp_key -> v)
    })
    buffer.update(2, dog)

  }


  override def merge(buffer1: MutableAggregationBuffer, buffer2: Row): Unit = {
    //
    buffer1.update(3, buffer2.getAs[String](3))

    buffer1.update(4, buffer2.getInt(4))
    buffer1.update(5, buffer2.getInt(5))
    buffer1.update(6, buffer2.getInt(6))


    val measure_name = buffer2.getAs[String](1)
    buffer1.update(1, measure_name)

    var cat1 = buffer1.getAs[Map[String, Map[String, Double]]](0)
    val cat2 = buffer2.getAs[Map[String, Map[String, Double]]](0)
    val key = cat1.keySet ++ cat2.keySet

    key.foreach(k => {
      var cat11 = cat1.getOrElse(k, Map())
      val cat21 = cat2.getOrElse(k, Map())

      val dkey = cat11.keySet ++ cat21.keySet
      dkey.foreach(subk => {
        if (subk.contains("count")) {

          val dvalue = cat11.getOrElse(subk, 0.00) + cat21.getOrElse(subk, 0.00)
          cat11 += (subk -> dvalue)
        } else {
          val dvalue = cat11.getOrElse(subk, 0.00) + cat21.getOrElse(subk, 0.00)
          cat11 += (subk -> dvalue)
        }
        cat1 += (k -> cat11)
      })
    })
    buffer1.update(0, cat1)


    val dog1 = buffer1.getAs[Map[String, Double]](2)
    val dog2 = buffer2.getAs[Map[String, Double]](2)

    val dog3 = dog1 ++ dog2.map(t => {
      t._1.toString -> (t._2 + dog1.getOrElse(t._1, 0.00))
    })
    buffer1.update(2, dog3)
  }


  override def evaluate(row: Row): Any = {
    // dimension_key + compare_key
    val compare = row.getAs[Map[String, Map[String, Double]]](0)

    val dimension_length = row.getInt(4)
    val compare_length = row.getInt(5)
    val measure_length = row.getInt(6)

    val measure_name = row.getAs[String](1)
    val measure_arr = measure_name.split(",")

    var compareValue = mutable.Map[String, Double]()
    compare.values.foreach(en =>
      compareValue = compareValue ++ en
    )
    val dimension = row.getAs[Map[String, Double]](2)

    val rowcol = row.getAs[String](3)
    var result: Map[String, Double] = Map()
    compareValue.foreach(en => {
      val measure_key = en._1

      val compare_key = measure_key.substring(0, measure_key.lastIndexOf("△"))
      var compare_key_tmp = measure_key.substring(0, measure_key.lastIndexOf("△"))

      val first_key = compare_key.split("△")

      var dimensionKeys = first_key(0)
      for (i <- 1 until dimension_length) {
        dimensionKeys = dimensionKeys + "△" + first_key(i)
      }

      var compareKeys = first_key(dimension_length)
      for (i <- dimension_length + 1 until dimension_length + compare_length) {
        compareKeys = compareKeys + "△" + first_key(i)
      }

      var tmp_count = 0.00
      var tmp_count2 = 0.00

      for (i <- 0 until measure_arr.length) {
        val s = measure_arr(i)
        val tmp_key = compare_key + "△" + s
        val v = compareValue.getOrElse(tmp_key, 0.00)
        tmp_count = tmp_count + v
        compare_key_tmp = compare_key_tmp + "△" + v
      }

      if (rowcol.toInt > 2) {
        for (i <- 0 until measure_arr.length) {
          val s = measure_arr(i)
          val v = dimension.getOrElse(dimensionKeys + "△" + s, 0.00)
          tmp_count2 = tmp_count2 + v
          compare_key_tmp = compare_key_tmp + "△" + v
        }

        compare_key_tmp = compare_key_tmp + "△" + tmp_count2
        compare_key_tmp = compare_key_tmp + "△" + tmp_count + "△"
      }
      result += (compare_key_tmp -> 0.00)
    })

    if (rowcol.toInt > 6) {
      var totl = Map[String, String]()
      var total = "总计"
      for (i <- 1 until dimension_length) {
        total += "△"
      }
      result.keySet.foreach(k => {
        val k_rr = k.split("△")
        var v_tmp = k_rr(dimension_length + compare_length) + ""

        val total_pre_key = total + "△" + k_rr(dimension_length + compare_length - 1)

        var v = totl.getOrElse(total_pre_key, "0△0")
        for (i <- 1 until measure_length) {

          v_tmp = v_tmp + "△" + k_rr(dimension_length + compare_length + i).toDouble
        }
        val c = v.split("△").zip(v_tmp.split("△")).map(m => m._1.toDouble + m._2.toDouble)
        v = v_tmp
        totl += (total_pre_key -> (c.mkString("△") + "△" + c.mkString("△") + "△" + c.sum +
          "△" + c.sum + "△columnSum"
          ))

      })


      var sub_ttal = Map[String, String]()

      result.keySet.foreach(k => {
        val start_length = dimension_length + compare_length
        val k_rr = k.split("△")
        val pre_sub_total_key = k_rr(0) + "△" + "小计" + "△" + k_rr(dimension_length)

        var v_tmp = k_rr(start_length) + ""
        for (i <- 1 until measure_length) {
          v_tmp = v_tmp + "△" + k_rr(start_length + i)
        }
        v_tmp = v_tmp + "△" + k_rr(start_length + measure_length + measure_length + 1)


        var v = sub_ttal.getOrElse(pre_sub_total_key, "0△0△0")

        val c = v.split("△").zip(v_tmp.split("△")).map(m => m._1.toDouble + m._2.toDouble)
        v = v_tmp
        sub_ttal += (pre_sub_total_key -> (c.mkString("△")
          ))
      })

      totl.foreach(i => {
        result += (i._1 + "△" + i._2 -> 0.00)
      })
      sub_ttal.foreach(i => {
        val i2 = i._2.split("△")
        val a = Seq(i2(0), i2(1)).mkString("△")
        val ni2 = a + "△" + a + "△" + (i2(0).toDouble + i2(1).toDouble) + "△" + i2(2)
        result += (i._1 + "△" + ni2 + "△columnSum_subtotal_" -> 0.00)
      })
    }

    result
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
