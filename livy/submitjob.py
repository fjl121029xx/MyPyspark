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
    desc  db_yqs_p_common.rt_bill_shop_summary
   """
    ,
    'kind': "sql"
}
sid = 9292
# SELECT sum(bill_actual_amt) AS `bill_actual_amt_1575284488348`, timestamp_format(report_date ,'ymd' ) AS `report_date_1575284605702` FROM `db_yqs_b_777777777`.`standard_summary_bill_shop_food_day_8`  GROUP BY report_date_1575284605702 ORDER BY `report_date_1575284605702`ASC LIMIT 1000
# SELECT sum(bill_actual_amt) AS `bill_actual_amt_1575284488348`, report_date_format(cast(report_date as string) ,'ymd' ) AS `report_date_1575284605702` FROM `db_yqs_b_777777777`.`standard_summary_bill_shop_food_day_8`  GROUP BY report_date_1575284605702 ORDER BY `report_date_1575284605702`ASC LIMIT 1000
# response = requests.post("http://172.20.44.6:8999/sessions/" + str(sid) + '/statements', data=json.dumps(data),
#                          headers=headers)
response = requests.post("http://192.168.101.39:8999/sessions/" + str(sid) + '/statements', data=json.dumps(data),
                         headers=headers)
print(response.text)
id = response.json()['id']
print(id)
time.sleep(30)
# response = request.urlopen('http://172.20.44.6:8999/sessions/%d/statements/%d' % (sid, id))
response = request.urlopen('http://192.168.101.39:8999/sessions/%d/statements/%d' % (sid, id))
statements = json.loads(response.read())
print(statements)
stmt = statements['state']
print('getStatements %s' % (statements['state']))
if 'available' == stmt:
    print(statements)
    # print(statements['output']['data']['application/json']['data'][0])
