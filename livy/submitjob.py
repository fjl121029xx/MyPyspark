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
# select compare_sum(Array(report_date),food_price_amount,'ymd','0') as m from `db_yqs_b_505`.`tbl_pos_bill_food`
data = {
    'code': """
    select compare(Array(report_date),food_price_amount,'ymd','0','sum') as m from `db_yqs_b_505`.`tbl_pos_bill_food`;
   """
    ,
    'kind': "sql"
}
sid = 78366
# url = "http://bi-olap1.sm02:8999/sessions/"
url="http://172.20.44.6:8999/sessions/"
response = requests.post(url + str(sid) + '/statements', data=json.dumps(data),
                         headers=headers)
id = response.json()['id']
print(id)
stmt = 'running'
while stmt != 'available':
    response = request.urlopen(url + '%d/statements/%d' % (sid, id))
    statements = json.loads(response.read())
    stmt = statements['state']
    print(stmt)
    time.sleep(5)
    if 'available' == stmt:
        print(statements)
