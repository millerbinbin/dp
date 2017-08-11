# -*- coding:utf-8 -*-
import urllib2
import json
from bs4 import BeautifulSoup
import requests

__author__ = 'hubin6'


class Crawler(object):
    def __init__(self, url):
        self.url = url

    def crawl(self):
        return urllib2.urlopen(self.url).read()

    def parse_content(self, mode="normal"):
        if mode == "complex":
            return BeautifulSoup(self.auth_crawl(), "lxml")
        return BeautifulSoup(self.crawl(), "lxml")

    def to_json(self):
        return json.loads(self.crawl())

    def auth_crawl(self):
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate',
                   'Accept-Language': 'en-US,en;q=0.8',
                   'Connection': 'keep-alive',
                   'Cookie': '_hc.v=498e3bf3-bdf9-116d-1e26-8bf5bcffb775.1502175474; '
                             '_lxsdk_cuid=15dcaa9f195c8-01acd2d00fe066-333f5902-168000-15dcaa9f196c8;'
                             '_lxsdk=15dcaa9f195c8-01acd2d00fe066-333f5902-168000-15dcaa9f196c8; '
                             'PHOENIX_ID=0a010725-15dcaad1966-497eb1d; '
                             's_ViewType=10; '
                             '__mta=250044345.1502343729701.1502352611764.1502352707776.6; '
                             'JSESSIONID=1E6FAE3A93548EF549CF3047C8A2552E; '
                             'aburl=1; '
                             'cy=1; '
                             'cye=shanghai; '
                             '_lxsdk_s=15dcb31452f-3db-0ea-429%7C%7C47',
                   'Host': 'www.dianping.com',
                   'Upgrade-Insecure-Requests': '1',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
                   }
        return requests.get(self.url, headers=headers).text

if __name__ == '__main__':
    print Crawler("http://www.dianping.com/shop/19612173").parse_content()