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
    spark.udf.register("compare_sum_rate", new UserDefinedAggregateFunction() {

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
      DataTypes.createStructField("measure", DataTypes.DoubleType, true),
      DataTypes.createStructField("dimen_mode", DataTypes.StringType, true),
      DataTypes.createStructField("time_diff_type", DataTypes.StringType, true)
    ))

  override def bufferSchema: StructType =
    DataTypes.createStructType(util.Arrays.asList(
      DataTypes.createStructField(
        "mid_result",
        DataTypes.createMapType(DataTypes.StringType, DataTypes.DoubleType, true),
        true),
      DataTypes.createStructField("dimen_mode", DataTypes.StringType, true),
      DataTypes.createStructField("time_diff_type", DataTypes.StringType, true),

      DataTypes.createStructField("min_reportdate", DataTypes.IntegerType, true),
      DataTypes.createStructField("max_reportdate", DataTypes.IntegerType, true)
    )
    )

  override def dataType: DataType =
  //        DataTypes.createMapType(DataTypes.createArrayType(DataTypes.StringType), DataTypes.DoubleType)
    DataTypes.createMapType(DataTypes.StringType, DataTypes.StringType)

  override def deterministic: Boolean = true

  override def initialize(buffer: MutableAggregationBuffer): Unit = {
    buffer.update(0, Map())
    buffer.update(1, "yearmonthday")
    buffer.update(2, "month")

    val format = new SimpleDateFormat("yyyyMMdd");
    val time = format.format(Calendar.getInstance().getTime()).toInt
    // ↓补全日期
    buffer.update(3, time)
    buffer.update(4, time)

  }

  def dayformat(day: String, dimen_mode: String): String = {
    val ca = Calendar.getInstance()
    if (day.contains("-")) {
      ca.set(day.substring(0, 4).toInt, day.substring(5, 7).toInt - 1, day.substring(8, 10).toInt)
    } else {
      if (day.contains("年")) {
        // 年
        ca.set(day.substring(0, 4).toInt, 0, 1)
      } else if (day.contains("年") && day.contains("月") && day.contains("日")) {
        // 年月日
        ca.set(day.substring(0, 4).toInt, day.substring(day.indexOf("年") + 1, day.indexOf("月")).toInt - 1,
          day.substring(day.indexOf("月") + 1, day.indexOf("日")).toInt)
      } else if (day.contains("年") && day.contains("月")) {
        // 年月
        ca.set(day.substring(0, 4).toInt, day.substring(day.indexOf("年") + 1, day.indexOf("月")).toInt - 1, 1)
      } else if (day.contains("年") && day.contains("周")) {
        // 年周
        ca.setFirstDayOfWeek(Calendar.MONDAY)
        ca.set(Calendar.YEAR, day.substring(0, 4).toInt)
        ca.set(Calendar.WEEK_OF_YEAR, day.substring(day.indexOf("年") + 1, day.indexOf("周")).toInt)
      } else if (day.contains("年") && day.contains("季度")) {
        // 年季度
        val m = day.substring(day.indexOf("年") + 1, day.indexOf("季度")).toInt match {
          case 1 => 1
          case 2 => 4
          case 3 => 7
          case _ => 10
        }
        ca.set(day.substring(0, 4).toInt, m - 1, 1)
      } else {
        ca.set(day.substring(0, 4).toInt, day.substring(4, 6).toInt - 1, day.substring(6, 8).toInt)
      }

    }

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

  // 判断是否存在reportdate
  def hasRD(input: String): Boolean = {
    val s = "\\\\d+-\\\\d+-\\\\d+"
    val pattern = Pattern.compile(s)
    val ma = pattern.matcher(input)
    var arr: Array[String] = Array()
    ma.find()
  }

  def hasRD2(input: String): Boolean = {
    val s = "\\\\d+-\\\\d+-\\\\d+"
    val pattern = Pattern.compile(s)
    val ma = pattern.matcher(input)
    ma.find()
  }

  def generateKey(rd: String, s: Seq[AnyRef]): String = {
    var buffer = rd
    s.foreach(f => buffer += ("_" + f))

    buffer
  }

  override def update(buffer: MutableAggregationBuffer, input: Row): Unit = {

    //
    var cat = buffer.getAs[Map[String, Double]](0)
    val dimen_mode = input.getAs[String](2)

    val dimensions = input.getAs[Seq[String]](0)

    val aggr_key = dimensions.map(l => {
      if (hasRD2(l) || hasRD(l)) {
        dayformat(l, dimen_mode)
      } else {
        l
      }
    }).mkString("_")

    val min_reportdate = buffer.getAs[Int](3)
    val max_reportdate = buffer.getAs[Int](4)

    var measure = input.getAs[Double](1)

    val i = cat.getOrElse(aggr_key, 0.00)
    measure = i + measure
    cat += (aggr_key -> measure)

    buffer.update(0, cat)
    // dimen_mode
    buffer.update(1, input.getAs[String](2))
    // time_diff_type
    buffer.update(2, input.getAs[String](3))
  }

  override def merge(buffer1: MutableAggregationBuffer, buffer2: Row): Unit = {

    val cat1 = buffer1.getAs[Map[String, Double]](0)
    val cat2 = buffer2.getAs[Map[String, Double]](0)

    val dog1 = cat1 ++ cat2.map(t => t._1 -> (t._2 + cat1.getOrElse(t._1, 0.00)))
    buffer1.update(0, dog1)

    buffer1.update(1, buffer2.getAs[String](1))
    buffer1.update(2, buffer2.getAs[String](2))

    //
    val min_reportdate1 = buffer1.getAs[Int](3)
    val min_reportdate2 = buffer2.getAs[Int](3)
    if (min_reportdate2 < min_reportdate1)
      buffer1.update(3, min_reportdate2)

    val max_reportdate1 = buffer1.getAs[Int](4)
    val max_reportdate2 = buffer2.getAs[Int](4)
    if (max_reportdate2 < max_reportdate1)
      buffer1.update(4, max_reportdate2)

  }

  def getNumFromMatch(input: String): Array[String] = {

    val s = "\\\\d+"
    val pattern = Pattern.compile(s)
    val ma = pattern.matcher(input)
    val arr: Array[String] = Array()
    while ( {
      ma.find
    }) {
      arr ++ ma.group
    }
    arr
  }

  def creatbasiresult(a: Int, b: Int, dimen_mode: String): Map[String, Double] = {

    var basic_map = Map[String, Double]()
    var flag = true
    var tmp_a = a
    while (flag) {
      val ca = Calendar.getInstance()
      ca.set(tmp_a.toString.substring(0, 4).toInt, tmp_a.toString.substring(4, 6).toInt - 1, tmp_a.toString.substring(6, 8).toInt)

      ca.add(Calendar.DAY_OF_YEAR, 1)
      var m = (ca.get(Calendar.MONTH) + 1).toString
      var d = ca.get(Calendar.DAY_OF_MONTH).toString
      if (m.length < 2) m = "0" + (m.toInt)
      if (d.length < 2) d = "0" + d

      val rd = (ca.get(Calendar.YEAR) + "" + m + "" + d).toInt
      tmp_a = rd
      basic_map += (dayformat(rd.toString, dimen_mode) -> 0.00)
      if (tmp_a > b) {
        flag = false
      }
    }
    basic_map
  }

  override def evaluate(row: Row): Any = {

    val dog = row.getAs[Map[String, Double]](0)
      .map(f => (f._1 -> f._2))

    println("--")
    dog.foreach(f => {
      println(f._1 + " -> " + f._2)
    })
    println("--")

    val dimen_mode = row.getAs[String](1)
    val time_diff_type = row.getAs[String](2)
    val time_diff: Int = -1

    val result: Map[String, String] = dimen_mode match {
      case "y" =>
        time_diff_type match {
          case "0" =>
            val dog2 = dog.map(f => {
              val k = f._1.split("_")
              val k_1 = k.mkString("_")
              val rd = k(0)

              val ca = Calendar.getInstance()
              ca.set(rd.substring(0, 4).toInt, 0, 1)
              ca.add(Calendar.YEAR, time_diff)
              val day = getTime(ca)

              k(0) = dayformat(day, dimen_mode)
              println(f._1 + ":::" +
                k.mkString("_") + ":::" +
                f._2 + ":::" +
                dog.getOrElse(k.mkString("_"), 0.00)
              )
              (k_1, dog.getOrElse(k.mkString("_"), 0.00))
            })

            val result_dog = dog.map(m => {
              var m3 = dog2.getOrElse(m._1, 0.00)
              if (m3 != 0.0) {
                m3 = (m._2 - dog2.getOrElse(m._1, 0.00)) / dog2.getOrElse(m._1, 0.00)
                m._1 -> m3.toString
              } else {
                m._1 -> "-"
              }

            })
            result_dog
          case _ => throw new RuntimeException("dimen_mode y must match time_diff_type[0]")
        }
      case "ym" =>
        time_diff_type match {
          case "1" =>
            val dog2 = dog.map(f => {
              val k = f._1.split("_")
              val k_1 = k.mkString("_")
              val rd = k(0)

              val ca = Calendar.getInstance()
              ca.set(rd.substring(0, 4).toInt, rd.substring(rd.indexOf("年") + 1, rd.indexOf("月")).toInt - 1, 1)
              ca.add(Calendar.YEAR, time_diff)
              val day = getTime(ca)

              k(0) = dayformat(day, dimen_mode)
              println(f._1 + ":::" +
                k.mkString("_") + ":::" +
                f._2 + ":::" +
                dog.getOrElse(k.mkString("_"), 0.00)
              )
              (k_1, dog.getOrElse(k.mkString("_"), 0.00))
            })

            val result_dog = dog.map(m => {
              var m3 = dog2.getOrElse(m._1, 0.00)
              if (m3 != 0.0) {
                m3 = (m._2 - dog2.getOrElse(m._1, 0.00)) / dog2.getOrElse(m._1, 0.00)
                m._1 -> m3.toString
              } else {
                m._1 -> "-"
              }
            })
            result_dog

          case "0" =>
            val dog2 = dog.map(f => {
              val k = f._1.split("_")
              val k_1 = k.mkString("_")
              val rd = k(0)

              val ca = Calendar.getInstance()
              ca.set(rd.substring(0, 4).toInt, rd.substring(rd.indexOf("年") + 1, rd.indexOf("月")).toInt - 1, 1)
              ca.add(Calendar.MONTH, time_diff)
              val day = getTime(ca)
              k(0) = dayformat(day, dimen_mode)
              println(f._1 + ":::" +
                k.mkString("_") + ":::" +
                f._2 + ":::" +
                dog.getOrElse(k.mkString("_"), 0.00)
              )
              (k_1, dog.getOrElse(k.mkString("_"), 0.00))
            })
            val result_dog = dog.map(m => {
              var m3 = dog2.getOrElse(m._1, 0.00)
              if (m3 != 0.0) {
                m3 = (m._2 - dog2.getOrElse(m._1, 0.00)) / dog2.getOrElse(m._1, 0.00)
                m._1 -> m3.toString
              } else {
                m._1 -> "-"
              }

            })
            result_dog

          case _ => throw new RuntimeException("dimen_mode ym must match time_diff_type[0,1]")
        }
      case "yq" =>
        time_diff_type match {
          case "1" =>
            val dog2 = dog.map(f => {
              val k = f._1.split("_")
              val k_1 = k.mkString("_")
              val rd = k(0)

              val ca = Calendar.getInstance()

              val m = rd.substring(rd.indexOf("年") + 1, rd.indexOf("季")).toInt match {
                case 1 => 1
                case 2 => 4
                case 3 => 7
                case _ => 10
              }
              ca.set(rd.substring(0, 4).toInt, m - 1, 1)
              ca.add(Calendar.YEAR, time_diff)
              val day = getTime(ca)
              k(0) = dayformat(day, dimen_mode)
              println(f._1 + ":::" +
                k.mkString("_") + ":::" +
                f._2 + ":::" +
                dog.getOrElse(k.mkString("_"), 0.00)
              )
              (k_1, dog.getOrElse(k.mkString("_"), 0.00))
            })
            val result_dog = dog.map(m => {
              var m3 = dog2.getOrElse(m._1, 0.00)
              if (m3 != 0.0) {
                m3 = (m._2 - dog2.getOrElse(m._1, 0.00)) / dog2.getOrElse(m._1, 0.00)
                m._1 -> m3.toString
              } else {
                m._1 -> "-"
              }

            })
            result_dog

          case "0" =>
            val dog2 = dog.map(f => {
              val k = f._1.split("_")
              val k_1 = k.mkString("_")
              val rd = k(0)
              val ca = Calendar.getInstance()

              val m = rd.substring(rd.indexOf("年") + 1, rd.indexOf("季")).toInt match {
                case 1 => 1
                case 2 => 4
                case 3 => 7
                case _ => 10
              }
              ca.set(rd.substring(0, 4).toInt, m - 1, 1)
              ca.add(Calendar.MONTH, time_diff)
              val day = getTime(ca)
              k(0) = dayformat(day, dimen_mode)
              println(f._1 + ":::" +
                k.mkString("_") + ":::" +
                f._2 + ":::" +
                dog.getOrElse(k.mkString("_"), 0.00)
              )
              (k_1, dog.getOrElse(k.mkString("_"), 0.00))
            })
            val result_dog = dog.map(m => {
              var m3 = dog2.getOrElse(m._1, 0.00)
              if (m3 != 0.0) {
                m3 = (m._2 - dog2.getOrElse(m._1, 0.00)) / dog2.getOrElse(m._1, 0.00)
                m._1 -> m3.toString
              } else {
                m._1 -> "-"
              }

            })
            result_dog

          case _ => throw new RuntimeException("dimen_mode yq must match time_diff_type[0,1]")
        }
      case "yw" =>
        time_diff_type match {
          case "1" =>
            val dog2 = dog.map(f => {
              val k = f._1.split("_")
              val k_1 = k.mkString("_")
              val rd = k(0)

              val ca = Calendar.getInstance()
              ca.setFirstDayOfWeek(Calendar.MONDAY)
              ca.set(Calendar.YEAR, rd.substring(0, 4).toInt)
              ca.set(Calendar.WEEK_OF_YEAR, rd.substring(rd.indexOf("年") + 1, rd.indexOf("周")).toInt)
              ca.add(Calendar.YEAR, time_diff)
              val day = getTime(ca)
              k(0) = dayformat(day, dimen_mode)
              println(f._1 + ":::" +
                k.mkString("_") + ":::" +
                f._2 + ":::" +
                dog.getOrElse(k.mkString("_"), 0.00)
              )
              (k_1, dog.getOrElse(k.mkString("_"), 0.00))
            })
            val result_dog = dog.map(m => {
              var m3 = dog2.getOrElse(m._1, 0.00)
              if (m3 != 0.0) {
                m3 = (m._2 - dog2.getOrElse(m._1, 0.00)) / dog2.getOrElse(m._1, 0.00)
                m._1 -> m3.toString
              } else {
                m._1 -> "-"
              }

            })
            result_dog

          case "0" =>
            val dog2 = dog.map(f => {
              val k = f._1.split("_")
              val k_1 = k.mkString("_")
              val rd = k(0)

              val ca = Calendar.getInstance()
              ca.setFirstDayOfWeek(Calendar.MONDAY)
              ca.set(Calendar.YEAR, rd.substring(0, 4).toInt)
              ca.set(Calendar.WEEK_OF_YEAR, rd.substring(rd.indexOf("年") + 1, rd.indexOf("周")).toInt)
              ca.add(Calendar.WEEK_OF_YEAR, time_diff)
              val day = getTime(ca)

              k(0) = dayformat(day, dimen_mode)
              println(f._1 + ":::" +
                k.mkString("_") + ":::" +
                f._2 + ":::" +
                dog.getOrElse(k.mkString("_"), 0.00)
              )
              (k_1, dog.getOrElse(k.mkString("_"), 0.00))
            })
            val result_dog = dog.map(m => {
              var m3 = dog2.getOrElse(m._1, 0.00)
              if (m3 != 0.0) {
                m3 = (m._2 - dog2.getOrElse(m._1, 0.00)) / dog2.getOrElse(m._1, 0.00)
                m._1 -> m3.toString
              } else {
                m._1 -> "-"
              }

            })
            result_dog

          case _ => throw new RuntimeException("dimen_mode yw must match time_diff_type[0,1]")
        }
      case "ymd" =>
        time_diff_type match {
          case "3" =>
            val dog2 = dog.map(f => {
              val k = f._1.split("_")
              val k_1 = k.mkString("_")
              val rd = k(0)

              val ca = Calendar.getInstance()
              ca.set(rd.substring(0, 4).toInt, rd.substring(rd.indexOf("年") + 1, rd.indexOf("月")).toInt - 1,
                rd.substring(rd.indexOf("月") + 1, rd.indexOf("日")).toInt)
              ca.add(Calendar.YEAR, time_diff)
              val day = getTime(ca)
              k(0) = dayformat(day, dimen_mode)
              println(f._1 + ":::" +
                k.mkString("_") + ":::" +
                f._2 + ":::" +
                dog.getOrElse(k.mkString("_"), 0.00)
              )

              (k_1, dog.getOrElse(k.mkString("_"), 0.00))
            })
            val result_dog = dog.map(m => {
              var m3 = dog2.getOrElse(m._1, 0.00)
              if (m3 != 0.0) {
                m3 = (m._2 - dog2.getOrElse(m._1, 0.00)) / dog2.getOrElse(m._1, 0.00)
                m._1 -> m3.toString
              } else {
                m._1 -> "-"
              }

            })
            result_dog

          case "2" =>
            val dog2 = dog.map(f => {
              val k = f._1.split("_")
              val k_1 = k.mkString("_")
              val rd = k(0)

              val ca = Calendar.getInstance()
              ca.set(rd.substring(0, 4).toInt, rd.substring(rd.indexOf("年") + 1, rd.indexOf("月")).toInt - 1,
                rd.substring(rd.indexOf("月") + 1, rd.indexOf("日")).toInt)
              ca.add(Calendar.MONTH, time_diff)
              val day = getTime(ca)
              k(0) = dayformat(day, dimen_mode)
              println(f._1 + ":::" +
                k.mkString("_") + ":::" +
                f._2 + ":::" +
                dog.getOrElse(k.mkString("_"), 0.00)
              )

              (k_1, dog.getOrElse(k.mkString("_"), 0.00))
            })
            val result_dog = dog.map(m => {
              var m3 = dog2.getOrElse(m._1, 0.00)
              if (m3 != 0.0) {
                m3 = (m._2 - dog2.getOrElse(m._1, 0.00)) / dog2.getOrElse(m._1, 0.00)
                m._1 -> m3.toString
              } else {
                m._1 -> "-"
              }

            })
            result_dog

          case "1" =>
            val dog2 = dog.map(f => {
              val k = f._1.split("_")
              val k_1 = k.mkString("_")
              val rd = k(0)

              val ca = Calendar.getInstance()
              ca.setFirstDayOfWeek(Calendar.MONDAY)
              ca.set(rd.substring(0, 4).toInt, rd.substring(rd.indexOf("年") + 1, rd.indexOf("月")).toInt - 1,
                rd.substring(rd.indexOf("月") + 1, rd.indexOf("日")).toInt)
              ca.add(Calendar.WEEK_OF_YEAR, time_diff)

              val day = getTime(ca)
              k(0) = dayformat(day, dimen_mode)
              println(f._1 + ":::" +
                k.mkString("_") + ":::" +
                f._2 + ":::" +
                dog.getOrElse(k.mkString("_"), 0.00)
              )

              (k_1, dog.getOrElse(k.mkString("_"), 0.00))
            })
            val result_dog = dog.map(m => {
              var m3 = dog2.getOrElse(m._1, 0.00)
              if (m3 != 0.0) {
                m3 = (m._2 - dog2.getOrElse(m._1, 0.00)) / dog2.getOrElse(m._1, 0.00)
                m._1 -> m3.toString
              } else {
                m._1 -> "-"
              }

            })
            result_dog
          case "0" =>
            val dog2 = dog.map(f => {
              val k = f._1.split("_")
              val k_1 = k.mkString("_")
              val rd = k(0)
              val ca = Calendar.getInstance()
              ca.set(rd.substring(0, 4).toInt, rd.substring(rd.indexOf("年") + 1, rd.indexOf("月")).toInt - 1,
                rd.substring(rd.indexOf("月") + 1, rd.indexOf("日")).toInt)
              ca.add(Calendar.DAY_OF_YEAR, time_diff)
              val day = getTime(ca)

              k(0) = dayformat(day, dimen_mode)
              println(f._1 + ":::" +
                k.mkString("_") + ":::" +
                f._2 + ":::" +
                dog.getOrElse(k.mkString("_"), 0.00)
              )

              (k_1, dog.getOrElse(k.mkString("_"), 0.00))
            })


            val result_dog = dog.map(m => {
              var m3 = dog2.getOrElse(m._1, 0.00)
              if (m3 != 0.0) {
                m3 = (m._2 - dog2.getOrElse(m._1, 0.00)) / dog2.getOrElse(m._1, 0.00)
                m._1 -> m3.toString
              } else {
                m._1 -> "-"
              }

            })
            result_dog


          case _ => throw new RuntimeException(
            "dimen_mode ymd must match time_diff_type[0,1,2,3]")
        }

      case _ =>
        throw new RuntimeException("nonexistent dimen_mode. [y,yq,ym,yw,ymd]")
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

sid = 77975
response = requests.post("http://172.20.44.6:8999/sessions/" + str(sid) + '/statements', data=json.dumps(data),
                         headers=headers)
# response = requests.post("http://192.168.101.39:8999:8999/sessions/" + str(sid) + '/statements', data=json.dumps(data),
#                          headers=headers)
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
