# -*- coding:utf-8 -*-
from db import mysqlBase, dbinit
import os
import json

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
    cursor.close()
    print "loading category data finished..."


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
    print "loading district data finished..."


def load_region(cnx):
    cursor = cnx.cursor()
    add_region = "INSERT INTO region (region_id, region_name, district_id) VALUES (%s, %s, %s)"
    lib = mysqlBase.MySQLLib(cursor)
    for r in open("../data/base/regions.csv", "r"):
        region_name, region_id, district_id = r.strip().split(FIELD_DELIMITER)[0:3]
        region_id = region_id[1:]
        district_id = district_id[1:]
        lib.insert_record(sql=add_region, data=(region_id, region_name, district_id))
    cnx.commit()
    cursor.close()
    print "loading region data finished..."



def truncate_all_base(cnx):
    cursor = cnx.cursor()
    cursor.execute("truncate table category")
    cursor.execute("truncate table district")
    cursor.execute("truncate table region")


def truncate_all_shops(cnx):
    cursor = cnx.cursor()
    cursor.execute("truncate table shop")
    cursor.execute("truncate table shop_score")
    cursor.execute("truncate table shop_heat")
    cursor.execute("truncate table shop_comment")
    cursor.execute("truncate table shop_route")


def load_all_shops_info(cnx):
    cursor = cnx.cursor()
    add_shop = ("INSERT INTO shop(shop_id, shop_name, address, lng, lat, district_id, region_id, category_id, phone) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
    cnt = 0
    shop_path = "../data/shops/"
    lib = mysqlBase.MySQLLib(cursor)
    for f in os.listdir(shop_path):
        for r in open(shop_path + f, "r"):
            cnt += 1
            shop_id, shop_name, address, lng, lat, phone_no, district_id, region_id, category_id = r.strip().split(FIELD_DELIMITER)
            if district_id == "None": district_id = None
            if region_id == "None": region_id = None
            lib.insert_record(sql=add_shop, data = (shop_id, shop_name, address, lng, lat, district_id, region_id, category_id, phone_no))
            if cnt % 50 == 0: cnx.commit()
        cnx.commit()
    cursor.close()
    print "loading shops data finished..."


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
    print "loading scores data finished..."


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
    print "loading heat data finished..."


def load_all_shops_comment(cnx):
    cursor = cnx.cursor()
    shop_id_list = []
    add_comment = ("INSERT INTO shop_comment "
                   "(shop_id, comment_num, star_5_num, star_4_num, star_3_num, star_2_num, star_1_num) "
                   "VALUES (%s, %s, %s, %s, %s, %s, %s)")
    cnt = 0
    shop_path = "../data/comments/"
    lib = mysqlBase.MySQLLib(cursor)
    for f in os.listdir(shop_path):
        for r in open(shop_path + f, "r"):
            cnt += 1
            shop_id, comment_num, star_5_num, star_4_num, star_3_num, star_2_num, star_1_num = r.strip().split(FIELD_DELIMITER)
            if shop_id in shop_id_list: continue
            shop_id_list.append(shop_id)
            lib.insert_record(sql=add_comment, data=(shop_id, comment_num, star_5_num, star_4_num, star_3_num, star_2_num, star_1_num))
            if cnt % 50 == 0: cnx.commit()
        cnx.commit()
    cursor.close()
    print "loading comment data finished..."


def load_all_shops_route(cnx):
    cursor = cnx.cursor()
    shop_id_list = []
    add_route = ("INSERT INTO shop_route "
                   "(shop_id, taxi_duration, taxi_distance, taxi_price, public_duration, public_distance, routes) "
                   "VALUES (%s, %s, %s, %s, %s, %s, %s)")
    cnt = 0
    shop_path = "../data/routes/"
    lib = mysqlBase.MySQLLib(cursor)
    for f in os.listdir(shop_path):
        for r in open(shop_path + f, "r"):
            cnt += 1
            shop_id, taxi_route, public_route = r.strip().split(FIELD_DELIMITER)
            if shop_id in shop_id_list: continue
            taxi_json = json.loads(taxi_route)
            taxi_duration = taxi_json['duration']
            taxi_distance = taxi_json['distance']
            taxi_price = taxi_json['price']
            if public_route == "None":
                public_duration = None
                public_distance = None
                public_routes = None
            else:
                public_json = json.loads(public_route)
                public_duration = public_json['duration']
                public_distance = public_json['distance']
                public_routes = json.dumps(public_json['routes'], ensure_ascii=False).encode('utf8')
            shop_id_list.append(shop_id)
            lib.insert_record(sql=add_route, data=(shop_id, taxi_duration, taxi_distance, taxi_price, public_duration, public_distance, public_routes))
            if cnt % 50 == 0: cnx.commit()
        cnx.commit()
    cursor.close()
    print "loading routes data finished..."


def load_all_shops(cnx):
    load_all_shops_info(cnx)
    load_all_shops_score(cnx)
    load_all_shops_heat(cnx)
    load_all_shops_comment(cnx)
    load_all_shops_route(cnx)


def load_all_base(cnx):
    load_category(cnx)
    load_district(cnx)
    load_region(cnx)


def get_all_shops_location(cnx):
    cursor = cnx.cursor()
    lib = mysqlBase.MySQLLib(cursor)
    result = lib.fetch_result("select distinct shop_id, lng, lat from shop order by id")
    return result


def get_region_table():
    cnx = mysqlBase.MySQLConnection().get_connection()
    lib = mysqlBase.MySQLLib(cnx.cursor())
    region_table = {}
    for item in lib.fetch_result("select distinct region_id, region_name, district_id from region order by id"):
        region_table[item[1]] = (item[0], item[2])
    for item in lib.fetch_result("select distinct district_id, district_name from district order by id"):
        region_table[item[1]] = (None, item[0])
    return region_table


def get_all_shops():
    cnx = mysqlBase.MySQLConnection().get_connection()
    cursor = cnx.cursor()
    lib = mysqlBase.MySQLLib(cursor)
    result = lib.fetch_result("select distinct shop_id from shop order by id")
    return result
"""
SELECT distinct s.shop_name, s.address, 
ca.category_name, d.district_name, re.region_name,  
e.avg_price, e.taste_score, e.env_score, e.ser_score,
h.last_week_hits, h.today_hits, h.monthly_hits,
c.comment_num, 
r.taxi_duration, r.taxi_price, r.public_duration
FROM dp.shop s
left join dp.shop_score e on s.shop_id = e.shop_id
left join dp.shop_heat h on s.shop_id = h.shop_id
left join dp.shop_comment c on s.shop_id = c.shop_id
left join dp.shop_route r on s.shop_id = r.shop_id
left join dp.category ca on s.category_id = ca.category_id
left join dp.region re on s.region_id = re.region_id
left join dp.district d on s.district_id = d.district_id
where taste_score >= 9 
and category_name in('蟹宴', '日本菜', '海鲜')
order by taste_score
"""

if __name__ == '__main__':
    conn = mysqlBase.MySQLConnection().get_connection()
    dbinit.init_all_tables(cnx=conn)
    truncate_all_base(cnx=conn)
    load_all_base(cnx=conn)
    truncate_all_shops(cnx=conn)
    load_all_shops(cnx=conn)
