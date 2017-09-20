# -*- coding:utf-8 -*-
from main import WORK_DIR
import pandas as pd
import numpy as np
import os
import glob
import json
import math
import sys
import redis

reload(sys)
sys.setdefaultencoding("utf-8")

BASE_DATA_DIR = os.path.join(WORK_DIR, "data/base")
REGION_CSV = os.path.join(BASE_DATA_DIR, "regions.csv")
DISTRICT_CSV = os.path.join(BASE_DATA_DIR, "districts.csv")
CATEGORY_CSV = os.path.join(BASE_DATA_DIR, "category.csv")
SUBCATEGORY_CSV = os.path.join(BASE_DATA_DIR, "subcategory.csv")
SHOP_DATA_DIR = os.path.join(BASE_DATA_DIR, "../shops")
LOCATION_DATA_DIR = os.path.join(BASE_DATA_DIR, "../location")
COMMENT_DATA_DIR = os.path.join(BASE_DATA_DIR, "../comments")
HEAT_DATA_DIR = os.path.join(BASE_DATA_DIR, "../heats")
SCORE_DATA_DIR = os.path.join(BASE_DATA_DIR, "../scores")
ROUTE_DATA_DIR = os.path.join(BASE_DATA_DIR, "../routes")
FAVOR_DATA_DIR = os.path.join(BASE_DATA_DIR, "../favorite")
DETAILS_CSV_ZIP = os.path.join(WORK_DIR, "main/shop_details.gz")
FIELD_DELIMITER = "\t"

redis_host = os.getenv("REDIS_PORT_6379_TCP_ADDR") if os.getenv("REDIS_PORT_6379_TCP_ADDR") != None else os.getenv("REDIS_HOST")
redis_port = int(os.getenv("REDIS_PORT_6379_TCP_PORT") if os.getenv("REDIS_PORT_6379_TCP_PORT") != None else os.getenv("REDIS_PORT"))
redis_password = os.getenv("REDIS_PASSWORD")
r = redis.Redis(host=redis_host, port=redis_port, password=redis_password)


def get_region_table():
    regions = get_regions()
    districts = get_districts()
    region_table = {}
    for region in regions.itertuples():
        region_table[region.region_name] = (region.region_id, region.district_id)
    for district in districts.itertuples():
        region_table[district.district_name] = (None, district.district_id)
    return region_table


def get_category_table():
    category = get_category()
    subcategory = get_subcategory()
    category_table = {}
    for sub in subcategory.itertuples():
        category_table[sub.subcategory_name] = (sub.subcategory_id, sub.category_id)
    for cate in category.itertuples():
        category_table[cate.category_name] = (None, cate.category_id)
    return category_table


def get_districts():
    df = pd.read_csv(DISTRICT_CSV, header=None, sep=FIELD_DELIMITER)
    df.columns = ["district_name", "district_code", "district_id"]
    return df


def get_regions():
    df = pd.read_csv(REGION_CSV, header=None, sep=FIELD_DELIMITER)
    df.columns = ["region_name", "region_code", "region_id", "district_id"]
    return df


def get_category():
    df = pd.read_csv(CATEGORY_CSV, header=None, sep=FIELD_DELIMITER)
    df.columns = ["category_name", "category_code", "category_id"]
    return df


def get_subcategory():
    df = pd.read_csv(SUBCATEGORY_CSV, header=None, sep=FIELD_DELIMITER)
    df.columns = ["subcategory_name", "subcategory_code", "subcategory_id", "category_id"]
    return df


