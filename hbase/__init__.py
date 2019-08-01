#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import happybase
import sensorsanalytics


class HBaseUtil(object):

    def __init__(self):
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
        conn = self.get_hbase_connection()
        t = happybase.Table(table, conn)
        scan = t.scan(row_start=row_start, row_stop=row_stop, row_prefix=row_prefix, limit=1000)
        # print(self.recourd_count)
        count = 0
        for_size = 0

        for key, value in scan:

            if for_size < 1000:
                count += 1
                # 记录用户登录事件
                distinct_id = str(dict(value)['i:phone'.encode()])
                if distinct_id == '':
                    self.zero_count += 1;
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

            for_size += 1
            self.row_stop = key

        print(self.recourd_count)
        if count < 1000:
            self.recourd_count += 1
            scan = t.scan(row_start=self.row_stop, row_stop=self.row_stop, row_prefix=row_prefix)
            for key, value in scan:
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
                # 记录用户登录事件
                distinct_id = str(dict(value)['i:phone'.encode()])

                properties = {'HuaTuOnline_exercises': float(dict(value)['i:exerciseNum'.encode()]),
                              'HuaTuOnline_prediction_score': float(dict(value)['i:predictScore'.encode()]),
                              'HuaTuOnline_accuracy': accuracy}
                # self.sa.profile_set(distinct_id, properties, is_login_id=True)
                self.l.append((distinct_id, properties))

            conn.close()
            return 0
        conn.close()
        return 1


if __name__ == '__main__':
    h = HBaseUtil()
    h.scan_table(table='scaa', row_start=None, row_stop=None, row_prefix=None)

    if h.row_stop != 0:
        while True:
            i = h.scan_table(table='scaa', row_start=h.row_stop, row_stop=None, row_prefix=None)
            if i == 0:
                break

    for tup in h.l:
        print(tup)
        h.sa.profile_set(tup[0], tup[1], is_login_id=True)

    print(h.zero_count)
    print(h.recourd_count)
