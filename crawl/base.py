# -*- coding:utf-8 -*-
__author__ = 'hubin6'

from crawl import crawlLib
from csv import csvLib

SH_URL = "http://www.dianping.com/search/category/1/10"


def get_all_cbd(data):
    return [(item.text, item['href'][item['href'].rfind("/")+1:]) for item in data.find("div", id="bussi-nav", class_="nc-items").find_all("a")]


def get_all_metros(data):
    return [(item.text, item['href'][item['href'].rfind("/")+1:]) for item in data.find("div", id="metro-nav", class_="nc-items").find_all("a")]


def get_all_districts(data):
    return [(item.text, item['href'][item['href'].rfind("/")+1:]) for item in data.find("div", id="region-nav", class_="nc-items").find_all("a")]


def get_all_category(data):
    return [(item.text, item['href'][item['href'].rfind("/")+1:]) for item in data.find("div", id="classfy", class_="nc-items").find_all("a")]


def get_all_base_info(data):
    return get_all_cbd(data), get_all_metros(data), get_all_districts(data), get_all_category(data)

if __name__ == '__main__':
    content = crawlLib.Crawler(SH_URL).parseContent()
    cbd, metros, regions, category = get_all_base_info(content)
    field_delimiter = "\t"
    csvLib.writeRecordsToFile("../data/base/CBD.csv", cbd, field_delimiter)
    csvLib.writeRecordsToFile("../data/base/metros.csv", metros, field_delimiter)
    csvLib.writeRecordsToFile("../data/base/districts.csv", regions, field_delimiter)
    csvLib.writeRecordsToFile("../data/base/category.csv", category, field_delimiter)