def get_shops():
    all_files = glob.glob(os.path.join(SHOP_DATA_DIR, "*.csv"))
    df = pd.concat((pd.read_csv(f, header=None, sep=FIELD_DELIMITER) for f in all_files))
    df.columns = ["shop_id", "shop_name", "shop_group_name", "address", "lng", "lat", "phone", "district_id", "region_id", "category_id", "subcategory_id"]
    shops = df[["shop_id", "shop_name", "shop_group_name", "address", "lng", "lat", "category_id", "subcategory_id"]]
    locations = get_locations()
    df = pd.merge(shops, locations, how="left", on="shop_id")
    df["lng"] = df["lng_baidu"].apply(lambda x: "{0:.6f}".format(x))
    df["lat"] = df["lat_baidu"].apply(lambda x: "{0:.6f}".format(x))
    df["mainCategory_id"] = df.apply(
        lambda x: x['category_id'] if x['subcategory_id'] == "None" else x['subcategory_id'], axis=1)
    df["shop_group_name"] = df.apply(
        lambda x: x['shop_name'] if x['shop_group_name'] == "None" else x['shop_group_name'], axis=1)
    return df[["shop_id", "shop_name", "shop_group_name", "address", "lng", "lat", "category_id", "mainCategory_id"]]


def get_locations():
    all_files = glob.glob(os.path.join(LOCATION_DATA_DIR, "*.csv"))
    df = pd.concat((pd.read_csv(f, header=None, sep=FIELD_DELIMITER) for f in all_files))
    df.columns = ["shop_id", "lng_baidu", "lat_baidu"]
    return df


def get_comments():
    all_files = glob.glob(os.path.join(COMMENT_DATA_DIR, "*.csv"))
    df = pd.concat((pd.read_csv(f, header=None, sep=FIELD_DELIMITER, na_filter=True, na_values="None") for f in all_files))
    df.columns = ["shop_id", "first_cmt_date", "comment_num", "star_5_num", "star_4_num", "star_3_num", "star_2_num", "star_1_num"]
    df["good_rate"] = 100 * ((df["star_4_num"]+df["star_5_num"]) / df["comment_num"])
    df["good_rate"] = df["good_rate"].apply(lambda x: "{0:.1f}".format(x))
    return df[["shop_id", "first_cmt_date", "comment_num", "good_rate"]]


def get_scores():
    all_files = glob.glob(os.path.join(SCORE_DATA_DIR, "*.csv"))
    df = pd.concat((pd.read_csv(f, header=None, sep="\t") for f in all_files))
    df.columns = ["shop_id", "avg_price", "taste_score", "env_score", "ser_score"]
    return df


def get_heats():
    all_files = glob.glob(os.path.join(HEAT_DATA_DIR, "*.csv"))
    df = pd.concat((pd.read_csv(f, header=None, sep=FIELD_DELIMITER) for f in all_files))
    df.columns = ["shop_id", "total_hits", "today_hits", "monthly_hits", "weekly_hits", "last_week_hits"]
    df["weighted_hits"] = df.apply(lambda x: "{0:.1f}".format(
                                    0.2 * (0 if str(x["total_hits"])=="None" else int(x["total_hits"])) +
                                    0.5 * (0 if str(x["monthly_hits"])=="None" else int(x["monthly_hits"])) +
                                    0.3 * (0 if str(x["last_week_hits"])=="None" else int(x["last_week_hits"]))), axis=1)

    return df[["shop_id", "total_hits", "monthly_hits", "last_week_hits", "weighted_hits"]]


def get_routes():
    all_files = glob.glob(os.path.join(ROUTE_DATA_DIR, "*.csv"))
    df = pd.concat((pd.read_csv(f, header=None, sep=FIELD_DELIMITER, na_values="None") for f in all_files))
    df.columns = ["shop_id", "taxi_route", "public_route"]
    df['verse_taxi_distance'] = df['taxi_route'].apply(lambda x: 0-int(json.loads(x)['distance']))
    df['route'] = df['public_route'].apply(get_route_info)
    df['public_duration'] = df['public_route'].apply(get_duration)
    return df[["shop_id", "verse_taxi_distance", "route", "public_duration"]]


def get_favors():
    all_files = glob.glob(os.path.join(FAVOR_DATA_DIR, "*.csv"))
    df = pd.concat((pd.read_csv(f, header=None, sep=FIELD_DELIMITER, na_values="None") for f in all_files))
    df.columns = ["shop_id", "favors"]
    df["favor_list"] = df["favors"].apply(lambda x: ",".join([item['dishTagName'] for item in json.loads(x)]))
    return df[["shop_id", "favor_list"]]


