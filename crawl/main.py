# -*- coding:utf-8 -*-
from crawl import shop
from csv import csvLib
__author__ = 'hubin6'


if __name__ == '__main__':
    for i in open("../data/base/category.csv"):
        category = i.strip().split("\t")[1]
        info_list, heat_list, score_list, cmt_list = shop.crawl_all_shops_by_category(category, "taste", 8.5, 500)
        csvLib.writeRecordsToFile("../data/shops/{0}.csv".format(category), info_list, "\t")
        csvLib.writeRecordsToFile("../data/heats/{0}.csv".format(category), heat_list, "\t")
        csvLib.writeRecordsToFile("../data/scores/{0}.csv".format(category), score_list, "\t")
        csvLib.writeRecordsToFile("../data/comments/{0}.csv".format(category), cmt_list, "\t")