import urllib2
import json
from bs4 import BeautifulSoup
import time
# -*- coding:utf-8 -*-
__author__ = 'hubin6'


class Crawler(object):
    def __init__(self, url):
        self.url = url

    def crawl(self):
        #time.sleep(0.1)
        return urllib2.urlopen(self.url).read()

    def parseContent(self):
        return BeautifulSoup(self.crawl(), "lxml")

    def toJson(self):
        return json.loads(self.crawl())