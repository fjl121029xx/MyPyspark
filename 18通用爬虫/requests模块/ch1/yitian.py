#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import requests
from bs4 import BeautifulSoup


class TiebaSpider:

    def __init__(self, name):
        self.name = name
        self.url_temp = "http://www.jinyongwang.com/yi/{}.html"
        self.headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'}
        self.titles = []
        self.str = ""

    def get_url_list(self):
        # url_list = list()
        # for i in range(50):
        #     url_list.append(self.url_temp.format(i * 50))
        return [self.url_temp.format(i) for i in range(443, 483)]

    def parse_url(self, url):
        print(url)
        response = requests.get(url, headers=self.headers)
        s = response.content.decode()
        soup = BeautifulSoup(s, "html.parser")
        self.titles.append(str(soup.title.get_text()).split("　")[1].split("_")[0])

        self.str = ""
        for k in soup.find_all('p')[3:]:
            self.str = self.str + "\t" + k.get_text() + "\n"

        return self.str

    def save_html(self, html_str, page_num):
        file_path = "{}-第{}章-{}.txt".format(self.name, page_num, self.titles[page_num - 1])
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_str)

    def run(self):
        url_list = self.get_url_list()
        # print(url_list)
        for url in url_list:
            html_str = self.parse_url(url)
            page_num = url_list.index(url) + 1
            self.save_html(html_str, page_num)


if __name__ == '__main__':
    tieba_spider = TiebaSpider("倚天屠龙记")
    tieba_spider.run()
