#!/usr/bin/env python
# -*- coding:utf-8 -*-
from livy.fun.ReportDateFormat import report_date_format
from livy.fun.compare import compare
from livy.fun.compareRate import compare_rate

__author__ = 'fjl'

import json
import requests
from urllib import request
import time
def reg():
    url1 = "http://172.20.44.6:8999/sessions/"
    sid = []
    response = request.urlopen(url1)
    sessionDict = json.loads(response.read())['sessions']

    for i in range(len(sessionDict)):
        cur = sessionDict[i]
        sid.append(cur['id'])

    for i in sid:
        print(i)
        report_date_format(i, url1)
        compare(i, url1)
        compare_rate(i, url1)
        # row_col_stat(i, url1)
        # ***************************
        # report_date_format(sid2, url1)
        # compare(sid2, url1)
        # compare_rate(sid2, url1)
reg()