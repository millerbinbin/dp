# -*- coding:utf-8 -*-
__author__ = 'hubin6'
import os, sys
import urllib2
import re
from bs4 import BeautifulSoup
import math
import json
import time, datetime
import mysql.connector
from mysql.connector import errorcode

reload(sys)
sys.setdefaultencoding("utf-8")

def crawl(url):
    time.sleep(0.1)
    return urllib2.urlopen(url).read()

def getAllCBD(content):
    return {(item.text, item['href'][item['href'].rfind("/")+1:]) for item in content.find("div", id="bussi-nav", class_="nc-items").find_all("a")}

def getAllMetros(content):
    return {(item.text, item['href'][item['href'].rfind("/")+1:]) for item in content.find("div", id="metro-nav", class_="nc-items").find_all("a")}

def getAllRegions(content):
    return {(item.text, item['href'][item['href'].rfind("/")+1:]) for item in content.find("div", id="region-nav", class_="nc-items").find_all("a")}

def getAllClass(content):
    return {(item.text, item['href'][item['href'].rfind("/")+1:]) for item in content.find("div", id="classfy", class_="nc-items").find_all("a")}

def parseContent(url):
    return BeautifulSoup(crawl(url), "lxml")

def writeRecordsToFile(fileName, records, field_delimiter):
    f = open(fileName, "w")
    for row in records:
        f.write(field_delimiter.join(row[0:])+'\n')
    f.close()

def parseScoreFromContent(data):
    for i in data.find_all("span"):
        score = i.find(text=re.compile("\.\d*"))
        if i.text.find("口味") >= 0:
            taste_score = score
        if i.text.find("环境") >= 0:
            env_score = score
        if i.text.find("服务") >= 0:
            ser_score = score
    return taste_score, env_score, ser_score

def getCommentNumFromContent(data):
    try:
        t = data.find("a", class_="review-num")
        num = t.find(text=re.compile(".*\d.*"))
    except:
        num = ""
    return num

def getAvgPriceFromContent(data):
    try:
        t = data.find("a", class_="mean-price")
        num = t.find(text=re.compile("\d.*"))[1:]
    except:
        num = ""
    return num

def crawlAllShopsInfoByCategory(category, orderBy, threshold, limit_num=1000):
    prefix = "http://www.dianping.com/search/category/1/10"
    category_id = category[1:]
    heat_seq = "o2"
    rate_seq = "o3"
    taste_seq = "o5"
    env_seq = "o6"
    ser_seq = "o7"
    cmmt_seq = "o10"
    if orderBy == "taste":
        url = prefix + "/" + category + taste_seq
    elif orderBy == "rate":
        url = prefix + "/" + category + rate_seq
    elif orderBy == "heat":
        url = prefix + "/" + category + heat_seq
    elif orderBy == "env":
        url = prefix + "/" + category + env_seq
    elif orderBy == "ser":
        url = prefix + "/" + category + ser_seq
    elif orderBy == "cmmt":
        url = prefix + "/" + category + cmmt_seq
    shop_infos = []
    shop_heats = []
    shop_scores = []
    page = 0
    stop_flag = 0
    total_num = 0
    while True:
        if stop_flag == 1: break
        page += 1
        page_num = "p{0}".format(page)
        p_url = url + page_num
        print p_url
        content = parseContent(p_url)
        for shop in content.find("div", id="shop-all-list").find_all("li", class_=""):
            link = shop.find("div", class_="pic")
            shop_name = link.img['alt']
            shop_id = link.a['href'][link.a['href'].rfind('/')+1:]
            comment = shop.find("div", class_="comment")
            avg_price = getAvgPriceFromContent(comment)
            #cmmt_num = getCommentNumFromContent(comment)
            address = shop.find("div", class_="tag-addr").find("span", class_="addr").text
            scores = shop.find("span", class_="comment-list")
            taste_score, env_score, ser_score = parseScoreFromContent(scores)
            phoneNo, hits, monthlyHits, weeklyHits, todayHits, prevWeeklyHits, glat, glng = getShopDetails(shop_id)
            total_num += 1
            if float(taste_score) < threshold or total_num > limit_num:
                stop_flag = 1
                break
            shop_infos.append((shop_id, shop_name, address, glng, glat, category_id, phoneNo ))
            shop_scores.append((shop_id, avg_price, taste_score, env_score, ser_score))
            shop_heats.append((shop_id, hits, monthlyHits, weeklyHits, todayHits, prevWeeklyHits))
    return shop_infos, shop_scores, shop_heats

