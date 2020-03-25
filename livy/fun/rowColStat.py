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
      DataTypes.createStructField("rowcol_num", DataTypes.StringType, true),
      DataTypes.createStructField("date_mode", DataTypes.StringType, true),
      DataTypes.createStructField("measure_func", DataTypes.createArrayType(DataTypes.StringType), true)
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

  def dayformat(day: String, dimen_mode: String, format: Int): String = {
    if (day.length != 8 && day.length != 19 && day.length != 10) {
      return day
    }
    val ca = Calendar.getInstance()
    if (format == 19 || format == 10) {
      ca.set(day.substring(0, 4).toInt, day.substring(5, 7).toInt - 1, day.substring(8, 10).toInt)
    } else if (format == 8) {
      ca.set(day.substring(0, 4).toInt, day.substring(4, 6).toInt - 1, day.substring(6, 8).toInt)
    } else {
      return day
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
      case _ =>
        throw new RuntimeException("nonexistent dimen_mode. [y,yq,ym,yw,ymd]]")
    }
  }


  def hasRD(input: String): Int = {
    var s = "\\\\d+-\\\\d+-\\\\d+ \\\\d+:\\\\d+:\\\\d+"
    var pattern = Pattern.compile(s)
    var ma = pattern.matcher(input)
    if (ma.find()) 19
    else {
      s = "\\\\d+-\\\\d+-\\\\d+"
      pattern = Pattern.compile(s)
      ma = pattern.matcher(input)
      if (ma.find()) 10
      else {
        s = "^[0-9]*$"
        pattern = Pattern.compile(s)
        ma = pattern.matcher(input)
        if (ma.find()) 8
        else 0
      }
    }
  }

  def regJson(json: Option[Any]) = json match {
    case Some(map: Map[String, Any]) => map
    //      case None => "erro"
    //      case other => "Unknow data structure : " + other
  }

  override def update(buffer: MutableAggregationBuffer, input: Row): Unit = {

    // 行统计维度
    var cat = buffer.getAs[Map[String, Map[String, Double]]](0)

    // 时间格式化 ymd ...
    val dimen_mode = input.getAs[String](4)
    val rowcol = input.getAs[String](3)
    buffer.update(3, rowcol)

    // dimensions
    // 行键
    val dimensions = input.getAs[Seq[String]](0).map(d => {
      if (hasRD(d) > 7) {
        dayformat(d, dimen_mode, hasRD(d))
      } else {
        d
      }
    })
    buffer.update(4, dimensions.length)
    // 行键
    val dimension_key = dimensions.mkString("△")

    // compare
    // 列键
    val compare = input.getAs[Seq[String]](1)
    val compare_key = (dimensions ++ compare).mkString("△")
    buffer.update(5, compare.length)

    // measure_value
    val measure_value = input.getAs[Seq[String]](2)
    buffer.update(6, measure_value.length)

    // measure_name
    val measure_func = input.getAs[Seq[String]](5)
    buffer.update(1, measure_func.mkString(","))
    val measure = measure_func.zip(measure_value).toMap


    var subCat = cat.getOrElse(dimension_key, Map())

    // 列统计
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

    // 行统计
    var dog = buffer.getAs[Map[String, Double]](2)
    measure.foreach(m => {
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
    // rowcol
    buffer1.update(3, buffer2.getAs[String](3))
    // length [dimension compare measure]
    buffer1.update(4, buffer2.getInt(4))
    buffer1.update(5, buffer2.getInt(5))
    buffer1.update(6, buffer2.getInt(6))

    val measure_name = buffer2.getAs[String](1)
    buffer1.update(1, measure_name)

    // 列维度
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
      val key = t._1.toString
      val value1 = t._2
      val value2 = dog1.getOrElse(t._1, 0.00)
      t._1.toString -> (t._2 + dog1.getOrElse(t._1, 0.00))
    })
    buffer1.update(2, dog3)
  }


  override def evaluate(row: Row): Any = {
    // dimension_key + compare_key
    val compare = row.getAs[Map[String, Map[String, Double]]](0)
    val dimension = row.getAs[Map[String, Double]](2)


    val dimension_length = row.getInt(4)
    val compare_length = row.getInt(5)
    val measure_length = row.getInt(6)

    val measure_name = row.getAs[String](1)
    val measure_arr = measure_name.split(",")

    // 列
    var compareValue = mutable.Map[String, Double]()
    compare.values.foreach(en =>
      compareValue = compareValue ++ en
    )
    // rowcol
    val rowcol = row.getAs[String](3)

    var result: Map[String, Double] = Map()

    compareValue.foreach(en => {
      val measure_key = en._1

      val compare_key = measure_key.substring(0, measure_key.lastIndexOf("△"))
      var compare_key_tmp = measure_key.substring(0, measure_key.lastIndexOf("△"))

      val all_keys = compare_key.split("△")

      var dimensionKeys = all_keys(0)
      for (i <- 1 until dimension_length) {
        dimensionKeys = dimensionKeys + "△" + all_keys(i)
      }

      var compareKeys = all_keys(dimension_length)
      for (i <- dimension_length + 1 until dimension_length + compare_length) {
        compareKeys = compareKeys + "△" + all_keys(i)
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

      // 行合计
      if (rowcol.toInt == 1 || rowcol.toInt == 7) {
        for (i <- 0 until measure_arr.length) {
          val s = measure_arr(i)
          val v = dimension.getOrElse(dimensionKeys + "△" + s, 0.00)
          tmp_count2 = tmp_count2 + v
          compare_key_tmp = compare_key_tmp + "△" + v
        }
        compare_key_tmp = compare_key_tmp + "△" + tmp_count2
        compare_key_tmp = compare_key_tmp + "△" + tmp_count + "△"
      } else {
        compare_key_tmp = compare_key_tmp + "△"
      }


      result += (compare_key_tmp -> 0.00)
    })

    if (rowcol.toInt == 7) {
      val mea = new Array[Double](measure_length).mkString("△")

      var totalSumMap = Map[String, String]()
      var total_key = "总计"
      for (i <- 1 until dimension_length) total_key += "△"

      result.keySet.foreach(k => {
        val all_key = k.split("△")

        val dimension = splitArray(k.split("△"), 0, dimension_length)
        val compare = splitArray(k.split("△"), dimension_length, dimension_length + compare_length)
        val measure = splitArray(k.split("△"), dimension_length + compare_length, dimension_length + compare_length + measure_length)

        var v_tmp = all_key(dimension_length + compare_length) + ""

        val total_pre_key = s"${total_key}△${compare.mkString("△")}"
        val res = totalSumMap.getOrElse(total_pre_key, mea).split("△").zip(measure).map(t => t._1.toDouble + t._2.toDouble).mkString("△")

        val sumRes = "%.1f".format(res.split("△").map(_.toDouble).sum)
        totalSumMap += (total_pre_key -> ("%s△%s△%s△%s△columnSum".format(res, res, sumRes, sumRes)))

      })

      var sub_ttal = Map[String, String]()
      result.keySet.foreach(k => {
        val dimension = splitArray(k.split("△"), 0, dimension_length)
        val compare = splitArray(k.split("△"), dimension_length, dimension_length + compare_length)
        val measure = splitArray(k.split("△"), dimension_length + compare_length, dimension_length + compare_length + measure_length)

        for (i <- 1 until dimension_length) {
          var dkey = dimension.zipWithIndex.filter(_._2 < i).map(_._1).mkString("△") + "△小计"

          if (dkey.split("△").length < dimension_length) {
            for (i <- 0 until (dimension_length - dkey.split("△").length)) {
              dkey += "△"
            }
          }
          val subtotal_tmp_key = "%s△%s".format(dkey, compare.mkString("△"))
          val res = sub_ttal.getOrElse(subtotal_tmp_key, mea).split("△").zip(measure).map(t => t._1.toDouble + t._2.toDouble).mkString("△")
          val sumRes = "%.1f".format(res.split("△").map(_.toDouble).sum)
          sub_ttal += (subtotal_tmp_key -> ("%s△%s△%s△%s△columnSum_subtotal_".format(res, res, sumRes, sumRes)))
        }
      })

      totalSumMap.foreach(i => {
        result += (i._1 + "△" + i._2 -> 2.00)
      })

      sub_ttal.foreach(i => {
        result += (i._1 + "△" + i._2 -> 1.00)
      })

    } else if (rowcol.toInt == 6 || rowcol.toInt == 2 || rowcol.toInt == 4) {
      val mea = new Array[Double](measure_length).mkString("△")

      var total_key = "总计"
      for (i <- 1 until dimension_length) total_key += "△"

      var totalSumMap = Map[String, String]()
      result.keySet.foreach(k => {
        val dimension = splitArray(k.split("△"), 0, dimension_length)
        val compare = splitArray(k.split("△"), dimension_length, dimension_length + compare_length)
        val measure = splitArray(k.split("△"), dimension_length + compare_length, dimension_length + compare_length + measure_length)
        val total_tmp_key = "%s△%s".format(total_key, compare.mkString("△"))

        val res = totalSumMap.getOrElse(total_tmp_key, mea).split("△").zip(measure).map(t => t._1.toDouble + t._2.toDouble).mkString("△")
        totalSumMap += (total_tmp_key -> res)
      })

      var sub_totalSumMap = Map[String, String]()
      result.keySet.foreach(k => {
        val dimension = splitArray(k.split("△"), 0, dimension_length)
        val compare = splitArray(k.split("△"), dimension_length, dimension_length + compare_length)
        val measure = splitArray(k.split("△"), dimension_length + compare_length, dimension_length + compare_length + measure_length)

        for (i <- 1 until dimension_length) {
          var dkey = dimension.zipWithIndex.filter(_._2 < i).map(_._1).mkString("△") + "△小计"

          if (dkey.split("△").length < dimension_length) {
            for (i <- 0 until (dimension_length - dkey.split("△").length)) {
              dkey += "△"
            }
          }
          val subtotal_tmp_key = "%s△%s".format(dkey, compare.mkString("△"))
          val res = sub_totalSumMap.getOrElse(subtotal_tmp_key, mea).split("△").zip(measure).map(t => t._1.toDouble + t._2.toDouble).mkString("△")
          sub_totalSumMap += (subtotal_tmp_key -> res)
        }
      })

      if (rowcol.toInt == 4) {
        totalSumMap.foreach(en => {
          val key = "%s△%s△columnSum".format(en._1, en._2)
          result += (key -> 2.00)
        })
      }
      if (rowcol.toInt == 2) {

        sub_totalSumMap.foreach(en => {
          val key = "%s△%s△columnSum_subtotal_".format(en._1, en._2)
          result += (key -> 1.00)
        })
      }
      if (rowcol.toInt == 6) {
        totalSumMap.foreach(en => {
          val key = "%s△%s△columnSum".format(en._1, en._2)
          result += (key -> 2.00)
        })
        sub_totalSumMap.foreach(en => {
          val key = "%s△%s△columnSum_subtotal_".format(en._1, en._2)
          result += (key -> 1.00)
        })
      }
    }
    result
  }

  def splitArray(arr: Seq[String], a: Int, b: Int): Seq[String] = {
    var newArr = Seq[String]()
    for (i <- a until b) {
      newArr = newArr :+ arr(i)
    }
    newArr
  }
  
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
row_col_stat(78357, url)
