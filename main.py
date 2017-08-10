# -*- coding:utf-8 -*-
from crawl import shop, location
from csv import csvLib
from entity import entity
from db import mysqlBase, tasks


__author__ = 'hubin6'


FIELD_DELIMITER = "\t"









if __name__ == '__main__':
    #crawl_shops()
    shop.crawl_all_shops()

