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
select  compare_sum_rate(ARRAY(CONCAT(SUBSTR(col_1,1,4),'-', SUBSTR(col_1,6,2),'-', SUBSTR(col_1,9,2))),col_6,'ymd','1') as m from `db_yqs_p_505`.`tbl_p_79466_1577179724` """
    ,
    'kind': "sql"
}
sid = 77731
response = requests.post("http://172.20.44.6:8999/sessions/" + str(sid) + '/statements', data=json.dumps(data),
                         headers=headers)
# response = requests.post("http://192.168.101.39:8999:8999/sessions/" + str(sid) + '/statements', data=json.dumps(data),
#                          headers=headers)
print(response.text)
id = response.json()['id']
print(id)
time.sleep(20)
response = request.urlopen('http://172.20.44.6:8999/sessions/%d/statements/%d' % (sid, id))
statements = json.loads(response.read())
print(statements)
stmt = statements['state']
print('getStatements %s' % (statements['state']))
if 'available' == stmt:
    print(statements)
    # print(statements['output']['data']['application/json']['data'][0])