def get_all_info():
    shops = get_shops()
    comments = get_comments()
    scores = get_scores()
    heats = get_heats()
    routes = get_routes()
    category = get_category()
    favors = get_favors()
    shop_comment = pd.merge(shops, comments, how="inner", on="shop_id")
    shop_comment_score = pd.merge(shop_comment, scores, how="inner", on="shop_id")
    shop_comment_score_heat = pd.merge(shop_comment_score, heats, how="inner", on="shop_id")
    shop_comment_score_heat_favors = pd.merge(shop_comment_score_heat, favors,how="inner",on="shop_id")
    shop_comment_score_heat_favors_distance_category = pd.merge(shop_comment_score_heat_favors, category, how="inner", on="category_id")
    return shop_comment_score_heat_favors_distance_category


def get_weight_details():
    all_info = get_all_info()
    df = all_info[["shop_id", "shop_name", "shop_group_name", "lng", "lat",
                   "first_cmt_date", "comment_num", "good_rate",
                   "avg_price", "taste_score", "env_score", "ser_score",
                   "weighted_hits", "favor_list","category_name", "category_id"
                   ]]
    return df


def save_weight_details():
    df = get_weight_details()
    import csv
    df.to_csv(DETAILS_CSV_ZIP, sep=FIELD_DELIMITER, doublequote=False, quoting=csv.QUOTE_NONE, compression="gzip")


def load_weight_details(filter_same_group=False, filter_new_shop=True):
    key = "all_shop_info,{0},{1}".format(filter_same_group, filter_new_shop)
    if r.get(key) is not None:
        all_shop_info = pd.read_msgpack(r.get(key))
    else:
        df = pd.read_csv(DETAILS_CSV_ZIP, sep=FIELD_DELIMITER, na_values="None", compression="gzip")
        df["shop_id"] = df["shop_id"].apply(lambda x: str(x))
        df['group_rank'] = df['taste_score'].groupby(df['shop_group_name']).rank(ascending=False)
        df["avg_price"] = df.apply(
            lambda x: "" if str(x["avg_price"]) == "nan" or str(x["avg_price"]) == "" else int(x["avg_price"]), axis=1)
        df["favor_list"] = df.apply(lambda x: "" if str(x["favor_list"]) == "nan" else x["favor_list"], axis=1)
        if filter_new_shop:
            df = df[df.first_cmt_date <= '2017-06-01']
        if filter_same_group:
            df = df[df.group_rank < 2]
        all_shop_info = df
        r.setex(key, all_shop_info.to_msgpack(compress='zlib', encoding='utf-8'), time=3600*12)

    key = "all_category,{0},{1}".format(filter_same_group, filter_new_shop)
    if r.get(key) is not None:
        all_category = pd.read_msgpack(r.get(key))
    else:
        all_category = all_shop_info[["category_name"]].drop_duplicates()
        r.setex(key, all_category.to_msgpack(compress='zlib', encoding='utf-8'), time=3600*12)

    return all_shop_info, all_category


