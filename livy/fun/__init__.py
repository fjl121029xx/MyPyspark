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

url1 = "http://172.20.44.6:8999/sessions/"
url2 = "http://192.168.101.39:8999/sessions/"

sid = 78171
report_date_format(sid, url1)
compare(sid, url1)
compare_rate(sid, url1)
