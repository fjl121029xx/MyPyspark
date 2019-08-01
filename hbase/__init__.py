#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import happybase
import sensorsanalytics
import datetime
import time
from datetime import datetime


class HBaseUtil(object):

    def __init__(self):
        self.row_start = 0
        self.row_stop = 0
        self.recourd_count = 0
        self.l = list()
        self.SA_SERVER_URL = 'https://datax-api.huatu.com/sa?project=production'
        # 初始化一个 Consumer，用于数据发送
        # DefaultConsumer 是同步发送数据，因此不要在任何线上的服务中使用此 Consumer
        consumer = sensorsanalytics.DefaultConsumer(self.SA_SERVER_URL)
        # 使用 Consumer 来构造 SensorsAnalytics 对象
        sa = sensorsanalytics.SensorsAnalytics(consumer)
        self.sa = sa
        self.zero_count = 0
        today = datetime.today()
        self.to = today.strftime('%Y%m%d')

    # 获取一个连接
    @staticmethod
    def get_hbase_connection():
        conn = happybase.Connection(host='192.168.100.68', port=9090, timeout=None, autoconnect=True,
                                    table_prefix=None, table_prefix_separator=b'_', compat='0.98',
                                    transport='buffered', protocol='binary')
        return conn

    def query_single_line(self, table, rowkey):
        conn = self.get_hbase_connection()
        t = happybase.Table(table, conn)
        return t.row(rowkey)

    def scan_table(self, table, row_start, row_stop, row_prefix):

        self.row_start = row_start

        conn = self.get_hbase_connection()
        t = happybase.Table(table, conn)
        scan = t.scan(row_start=row_start, row_stop=row_stop, row_prefix=row_prefix, limit=1000)
        # print(self.recourd_count)
        count = 0

        for key, value in scan:

            count += 1
            # 记录用户登录事件
            distinct_id = str(dict(value)['i:phone'.encode()])
            if distinct_id == '':
                self.zero_count += 1
                continue

            self.recourd_count += 1
            grade = str(dict(value)['i:grade'.encode()])
            g_list = grade.split("_")[1:-1]

            corr = 0
            num = 0
            for r in g_list:
                corr += int(r.split(":")[1])
                num += int(r.split(":")[2])

            if num == 0:
                accuracy = 0.0
            else:
                accuracy = corr / num

            properties = {'HuaTuOnline_exercises': float(dict(value)['i:exerciseNum'.encode()]),
                          'HuaTuOnline_prediction_score': float(dict(value)['i:predictScore'.encode()]),
                          'HuaTuOnline_accuracy': accuracy}

            # self.sa.profile_set(distinct_id, properties, is_login_id=True)
            self.l.append((distinct_id, properties))
            self.row_stop = key

        if self.row_stop == self.row_start:
            return 0

        if count < 1000:
            conn.close()
            return 0
        conn.close()
        return 1


if __name__ == '__main__':
    h = HBaseUtil()
    h.scan_table(table='scaa', row_start=None, row_stop=None, row_prefix=None)

    error_list = list()
    if h.row_stop != 0:
        while True:
            i = h.scan_table(table='scaa', row_start=h.row_stop, row_stop=None, row_prefix=None)
            if i == 0:
                break

    l_len = int(len(h.l) / 1000)
    for i in range(0, l_len):
        i_s = i * 1000
        i_e = (i + 1) * 1000

        if i_e > len(h.l):
            i_e = -1

        print(i_s, i_e)
        for tup in h.l[i_s:i_e]:
            try:
                h.sa.profile_set(tup[0], tup[1], is_login_id=True)
            except sensorsanalytics.urllib2.URLError:
                error_list.append(tup)
                print(len(error_list))
            else:
                pass
        # time.sleep(3)

    print(len(error_list))
    l_len = int(len(error_list) / 1000)
    for i in range(0, l_len):
        i_s = i * 1000
        i_e = (i + 1) * 1000

        if i_e > len(error_list):
            i_e = -1

        print(i_s, i_e)
        for tup in error_list[i_s:i_e]:
            try:
                h.sa.profile_set(tup[0], tup[1], is_login_id=True)
            except sensorsanalytics.urllib2.URLError:
                pass
            else:
                pass
        time.sleep(5)

    print(h.zero_count)
    print(h.recourd_count)
