# -*- coding:utf-8 -*-
from db import mysqlBase
import os

__author__ = 'hubin6'

FIELD_DELIMITER = "\t"


def load_category(cnx):
    cursor = cnx.cursor()
    add_category = "INSERT INTO category (category_id, category_name) VALUES (%s, %s)"
    lib = mysqlBase.MySQLLib(cursor)
    for r in open("../data/base/category.csv", "r"):
        category_name, category_id = r.strip().split(FIELD_DELIMITER)[0:2]
        category_id = category_id[1:]
        lib.insert_record(sql=add_category, data=(category_id, category_name))
    cnx.commit()
    cursor.close


def load_district(cnx):
    cursor = cnx.cursor()
    add_district = "INSERT INTO district (district_id, district_name) VALUES (%s, %s)"
    lib = mysqlBase.MySQLLib(cursor)
    for r in open("../data/base/districts.csv", "r"):
        district_name, district_id = r.strip().split(FIELD_DELIMITER)[0:2]
        district_id = district_id[1:]
        lib.insert_record(sql=add_district, data=(district_id, district_name))
    cnx.commit()
    cursor.close


def truncate_all_shops(cnx):
    cursor = cnx.cursor()
    cursor.execute("truncate table shop")
    cursor.execute("truncate table shop_score")
    cursor.execute("truncate table shop_heat")


def load_all_shops_info(cnx):
    cursor = cnx.cursor()
    add_shop = ("INSERT INTO shop(shop_id, shop_name, address, lng, lat, category_id, phone) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)")
    cnt = 0
    shop_path = "../data/shops/"
    lib = mysqlBase.MySQLLib(cursor)
    for f in os.listdir(shop_path):
        for r in open(shop_path + f, "r"):
            cnt += 1
            shop_id, shop_name, address, lng, lat, phone_no, category_id = r.strip().split(FIELD_DELIMITER)
            lib.insert_record(sql=add_shop, data = (shop_id, shop_name, address, lng, lat, category_id, phone_no))
            if cnt % 50 == 0: cnx.commit()
        cnx.commit()
    cursor.close()


def load_all_shops_score(cnx):
    cursor = cnx.cursor()
    shop_id_list = []
    add_score = ("INSERT INTO shop_score (shop_id, avg_price, taste_score, env_score, ser_score)"
                 "VALUES (%s, %s, %s, %s, %s)")
    cnt = 0
    shop_path = "../data/scores/"
    lib = mysqlBase.MySQLLib(cursor)
    for f in os.listdir(shop_path):
        for r in open(shop_path + f, "r"):
            cnt += 1
            shop_id, avg_price, taste_score, env_score, ser_score = r.strip().split(FIELD_DELIMITER)
            if avg_price == "None":
                avg_price = None
            if shop_id in shop_id_list: continue
            shop_id_list.append(shop_id)
            lib.insert_record(sql=add_score, data=(shop_id, avg_price, taste_score, env_score, ser_score))
            if cnt % 50 == 0: cnx.commit()
        cnx.commit()
    cursor.close()


def load_all_shops_heat(cnx):
    cursor = cnx.cursor()
    shop_id_list = []
    add_heat = ("INSERT INTO shop_heat "
                "(shop_id, total_hits, today_hits, monthly_hits, weekly_hits, last_week_hits) "
                "VALUES (%s, %s, %s, %s, %s, %s)")
    cnt = 0
    shop_path = "../data/heats/"
    lib = mysqlBase.MySQLLib(cursor)
    for f in os.listdir(shop_path):
        for r in open(shop_path + f, "r"):
            cnt += 1
            shop_id, total_hits, today_hits, monthly_hits, weekly_hits, last_week_hits = r.strip().split(FIELD_DELIMITER)
            if shop_id in shop_id_list: continue
            shop_id_list.append(shop_id)
            if total_hits == "None": total_hits = None;
            if today_hits == "None": today_hits = None;
            if monthly_hits == "None": monthly_hits = None;
            if weekly_hits == "None": weekly_hits = None;
            if last_week_hits == "None": last_week_hits = None;
            lib.insert_record(sql=add_heat, data=(shop_id, total_hits, today_hits, monthly_hits, weekly_hits, last_week_hits))
            if cnt % 50 == 0: cnx.commit()
        cnx.commit()
    cursor.close()


def load_all_shops_comment(cnx):
    cursor = cnx.cursor()
    shop_id_list = []
    add_comment = ("INSERT INTO shop_comment (shop_id, comment_num) VALUES (%s, %s)")
    cnt = 0
    shop_path = "../data/comments/"
    lib = mysqlBase.MySQLLib(cursor)
    for f in os.listdir(shop_path):
        for r in open(shop_path + f, "r"):
            cnt += 1
            shop_id, comment_num = r.strip().split(FIELD_DELIMITER)
            if shop_id in shop_id_list: continue
            shop_id_list.append(shop_id)
            lib.insert_record(sql=add_comment, data=(shop_id, comment_num))
            if cnt % 50 == 0: cnx.commit()
        cnx.commit()
    cursor.close()


def load_all_shops(cnx):
    load_all_shops_info(cnx)
    load_all_shops_score(cnx)
    load_all_shops_heat(cnx)
    load_all_shops_comment(cnx)


def get_all_shops_location(cnx):
    cursor = cnx.cursor()
    lib = mysqlBase.MySQLLib(cursor)
    result = lib.fetch_result("select distinct shop_id, lng, lat from shop order by id")
    return result


