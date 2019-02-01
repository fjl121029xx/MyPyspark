#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'wsc'


# Question = Row('pid', 'qid')

def Hello():
    print("say Hello")


def mypartiton(arr):
    list = []
    for r in arr:
        list.append({'pid': r.points[2], 'qid': r._id})
    return list


def myfile(r):
    if r.isNull & r.points.isEmpty:
        return False
    len(r.points) == 3
