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
      DataTypes.createStructField("measure_func", DataTypes.createArrayType(DataTypes.StringType), true),
      DataTypes.createStructField("rowsumtype", DataTypes.createArrayType(DataTypes.StringType), true)
    ))

  override def bufferSchema: StructType =
    DataTypes.createStructType(util.Arrays.asList(
      DataTypes.createStructField(
        "buffer_measure",
        DataTypes.createMapType(
          DataTypes.StringType,
          DataTypes.createMapType(DataTypes.StringType, DataTypes.StringType, true),
          true),
        true),
      DataTypes.createStructField("measure_func", DataTypes.StringType, true),
      DataTypes.createStructField(
        "buffer_dimension",
        DataTypes.createMapType(
          DataTypes.StringType,
          DataTypes.StringType,
          true),
        true),
      DataTypes.createStructField("rowcol", DataTypes.StringType, true),
      DataTypes.createStructField("dimension_length", DataTypes.IntegerType, true),
      DataTypes.createStructField("compare_length", DataTypes.IntegerType, true),
      DataTypes.createStructField("measure_length", DataTypes.IntegerType, true),
      DataTypes.createStructField("rowsumtype", DataTypes.StringType, true)
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
    buffer.update(7, "")
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
    var cat = buffer.getAs[Map[String, Map[String, String]]](0)

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

    val rowsumtype = input.getAs[Seq[String]](6)
    buffer.update(7, rowsumtype.mkString("_"))

    // measure_name
    val measure_func = input.getAs[Seq[String]](5)
    buffer.update(1, measure_func.mkString(","))
    val measure = measure_func.zip(measure_value).toMap

    //
    //    val row_sum = input.getAs[Seq[String]](6)
    //    buffer.update(7, row_sum.mkString("_"))

    var subCat: Map[String, String] = cat.getOrElse(dimension_key, Map())

    // 列统计
    measure.foreach(mea => {
      val key = mea._1
      val value = mea._2.toString
      val key_arr = key.split("-")

      val mea_key = compare_key + "△" + key

      key_arr(1) match {
        case "sum" => {
          var v = subCat.getOrElse(mea_key, "0.00").toDouble
          v = (v + value.toDouble)
          subCat += (mea_key -> v.toString)
        }
        case "count" => {
          var v = subCat.getOrElse(mea_key, "0.00").toDouble
          v = (v + 1)
          subCat += (mea_key -> v.toString)
        }
        case "max" => {
          var v = subCat.getOrElse(mea_key, "0.00").toDouble
          if (value.toDouble > v) {
            v = value.toDouble
          }
          subCat += (mea_key -> v.toString)
        }
        case "min" => {
          var v = subCat.getOrElse(mea_key, "0.00").toDouble
          if (value.toDouble < v) {
            v = value.toDouble
          }
          subCat += (mea_key -> v.toString)
        }
        case "avg" => {
          val v = subCat.getOrElse(mea_key, "0,0")
          var a = v.split(",")(0).toDouble
          val b = v.split(",")(1).toDouble + 1.0
          a = a + value.toDouble
          subCat += (mea_key -> ("%f,%f".format(a, b)))
        }
        case "discount" => {
          var v = subCat.getOrElse(mea_key, "")
          if (v.eq("")) {
            v = value
          } else if (!v.contains(value)) {
            v = "%s,%s".format(v, value)
          }
          subCat += (mea_key -> v)

        }
        case _ => throw new RuntimeException("")
      }

    })

    cat += (dimension_key -> subCat)
    buffer.update(0, cat)

    // 行统计
    var dog = buffer.getAs[Map[String, String]](2)
    measure.foreach(m => {
      val dimension_tmp_key = dimension_key + "△" + m._1
      val m_value = m._2.toString

      if (m._1.endsWith("sum")) {

        var v = dog.getOrElse(dimension_tmp_key, "0.00").toDouble
        v = v + m_value.toDouble
        dog += (dimension_tmp_key -> v.toString)
      } else if (m._1.endsWith("count")) {

        var v = dog.getOrElse(dimension_tmp_key, "0.00").toDouble
        v = v + 1
        dog += (dimension_tmp_key -> v.toString)
      } else if (m._1.endsWith("max")) {

        var v = dog.getOrElse(dimension_tmp_key, "0.00").toDouble
        if (m_value.toDouble > v) {
          v = m_value.toDouble
        }
        dog += (dimension_tmp_key -> v.toString)
      } else if (m._1.endsWith("min")) {

        var v = dog.getOrElse(dimension_tmp_key, "0.00").toDouble
        if (m_value.toDouble < v) {
          v = m_value.toDouble
        }
        dog += (dimension_tmp_key -> v.toString)
      } else if (m._1.endsWith("avg")) {

        val v = dog.getOrElse(dimension_tmp_key, "0,0")
        var a = v.split(",")(0).toDouble
        val b = v.split(",")(1).toDouble + 1.0
        a = a + m_value.toDouble
        dog += (dimension_tmp_key -> "%f,%f".format(a, b))
      } else if (m._1.endsWith("discount")) {
        var v = dog.getOrElse(dimension_tmp_key, "")
        if (v.eq("")) {
          v = m_value
        } else if (!v.contains(m_value)) {
          v = v + "," + m_value
        }
        dog += (dimension_tmp_key -> v)
      }

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

    println(buffer2.getString(7))
    buffer1.update(7, buffer2.getString(7))

    val measure_name = buffer2.getAs[String](1)
    buffer1.update(1, measure_name)

    // 列维度
    var cat1 = buffer1.getAs[Map[String, Map[String, String]]](0)
    val cat2 = buffer2.getAs[Map[String, Map[String, String]]](0)
    val key = cat1.keySet ++ cat2.keySet

    key.foreach(k => {
      var cat11 = cat1.getOrElse(k, Map())
      val cat21 = cat2.getOrElse(k, Map())

      val ckey = cat11.keySet ++ cat21.keySet
      ckey.foreach(subk => {
        if (subk.contains("count")) {

          val dvalue = cat11.getOrElse(subk, "0.00").toDouble + cat21.getOrElse(subk, "0.00").toDouble
          cat11 += (subk -> dvalue.toString)
        } else if (subk.contains("max")) {
          var dvalue1 = cat11.getOrElse(subk, "0.00").toDouble
          val dvalue2 = cat21.getOrElse(subk, "0.00").toDouble
          if (dvalue2 > dvalue1) {
            dvalue1 = dvalue2
          }
          cat11 += (subk -> dvalue1.toString)
        } else if (subk.contains("min")) {

          var dvalue1 = cat11.getOrElse(subk, "0.00").toDouble
          val dvalue2 = cat21.getOrElse(subk, "0.00").toDouble
          if (dvalue2 < dvalue1) {
            dvalue1 = dvalue2
          }
          cat11 += (subk -> dvalue1.toString)
        } else if (subk.contains("discount")) {
          var dvalue1 = cat11.getOrElse(subk, "")
          val dvalue2 = cat21.getOrElse(subk, "")

          val dvalue2_arr = dvalue2.split(",")
          dvalue2_arr.foreach(f => {
            if (dvalue1.eq("")) {
              dvalue1 = f
            } else if (!dvalue1.contains(f)) {
              dvalue1 = dvalue1 + "," + f
            }
          })
        } else if (subk.contains("avg")) {
          val dvalue1 = cat11.getOrElse(subk, "0,0")
          val dvalue2 = cat21.getOrElse(subk, "0,0")

          val a1 = dvalue1.split(",")(0).toDouble
          val a2 = dvalue1.split(",")(1).toDouble

          val b1 = dvalue2.split(",")(0).toDouble
          val b2 = dvalue2.split(",")(1).toDouble
          cat11 += (subk -> ((a1 + b1) / (a2 + b2)).toString)
        } else {
          val dvalue = cat11.getOrElse(subk, "0.00").toDouble + cat21.getOrElse(subk, "0.00").toDouble
          cat11 += (subk -> dvalue.toString)
        }
        cat1 += (k -> cat11)
      })
    })
    buffer1.update(0, cat1)


    var dog1 = buffer1.getAs[Map[String, String]](2)
    val dog2 = buffer2.getAs[Map[String, String]](2)

    val dkey = dog1.keySet ++ dog2.keySet

    dkey.foreach(key => {
      if (key.contains("count")) {
        val v1 = dog2.getOrElse(key, "0.00").toDouble
        val v2 = dog1.getOrElse(key, "0.00").toDouble
        val result = v1 + v2
        dog1 += (key -> result.toString)
      } else if (key.contains("max")) {
        var v1 = dog2.getOrElse(key, "0.00").toDouble
        val v2 = dog1.getOrElse(key, "0.00").toDouble

        if (v2 > v1) {
          v1 = v2
        }
        dog1 += (key -> v1.toString)
      } else if (key.contains("min")) {
        var v1 = dog2.getOrElse(key, "0.00").toDouble
        val v2 = dog1.getOrElse(key, "0.00").toDouble

        if (v2 < v1) {
          v1 = v2
        }
        dog1 += (key -> v1.toString)
      } else if (key.contains("discount")) {

        val v1 = dog2.getOrElse(key, "")
        var v2 = dog1.getOrElse(key, "")
        if (v2.eq("")) {
          v2 = v1
        } else {
          val vrr = v1.split(",")
          vrr.foreach(f => {
            if (!v2.contains(f)) {
              v2 = v2 + "," + f
            }
          })
        }
        dog1 += (key -> v2.toString)

      } else if (key.contains("avg")) {

        val v1 = dog2.getOrElse(key, "0,0")
        val v2 = dog1.getOrElse(key, "0,0")
        val a1 = v1.split(",")(0).toDouble
        val a2 = v1.split(",")(1).toDouble
        val b1 = v2.split(",")(0).toDouble
        val b2 = v2.split(",")(1).toDouble

        dog1 += (key -> ((a1 + b1) / (a2 + b2)).toString)
      } else {
        val v1 = dog2.getOrElse(key, "0.00").toDouble
        val v2 = dog1.getOrElse(key, "0.00").toDouble
        val result = v1 + v2
        dog1 += (key -> result.toString)
      }
    })
    buffer1.update(2, dog1)
  }


  override def evaluate(row: Row): Any = {
    // dimension_key + compare_key

    val cat = row.getAs[Map[String, Map[String, String]]](0)
    val dog = row.getAs[Map[String, String]](2)

    val compare: Map[String, Map[String, Double]] = cat.map(f => {
      val key = f._1
      val value = f._2
      val p = Pattern.compile("\\\\d+\\\\.\\\\d+$|-\\\\d+\\\\.\\\\d+$")
      val p2 = Pattern.compile("\\\\d+\\\\.\\\\d+,\\\\d+\\\\.\\\\d+$")
      key -> value.map(en => {
        if (p.matcher(en._2).matches()) {
          en._1 -> en._2.toDouble
        } else if (p2.matcher(en._2).matches()) {
          en._1 -> en._2.split(",")(0).toDouble / en._2.split(",")(1).toDouble
        } else {
          en._1 -> en._2.split(",").length.toDouble
        }
      })
    })


    val dimension: Map[String, Double] = dog.map(en => {
      val key = en._1
      val value = en._2
      val p = Pattern.compile("\\\\d+\\\\.\\\\d+$|-\\\\d+\\\\.\\\\d+$")
      val p2 = Pattern.compile("\\\\d+\\\\.\\\\d+,\\\\d+\\\\.\\\\d+$")
      if (p.matcher(value).matches()) {
        key -> value.toDouble
      } else if (p2.matcher(value).matches()) {
        key -> value.split(",")(0).toDouble / value.split(",")(1).toDouble
      } else {
        key -> value.split(",").length.toDouble
      }
    })


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
        result += (i._1 + "△" + i._2 -> 0.00)
      })

      sub_ttal.foreach(i => {
        result += (i._1 + "△" + i._2 -> 0.00)
      })

    } else if (rowcol.toInt == 6 || rowcol.toInt == 4 || rowcol.toInt == 2) {
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
      if (rowcol.toInt == 4 && rowcol.toInt != 2) {
        totalSumMap.foreach(en => {
          val key = "%s△%s△columnSum".format(en._1, en._2)
          result += (key -> 0.00)
        })
      }
      if (rowcol.toInt != 4 && rowcol.toInt == 2) {
        sub_totalSumMap.foreach(en => {
          val key = "%s△%s△columnSum_subtotal_".format(en._1, en._2)
          result += (key -> 0.00)
        })
      }
      if (rowcol.toInt == 6) {
        totalSumMap.foreach(en => {
          val key = "%s△%s△columnSum".format(en._1, en._2)
          result += (key -> 0.00)
        })
        sub_totalSumMap.foreach(en => {
          val key = "%s△%s△columnSum_subtotal_".format(en._1, en._2)
          result += (key -> 0.00)
        })
      }

    } else {
      throw new RuntimeException("rowcol [0,1,6,7]")
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
row_col_stat(78628, url)
row_col_stat(78627, url)
