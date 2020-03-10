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
select row_number() over(order by split(key,'_')[0] ) as `key`, split(key,'_')[0] AS `report_date`, split(key,'_')[1] AS `__brand_id__`, split(key,'_')[2] AS `is_setfood`,cast(value as DECIMAL(15,2)) as `food_realamount` from (select compare_sum(ARRAY(report_date,__brand_id__,is_setfood),food_realamount,'ymd','0') as m from `db_yqs_b_505`.`tbl_pos_bill_food`) t LATERAL VIEW explode(t.m) tt as key ,value order by report_date desc
   """
    ,
    'kind': "sql"
}
sid = 77903
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
