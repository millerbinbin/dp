# -*- coding:utf-8 -*-
from crawl import WORK_DIR
import pandas as pd
import numpy as np
import os
import glob
import json
import sys
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
DETAILS_CSV = os.path.join(WORK_DIR, "data/shop_weight_details.csv")
FIELD_DELIMITER = "\t"


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
    df.columns = ["shop_id", "comment_num", "star_5_num", "star_4_num", "star_3_num", "star_2_num", "star_1_num"]
    df["good_rate"] = 100 * ((df["star_4_num"]+df["star_5_num"]) / df["comment_num"])
    df["good_rate"] = df["good_rate"].apply(lambda x: "{0:.1f}".format(x))
    return df[["shop_id", "comment_num", "good_rate"]]


def get_scores():
    all_files = glob.glob(os.path.join(SCORE_DATA_DIR, "*.csv"))
    df = pd.concat((pd.read_csv(f, header=None, sep="\t") for f in all_files))
    df.columns = ["shop_id", "avg_price", "taste_score", "env_score", "ser_score"]
    return df


def get_heats():
    all_files = glob.glob(os.path.join(HEAT_DATA_DIR, "*.csv"))
    df = pd.concat((pd.read_csv(f, header=None, sep=FIELD_DELIMITER) for f in all_files))
    df.columns = ["shop_id", "total_hits", "today_hits", "monthly_hits", "weekly_hits", "last_week_hits"]
    df["weighted_hits"] = 0.2*df["total_hits"] + 0.5*df["monthly_hits"] + 0.3*df["last_week_hits"]
    df["weighted_hits"] = df["weighted_hits"].apply(lambda x: "{0:.1f}".format(x))
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
    shop_comment_score_heat_favors_distance = pd.merge(shop_comment_score_heat_favors, routes, how="left", on="shop_id")
    shop_comment_score_heat_favors_distance_category = pd.merge(shop_comment_score_heat_favors_distance, category, how="inner", on="category_id")
    return shop_comment_score_heat_favors_distance_category


def get_weight_details():
    all_info = get_all_info()
    df = all_info[["shop_id", "shop_name", "shop_group_name", "lng", "lat",
                   "comment_num", "good_rate",
                   "avg_price", "taste_score", "env_score", "ser_score",
                   "weighted_hits", "favor_list",
                   "verse_taxi_distance", "route", "public_duration", "category_name", "category_id"
                   ]]
    return df


def save_weight_details():
    df = get_weight_details()
    import csv
    df.to_csv(DETAILS_CSV, sep=FIELD_DELIMITER, doublequote=False, quoting=csv.QUOTE_NONE)


def load_weight_details(filter_same_group):
    df = pd.read_csv(DETAILS_CSV, sep=FIELD_DELIMITER, na_values="None")
    df["shop_id"] = df["shop_id"].apply(lambda x: str(x))
    df['group_rank'] = df['taste_score'].groupby(df['shop_group_name']).rank(ascending=False)
    if filter_same_group:
        return df[df.group_rank<=1]
    return df


def get_customized_shops(details, params, order_by):
    good_rate, taste_score, comment_num, avg_price_min, avg_price_max, category = None, None, None, None, None, None
    try:
        good_rate = params['good_rate']
        taste_score = params['taste_score']
        comment_num = params['comment_num']
        avg_price_min = params['avg_price_min']
        avg_price_max = params['avg_price_max']
        category = params['category'].split(',') if params['category'] != '' else None
    except:
        pass
    condition = True
    if good_rate is not None:
        condition = condition & (details["good_rate"] >= good_rate)
    if taste_score is not None:
        condition = condition & (details["taste_score"] >= taste_score)
    if comment_num is not None:
        condition = condition & (details["comment_num"] >= comment_num)
    if avg_price_max is not None:
        condition = condition & (details["avg_price"] <= avg_price_max)
    if avg_price_min is not None:
        condition = condition & (details["avg_price"] >= avg_price_min)
    if category is not None:
        details = details[details["category_name"].isin(category)]
    if order_by is not None and order_by in ('taste_score', 'weighted_hits', 'comment_num', 'good_rate', 'verse_taxi_distance'):
        details = details.sort_values([order_by], ascending=[False])
    else:
        details = details
    details["avg_price"] = details["avg_price"].apply(lambda x: None if str(x) == "nan" else int(x))
    details["favor_list"] = details["favor_list"].apply(lambda x: "" if str(x) == "nan" else x)
    if condition is not True:
        return details[condition].loc[:, ["shop_id", "shop_name", "taste_score", 'comment_num', 'good_rate', "avg_price",
                                          "favor_list", "category_name", "lng", "lat", "route", "public_duration"]]
    else:
        return details.loc[:, ["shop_id", "shop_name", "taste_score", 'comment_num', 'good_rate', "avg_price",
                               "favor_list", "category_name", "lng", "lat", "route", "public_duration"]]


def get_distinct_shops():
    shops = get_shops()
    return shops[["shop_id", "shop_name", "address", "lng", "lat", "mainCategory_id"]].drop_duplicates().itertuples()


def get_json_data_from_df(df):
    res = [{"name": row.shop_name, "lng": row.lng, "lat": row.lat,
            "avg_price": "-" if row.avg_price is None else str(int(row.avg_price)),
            "taste_score": str(row.taste_score), "comment_num": int(row.comment_num), "good_rate": int(row.good_rate),
            "category": row.category_name, "shop_id": row.shop_id, "route": row.route, "public_duration": row.public_duration,
            "favor_list": row.favor_list
            }
            for row in df.itertuples()]
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
    hour = int(duration / 3600)
    duration -= hour * 3600
    minute = int(duration / 60)
    x = ""
    if hour > 0:
        x += "{0}时".format(hour)
    if minute > 0 :
        x += "{0}分".format(minute)
    return x


def get_random_favor_shops(all_data_info):
    favor_shops = get_favors()
    s = pd.merge(all_data_info, favor_shops, how="left", on="shop_id")
    return s[s.favors.isnull()][["shop_id", "shop_name", "taste_score", 'comment_num', 'good_rate', "avg_price",
                               "category_id", "category_name", "lng", "lat", "route", "public_duration"]]
