#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import happybase


class HBaseUtil(object):

    def __init__(self):
        self.row_stop = 0

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
        scan = t.scan(row_start=row_start, row_stop=row_stop, row_prefix=row_prefix, limit=10)

        if len(scan) == 0:
            return 0

        for key, value in scan:
            # print(value)

            print('i:key', str(key, encoding='utf-8'))
            print('i:exerciseNum', str(dict(value)['i:exerciseNum'.encode()], encoding='utf-8'))
            print('i:phone', str(dict(value)['i:phone'.encode()], encoding='utf-8'))
            print('i:predictScore', str(dict(value)['i:predictScore'.encode()], encoding='utf-8'))
            print('i:grade', str(dict(value)['i:grade'.encode()], encoding='utf-8'))
            print("----------------------------------------")
            # print(dict(value.encode())['i:exerciseDay'])
            self.row_stop = key

        print(self.row_stop)
        return 1


if __name__ == '__main__':
    h = HBaseUtil()
    h.scan_table(table='scaa', row_start=None, row_stop=None, row_prefix=None)
    if h.row_stop != 0:
        while True:
            i = h.scan_table(table='scaa', row_start=h.row_stop, row_stop=None, row_prefix=None)
            if i == 0:
                break