def getGeoFromAddr(address):
    app_key = "9MhIHvmWZHiQkEEoCIxKXGYkXbKS5hrq"
    url = "http://api.map.baidu.com/geocoder/v2/?city=上海市&address={0}&ak={1}&output=json".format(address, app_key)
    obj = json.loads(crawl(url))
    status = obj['status']
    if status == 0:
        result = obj['result']
    elif status == 1:
        url = "http://api.map.baidu.com/place/v2/suggestion?region=上海市&city_limit=true&query={0}&ak={1}&output=json".format(address, app_key)
        result = json.loads(crawl(url))['result'][0]
    loc = result['location']
    return "{0},{1}".format(loc['lat'], loc['lng'])

def getPath(origin, destination):
    app_key = "9MhIHvmWZHiQkEEoCIxKXGYkXbKS5hrq"
    url = "http://api.map.baidu.com/direction/v2/transit?tactics_incity=4&origin={0}&destination={1}&ak={2}".format(origin, destination, app_key)
    routes = json.loads(crawl(url))['result']['routes']
    return routes

def getVehicleNameByType(type_id):
    if type_id == 3:
        return "metro/bus"
    if type_id == 5:
        return "walk"

def getFormattedTimeBySeconds(seconds):
    hour = seconds / 3600
    min = (seconds-hour*3600) / 60
    sec = (seconds-hour*3600-min*60) % 60
    str = ""
    if hour > 0:
        str = "{0}小时".format(hour)
    if min > 0:
        str += "{0}分钟".format(min)
    if sec > 0:
        str += "{0}秒".format(sec)
    return str

def getCompleteRoutes(origin, destination):
    rec_route = getPath(origin, destination)[0]
    steps = rec_route['steps']
    total_distance = rec_route['distance']
    total_duration = getFormattedTimeBySeconds(rec_route['duration'])
    #routes.append("总路程{0:.1f}km, 耗时：{1}".format(total_distance/1000.0, getFormattedTimeBySeconds(total_duration)))
    routes = '['
    for t in steps:
        step = t[0]
        vehicle_info = step['vehicle_info']
        distance = step['distance']
        duration = getFormattedTimeBySeconds(step['duration'])
        if getVehicleNameByType(vehicle_info['type']) == "metro/bus":
            on_station = vehicle_info['detail']['on_station']
            off_station = vehicle_info['detail']['off_station']
            stop_num = vehicle_info['detail']['stop_num']
            name = vehicle_info['detail']['name']
            r = str(Route(distance, duration, on_station, off_station, stop_num, name, "metro/bus")) + ','
            routes += r
            #routes.append(" ▷从 {0} 乘坐{1}到 {2} 下，共{3}站，耗时{4}".format(on_station, name, off_station, stop_num, duration))
        else:
            if distance > 50:
                r = str(Route(distance, duration, "", "", 0, "", "walk")) + ','
                routes += r
                #routes.append(" ▷行走路程{0}m, 耗时:{1}".format(distance, duration))
    routes = routes[:-1] + ']'
    complete_routes = r'{{"distance":{0},"duration":"{1}","routes":{2}}}'.format(total_distance, total_duration, routes)
    return complete_routes

def crawlAllShops():
    for r in open("base/category.txt", "r"):
        info = r.strip().split(" ")
        category = info[1]
        shops, scores, heats = crawlAllShopsInfoByCategory(category, "taste", 8.5, 250)
        writeRecordsToFile(fileName="shops/" + category, records=shops, field_delimiter="\t")
        writeRecordsToFile(fileName="scores/" + category, records=scores, field_delimiter="\t")
        writeRecordsToFile(fileName="heats/" + category, records=heats, field_delimiter="\t")

def crawlAllShopsRoutesInfo():
    origin = getGeoFromAddr("金高路988弄")
    for r in open("hotpot", "r"):
        info = r.strip().split(",")
        name = info[0]
        addr = info[6]
        destination = getGeoFromAddr(addr)
        print "{0}||{1}||{2}".format(name, addr, getCompleteRoutes(origin, destination))

