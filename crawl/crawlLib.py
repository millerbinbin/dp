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
                   'Cookie': '_hc.v=498e3bf3-bdf9-116d-1e26-8bf5bcffb775.1502175474; __utma=1.915781408.1503991937.1503991937.1503991937.1; __utmz=1.1503991937.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _lxsdk_cuid=15e3ccb3a9ac8-0c79675ea7cb2c-3a3e5f04-168000-15e3ccb3a9aad; _lxsdk=15e3ccb3a9ac8-0c79675ea7cb2c-3a3e5f04-168000-15e3ccb3a9aad; PHOENIX_ID=0a010725-15e4b85f47f-e7e0abd; s_ViewType=10; JSESSIONID=44ACA9871B277237E474D341B5B022CF; aburl=1; cy=1; cye=shanghai; __mta=46527128.1504505111749.1504505644780.1504505743169.7; _lxsdk_s=15e4b7e0d99-f36-d53-e01%7C%7C112',
                   'Host': 'www.dianping.com',
                   'Upgrade-Insecure-Requests': '1',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
                   }
        return requests.get(self.url, headers=headers).text