def get_customized_shops(params):
    filter_same_group = True if params['filter_same_group'].lower() == "true" else False
    filter_new_shop = True if params['filter_new_shop'].lower() == "true" else False
    details = load_weight_details(filter_same_group=filter_same_group, filter_new_shop=filter_new_shop)[0]
    if r.get(params) is None:
        taste_score, comment_num, avg_price_min, avg_price_max, category, position, query = \
            None, None, None, None, None, None, None
        try:
            taste_score = params['taste_score']
            comment_num = params['comment_num']
            avg_price_min = params['avg_price_min']
            avg_price_max = params['avg_price_max']
            query = params['query']
            position = params["position"]
            category = params['category'].split(',') if params['category'] != '' else None
            order_by = params['order_by']
            page = params['page']
            limit = params['limit']
        except Exception:
            pass
        condition = True
        if taste_score is not None:
            condition = condition & (details["taste_score"] >= taste_score)
        if comment_num is not None:
            condition = condition & (details["comment_num"] >= comment_num)
        if avg_price_max is not None:
            condition = condition & (details["avg_price"] <= avg_price_max)
        if avg_price_min is not None:
            condition = condition & (details["avg_price"] >= avg_price_min)
        if category is not None:
            condition = condition & (details["category_name"].isin(category))
        if condition is not True:
            details = details[condition]
        if query is not None:
            details = details[details.shop_group_name.str.contains(query) | details.favor_list.str.contains(query)]
        if position is not None:
            lat = float(position.split(",")[0])
            lng = float(position.split(",")[1])
            details["distance"] = details.apply(
                lambda x: calc_earth_distance({"lat": x["lat"], "lng": x["lng"]}, {"lat": lat, "lng": lng}),
                axis=1)
            details = details[details.distance <= 5]
        if order_by is not None and order_by in ('taste_score', 'weighted_hits', 'comment_num', 'good_rate'):
            details = details.sort_values([order_by], ascending=[False])
        result = details.loc[:, ["shop_id", "shop_name", "taste_score", "env_score", "comment_num", "good_rate", "avg_price",
                                              "favor_list", "category_name", "lng", "lat"]].iloc[(page - 1) * limit:page * limit]
        r.setex(params, result.to_msgpack(compress='zlib', encoding='utf-8'), time=3600*12)
    else:
        print "Existing: {0}".format(params)
        result = pd.read_msgpack(r.get(params))
    return result


def get_distinct_shops():
    shops = get_shops()
    return shops[["shop_id", "shop_name", "address", "lng", "lat", "mainCategory_id"]].drop_duplicates().itertuples()


def get_shops_json_from_df(df):
    res = [{"name": row.shop_name, "lng": row.lng, "lat": row.lat,
            "avg_price": "-" if row.avg_price=="" else str(int(row.avg_price)),
            "taste_score": str(row.taste_score), "env_score": str(row.env_score), "comment_num": int(row.comment_num), "good_rate": int(row.good_rate),
            "category": row.category_name, "shop_id": row.shop_id, "favor_list": row.favor_list
            }
            for row in df.itertuples()]
    return json.dumps(res, ensure_ascii=False).encode("utf-8")


def get_category_json_from_df(df):
    res = [{"category": row.category_name} for row in df.itertuples()]
    return json.dumps(res, ensure_ascii=False).encode("utf-8")


def get_duration(public_route):
    if public_route is np.NAN: return "-"
    duration = get_time_str(json.loads(public_route)["duration"])
    return duration


def get_route_info(public_route):
    if public_route is np.NAN: return "-"
    routes = json.loads(public_route)["routes"]
    route_set = ""
    for route in routes:
        if route["type"] == 1:
            pass
        elif route["type"] == 2:
            if route_set == "":
                route_set += "{0}->{1}({2})".format(route["on_station"], route["off_station"], route["name"])
            else:
                route_set += "->{0}({1})".format(route["off_station"], route["name"])
    return route_set


def get_time_str(duration):
    duration = int(duration)
    hour = int(duration / 3600)
    duration -= hour * 3600
    minute = int(duration / 60)
    x = ""
    if hour > 0:
        x += "{0}小时".format(hour)
    if minute > 0 :
        x += "{0}分".format(minute)
    if hour==0 and minute==0:
        return "{0}秒".format(duration)
    return x


def get_random_favor_shops(all_data_info):
    favor_shops = get_favors()
    s = pd.merge(all_data_info, favor_shops, how="left", on="shop_id")
    return s[s.favors.isnull()][["shop_id", "shop_name", "taste_score", 'comment_num', 'good_rate', "avg_price",
                               "category_id", "category_name", "lng", "lat"]]


def calc_earth_distance(origin, dest):
    C = math.sin(origin['lat']) * math.sin(dest['lat']) + math.cos(origin['lng'] - dest['lng']) * math.cos(origin['lat']) * math.cos(
        dest['lat'])
    R = 6371.004
    Pi = 3.1415926
    distance = R * math.acos(C) * Pi / 180
    return float("{0:.2f}".format(distance))