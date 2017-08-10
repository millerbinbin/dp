# -*- coding:utf-8 -*-
import sys
import json
__author__ = 'hubin6'

reload(sys)
sys.setdefaultencoding("utf-8")


class Location(object):
    def __init__(self, lng, lat):
        self.lng = lng
        self.lat = lat

    def __str__(self):
        return "lng:{0}, lat:{1}".format(self.lng, self.lat)


class TaxiRoute(object):
    def __init__(self, distance, duration, price):
        self.distance = distance
        self.duration = duration
        self.price = price

    def __str__(self):
        return "distance:{0}, duration:{1}, price:{2}".format(self.distance, self.duration, self.price)

    def to_json(self):
        return json.dumps({"distance": self.distance, "duration": self.duration, "price": self.price})


class WalkRoute(object):
    def __init__(self, distance, duration):
        self.distance = distance
        self.duration = duration
        self.type = 1

    def __str__(self):
        return 'distance:{0}, duration:{1}, type:{2}'.format(self.distance, self.duration, self.type)

    def to_json(self):
        return {"distance": self.distance, "duration": self.duration, "type": self.type}


class PublicRoute(object):
    def __init__(self, distance, duration, on_station, off_station, stop_num, name):
        self.distance = distance
        self.duration = duration
        self.on_station = on_station
        self.off_station = off_station
        self.stop_num = stop_num
        self.name = name
        self.type = 2

    def __str__(self):
        return "distance:{0}, duration:{1}, on_station:{2}, off_station:{3}, stop_num:{4}, name:{5}, type:{6}"\
            .format(self.distance, self.duration, self.on_station, self.off_station, self.stop_num, self.name, self.type)

    def to_json(self):
        return {"distance": self.distance, "duration": self.duration, "name": self.name,
                "on_station": self.on_station, "off_station": self.off_station,
                "stop_num": self.stop_num, "type": self.type}


class Route(object):
    def __init__(self, distance, duration):
        self.distance = distance
        self.duration = duration
        self.routes = []

    def __str__(self):
        return "distance:{0}, duration:{1}, routes:{2}".format(self.distance, self.duration, self.routes)

    def add_route(self, route):
        self.routes.append(route.to_json())

    def to_json(self):
        return json.dumps({"distance": self.distance, "duration": self.duration, "routes": self.routes}, ensure_ascii=False).encode('utf8')


class Shop(object):
    def __init__(self, shop_id, shop_name, address, lng, lat, phone_no, district, region, category,
                 avg_price, taste_score, env_score, ser_score,
                 total_hits, today_hits, monthly_hits, weekly_hits, last_week_hits,
                 cmt_num, star_5_num, star_4_num, star_3_num, star_2_num, star_1_num):
        self.shop_id = shop_id
        self.shop_name = shop_name
        self.address = address
        self.lng = lng
        self.lat = lat
        self.phone_no = phone_no
        self.district = district
        self.region = region
        self.category = category
        self.avg_price = avg_price
        self.taste_score = taste_score
        self.env_score = env_score
        self.ser_score = ser_score
        self.total_hits = total_hits
        self.today_hits = today_hits
        self.monthly_hits = monthly_hits
        self.weekly_hits = weekly_hits
        self.last_week_hits = last_week_hits
        self.cmt_num = cmt_num
        self.star_5_num = star_5_num
        self.star_4_num = star_4_num
        self.star_3_num = star_3_num
        self.star_2_num = star_2_num
        self.star_1_num = star_1_num

    def get_info(self):
        return ShopInfo(self.shop_id, self.shop_name, self.address, self.lng, self.lat, self.phone_no, self.district, self.region, self.category)

    def get_score(self):
        return ShopScore(self.shop_id, self.avg_price, self.taste_score, self.env_score, self.ser_score)

    def get_heat(self):
        return ShopHeat(self.shop_id, self.total_hits, self.today_hits, self.monthly_hits, self.weekly_hits, self.last_week_hits)

    def get_comment(self):
        return ShopComment(self.shop_id, self.cmt_num, self.star_5_num, self.star_4_num, self.star_3_num, self.star_2_num, self.star_1_num)


class ShopInfo(object):
    def __init__(self, shop_id, shop_name, address, lng, lat, phone_no, district, region, category):
        self.shop_id = shop_id
        self.shop_name = shop_name
        self.address = address
        self.lng = lng
        self.lat = lat
        self.phone_no = phone_no
        self.district = district
        self.region = region
        self.category = category

    def to_tuple(self):
        return self.shop_id, self.shop_name, self.address, self.lng, self.lat, self.phone_no, self.district, self.region, self.category


class ShopScore(object):
    def __init__(self, shop_id, avg_price, taste_score, env_score, ser_score):
        self.shop_id = shop_id
        self.avg_price = avg_price
        self.taste_score = taste_score
        self.env_score = env_score
        self.ser_score = ser_score

    def to_tuple(self):
        return self.shop_id, self.avg_price, self.taste_score, self.env_score, self.ser_score


class ShopHeat(object):
    def __init__(self, shop_id, total_hits, today_hits, monthly_hits, weekly_hits, last_week_hits):
        self.shop_id = shop_id
        self.total_hits = total_hits
        self.today_hits = today_hits
        self.monthly_hits = monthly_hits
        self.weekly_hits = weekly_hits
        self.last_week_hits = last_week_hits

    def to_tuple(self):
        return self.shop_id, self.total_hits, self.today_hits, self.monthly_hits, self.weekly_hits, self.last_week_hits


class ShopComment(object):
    def __init__(self, shop_id, cmt_num, star_5_num, star_4_num, star_3_num, star_2_num, star_1_num):
        self.shop_id = shop_id
        self.cmt_num = cmt_num
        self.star_5_num = star_5_num
        self.star_4_num = star_4_num
        self.star_3_num = star_3_num
        self.star_2_num = star_2_num
        self.star_1_num = star_1_num

    def to_tuple(self):
        return self.shop_id, self.cmt_num, self.star_5_num, self.star_4_num, self.star_3_num, self.star_2_num, self.star_1_num