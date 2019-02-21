#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'wsc'
from pyspark.sql import Row


# Question = Row('pid', 'qid')

def Hello():
    print("say Hello")


# Row(name='Alice', age=5, height=80)
# {'pid': r.points[2], 'qid': r._id}
def mypartiton(arr):
    list = []
    for r in arr:
        list.append(Row(pid=r.points[2], qid=r._id))
    return list


def myfile(r):
    if r.points:
        if len(r.points) != 3:
            return False
    else:
        return False

    return True


def get_word(s):
    return str(s) + "udf"
