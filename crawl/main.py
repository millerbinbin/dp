# -*- coding:utf-8 -*-
from crawl import shop, location
from csv import csvLib
from entity import entity
from db import mysqlBase, tasks
__author__ = 'hubin6'

FIELD_DELIMITER = "\t"
CSV_BASE_DIR = "../data"

def crawl_shops():
    for i in open(CSV_BASE_DIR + "/base/category.csv"):
        category = i.strip().split("\t")[1]
        info_list, heat_list, score_list, cmt_list = shop.crawl_all_shops_by_category(category, "taste", 8.5, 5)
        csvLib.writeRecordsToFile(CSV_BASE_DIR + "/shops/{0}.csv".format(category), info_list, FIELD_DELIMITER)
        csvLib.writeRecordsToFile(CSV_BASE_DIR + "/heats/{0}.csv".format(category), heat_list, FIELD_DELIMITER)
        csvLib.writeRecordsToFile(CSV_BASE_DIR + "/scores/{0}.csv".format(category), score_list, FIELD_DELIMITER)
        csvLib.writeRecordsToFile(CSV_BASE_DIR + "/comments/{0}.csv".format(category), cmt_list, FIELD_DELIMITER)


def load_all_saved_routes():
    return {i.strip().split(FIELD_DELIMITER)[0] for i in open("../data/routes/data.csv")}


def crawl_shops_routes():
    shop_list = load_all_saved_routes()
    origin = entity.Location(lng=121.615539648, lat=31.2920292218)
    conn = mysqlBase.MySQLConnection().getConnection()
    public_routes = []
    for row in tasks.get_all_shops_location(cnx=conn):
        shop_id = str(row[0])
        if shop_id in shop_list: continue
        dest = entity.Location(lat=float(row[2]), lng=float(row[1]))
        routes = location.get_complete_route(origin, dest)
        taxi = routes.get("taxi")
        public = routes.get("public")
        if taxi is None: continue # too far to arrive
        if public is None:
            public_routes.append((shop_id, taxi.to_json(), None,))
        else:
            public_routes.append((shop_id, taxi.to_json(), public.to_json(),))
        if len(public_routes) % 10 == 0:
            print "flush data to disk..."
            csvLib.writeRecordsToFile(CSV_BASE_DIR + "/routes/data.csv", public_routes, FIELD_DELIMITER, mode="a")
            public_routes = []
    conn.close()
    csvLib.writeRecordsToFile(CSV_BASE_DIR + "/routes/data.csv", public_routes, FIELD_DELIMITER, mode="a")

if __name__ == '__main__':
    #crawl_shops()
    crawl_shops()