def getShopDetails(shopId):
    url = "http://www.dianping.com/ajax/json/shopfood/wizard/BasicHideInfoAjaxFP?_nr_force=1502177990602&shopId={0}".format(shopId)
    details = json.loads(crawl(url))['msg']['shopInfo']
    todayHits = str(details['todayHits'])
    monthlyHits = str(details['monthlyHits'])
    weeklyHits = str(details['weeklyHits'])
    glat = str(details['glat'])
    glng = str(details['glng'])
    hits = str(details['hits'])
    phoneNo = str(details['phoneNo'])
    prevWeeklyHits = str(details['prevWeeklyHits'])
    return phoneNo, hits, monthlyHits, weeklyHits, todayHits, prevWeeklyHits, glat, glng

def getMySQLConnection():
    config = {
        'user': 'dp_user',
        'password': 'dp_user',
        'host': 'localhost',
        'port': 3306,
        'database': 'dp'
    }
    cnx = mysql.connector.connect(**config)
    return cnx

class Route(object):
    def __init__(self, distance, duration, on_station, off_station, stop_num, name, type):
        self.distance = distance
        self.duration = duration
        self.on_station = on_station
        self.off_station = off_station
        self.stop_num = stop_num
        self.name = name
        self.type = type
    def __str__(self):
        return '{{"distance":"{0}","duration":"{1}","on_station":"{2}","off_station":"{3}","stop_num":{4},"name":"{5}",' \
                            '"type":"{6}"}}'.format(self.distance, self.duration, self.on_station, self.off_station, self.stop_num, self.name, self.type)

def loadShopsByCategory(category, cnx):
    cursor = cnx.cursor()
    category_id = category[1:]
    # cursor.execute("delete from shop where category_id = {0}".format(category_id))
    # cursor.execute("delete from shop_score where category_id = {0}".format(category_id))
    # cursor.execute("delete from shop_heat where category_id = {0}".format(category_id))
    cnx.commit()
    add_shop = ("INSERT INTO shop"
               "(shop_id, shop_name, address, phone, lat, lng, category_id) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s)")
    add_shop_score = ("INSERT INTO shop_score "
               "(shop_id, avg_price, taste_score, env_score, ser_score) "
               "VALUES (%s, %s, %s, %s, %s)")
    add_shop_heat = ("INSERT INTO shop_heat "
               "(shop_id, hits, monthlyHits, weeklyHits, todayHits, prevWeeklyHits) "
               "VALUES (%s, %s, %s, %s, %s, %s)")
    cnt = 0
    for r in open("shops/"+category, "r"):
        cnt += 1
        info = r.strip().split('\t')
        shop_id, shop_name, address, lat, lng, phoneNo = info[0:6]
        data = (shop_id, shop_name, address, phoneNo, lat, lng, category_id)
        cursor.execute(add_shop, data)
        if cnt % 50 == 0: cnx.commit()
    cnx.commit()
    for r in open("scores/"+category, "r"):
        cnt += 1
        info = r.strip().split('\t')
        shop_id, avg_price, taste_score, env_score, ser_score = info[0:5]
        if avg_price == "": avg_price = None
        data = (shop_id, avg_price, taste_score, env_score, ser_score)
        cursor.execute(add_shop_score, data)
        if cnt % 50 == 0: cnx.commit()
    cnx.commit()
    for r in open("heats/"+category, "r"):
        cnt += 1
        info = r.strip().split('\t')
        shop_id, hits, monthlyHits, weeklyHits, todayHits, prevWeeklyHits = info[0:6]
        if hits=="None": hits = None;
        if monthlyHits == "None": monthlyHits = None;
        if weeklyHits == "None": weeklyHits = None;
        if todayHits == "None": todayHits = None;
        if prevWeeklyHits == "None": prevWeeklyHits = None;
        data = (shop_id, hits, monthlyHits, weeklyHits, todayHits, prevWeeklyHits)
        cursor.execute(add_shop_heat, data)
        if cnt % 50 == 0: cnx.commit()
    cnx.commit()
    cursor.close()

def loadAllShops(cnx):
    for r in open("base/category.txt", "r"):
        info = r.strip().split(" ")
        category = info[1]
        loadShopsByCategory(category, cnx)

if __name__ == '__main__':
    cnx = getMySQLConnection()
    loadAllShops(cnx)
    cnx.close()



