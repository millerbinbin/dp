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
SHOP_DATA_DIR = os.path.join(BASE_DATA_DIR, "../shops")
LOCATION_DATA_DIR = os.path.join(BASE_DATA_DIR, "../location")
COMMENT_DATA_DIR = os.path.join(BASE_DATA_DIR, "../comments")
HEAT_DATA_DIR = os.path.join(BASE_DATA_DIR, "../heats")
SCORE_DATA_DIR = os.path.join(BASE_DATA_DIR, "../scores")
ROUTE_DATA_DIR = os.path.join(BASE_DATA_DIR, "../routes")
DETAILS_CSV = os.path.join(BASE_DATA_DIR, "../shop_weight_details.csv")
FIELD_DELIMITER = "\t"


def get_regions():
    df = pd.read_csv(REGION_CSV, header=None, sep=FIELD_DELIMITER)
    df.columns = ["region_name","region_id","district_id"]
    df["region_id"] = df["region_id"].apply(lambda x: x[1:])
    df["district_id"] = df["district_id"].apply(lambda x: x[1:])
    return df


def get_districts():
    df = pd.read_csv(DISTRICT_CSV, header=None, sep=FIELD_DELIMITER)
    df.columns = ["district_name","district_id"]
    df["district_id"] = df["district_id"].apply(lambda x: x[1:])
    return df


def get_category():
    df = pd.read_csv(CATEGORY_CSV, header=None, sep=FIELD_DELIMITER)
    df.columns = ["category_name","category_id"]
    df["category_id"] = df["category_id"].apply(lambda x: int(x[1:]))
    return df


def get_shops():
    all_files = glob.glob(os.path.join(SHOP_DATA_DIR, "*.csv"))
    df = pd.concat((pd.read_csv(f, header=None, sep=FIELD_DELIMITER) for f in all_files))
    df.columns = ["shop_id", "shop_name", "address", "lng", "lat", "phone", "district_id", "region_id", "category_id"]
    shops = df[["shop_id", "shop_name", "address", "lng", "lat", "category_id"]]
    locations = get_locations()
    df = pd.merge(shops, locations, how="left", on="shop_id")
    df["lng"] = df["lng_baidu"]
    df["lat"] = df["lat_baidu"]
    return df[["shop_id", "shop_name", "address", "lng", "lat", "category_id"]]


def get_locations():
    all_files = glob.glob(os.path.join(LOCATION_DATA_DIR, "*.csv"))
    df = pd.concat((pd.read_csv(f, header=None, sep=FIELD_DELIMITER) for f in all_files))
    df.columns = ["shop_id", "lng_baidu", "lat_baidu"]
    return df


def get_comments():
    all_files = glob.glob(os.path.join(COMMENT_DATA_DIR, "*.csv"))
    df = pd.concat((pd.read_csv(f, header=None, sep=FIELD_DELIMITER) for f in all_files))
    df.columns = ["shop_id", "comment_num", "star_5_num", "star_4_num", "star_3_num", "star_2_num", "star_1_num"]
    df["good_rate"] = 100 * (df["star_4_num"]+df["star_5_num"]) / df["comment_num"]
    return df


def get_scores():
    all_files = glob.glob(os.path.join(SCORE_DATA_DIR, "*.csv"))
    df = pd.concat((pd.read_csv(f, header=None, sep="\t") for f in all_files))
    df.columns = ["shop_id", "avg_price", "taste_score", "env_score", "ser_score"]
    return df


def get_heats():
    all_files = glob.glob(os.path.join(HEAT_DATA_DIR, "*.csv"))
    df = pd.concat((pd.read_csv(f, header=None, sep=FIELD_DELIMITER) for f in all_files))
    df.columns = ["shop_id", "total_hits", "today_hits", "monthly_hits", "weekly_hits", "last_week_hits"]
    return df


def get_routes():
    all_files = glob.glob(os.path.join(ROUTE_DATA_DIR, "*.csv"))
    df = pd.concat((pd.read_csv(f, header=None, sep=FIELD_DELIMITER) for f in all_files))
    df.columns = ["shop_id", "taxi_route", "public_route"]
    df['taxi_distance'] = df['taxi_route'].apply(lambda x: 0-float(json.loads(x)['distance']))
    return df

def get_all_info():
    shops = get_shops()
    comments = get_comments()
    scores = get_scores()
    heats = get_heats()
    routes = get_routes()
    category = get_category()
    shop_comment = pd.merge(shops, comments, how="left", on="shop_id")
    shop_comment_score = pd.merge(shop_comment, scores, how="left", on="shop_id")
    shop_comment_score_heat = pd.merge(shop_comment_score, heats, how="left", on="shop_id")
    shop_comment_score_heat_distance = pd.merge(shop_comment_score_heat, routes, how="left", on="shop_id")
    shop_comment_score_heat_distance_category = pd.merge(shop_comment_score_heat_distance, category, how="left", on="category_id")
    return shop_comment_score_heat_distance_category


def get_weight_details():
    all_info = get_all_info()
    df = all_info[["shop_id", "shop_name", "lng", "lat",
                   "comment_num", "star_5_num", "star_4_num", "star_3_num", "star_2_num", "star_1_num",
                   "avg_price", "taste_score", "env_score", "ser_score", "good_rate",
                   "total_hits", "today_hits", "monthly_hits", "weekly_hits", "last_week_hits",
                   "taxi_distance", "taxi_route", "public_route", "category_name"
                   ]]
    return df\
        .groupby("shop_id")\
        .agg({"shop_id": np.max, "shop_name": np.max, "lng": np.max, "lat": np.max,
            "comment_num": np.max, "star_5_num": np.max, "star_4_num": np.max, "star_3_num": np.max, "star_2_num": np.max, "star_1_num": np.max,
            "avg_price": np.max, "taste_score": np.max, "env_score": np.max, "ser_score": np.max, "good_rate": np.max,
            "total_hits": np.max, "today_hits": np.max, "monthly_hits": np.max, "weekly_hits": np.max, "last_week_hits": np.max,
            "taxi_distance": np.max, "taxi_route": np.max, "public_route": np.max, "category_name": np.max})


def save_weight_details():
    df = get_weight_details()
    import csv
    df.to_csv(DETAILS_CSV, sep=FIELD_DELIMITER, doublequote=False, quoting=csv.QUOTE_NONE)


def load_weight_details():
    df = pd.read_csv(DETAILS_CSV, sep=FIELD_DELIMITER, na_values="None")
    df["shop_id"] = df["shop_id"].apply(lambda x: str(x))
    return df


def get_customized_shops(details, params, order_by):
    bad_rate, taste_score, comment_num, avg_price = None, None, None, None
    try:
        bad_rate = params['bad_rate']
        taste_score = params['taste_score']
        comment_num = params['comment_num']
        avg_price = params['avg_price']
    except:
        pass
    condition = True
    if bad_rate is not None:
        condition = condition & (details["bad_rate"] <= bad_rate)
    if taste_score is not None:
        condition = condition & (details["taste_score"] >= taste_score)
    if comment_num is not None:
        condition = condition & (details["comment_num"] >= comment_num)
    if avg_price is not None:
        condition = condition & (details["avg_price"] <= avg_price)

    if order_by is not None and order_by in ('taste_score', 'last_week_hits', 'comment_num', 'good_rate', 'taxi_distance'):
        details = details.sort_values([order_by], ascending=[False])
    else:
        details = details

    details['route'] = details['public_route'].apply(get_metro_info)
    if condition is not True:
        return details[condition].loc[:, ["shop_id", "shop_name", "taste_score", "avg_price", "category_name", "lng", "lat", "route"]]
    else:
        return details.loc[:, ["shop_id", "shop_name", "taste_score", "avg_price", "category_name", "lng", "lat", "route"]]


def get_distinct_shops():
    shops = get_shops()
    return shops[["shop_id", "shop_name", "lng", "lat"]].drop_duplicates().itertuples()


def get_json_data_from_df(df):
    res = [{"name": row.shop_name, "lng": row.lng, "lat": row.lat, "avg_price": row.avg_price,
             "taste_score": row.taste_score, "category": row.category_name, "shop_id": row.shop_id,
            "route": row.route
            }
            for row in df.itertuples()]
    return json.dumps(res, ensure_ascii=False).encode("utf-8")


def get_metro_info(public_route):
    if public_route is np.NAN: return ""
    duration = json.loads(public_route)["duration"]
    routes = json.loads(public_route)["routes"]
    metros = ""
    for route in routes:
        if route["type"] == 1:
            pass
        elif route["type"] == 2:
            metros += "{0}->{1},".format(route["on_station"], route["off_station"])
    metros += "耗时:{0}".format(get_time_str(duration))
    return metros


def get_time_str(duration):
    hour = int(duration / 3600)
    duration -= hour*3600
    minute = int(duration / 60)
    return "{0}时{1}分".format(hour,minute)


def test_get_json_data_from_df():
    df = get_customized_shops(load_weight_details(),
                              params={'comment_num': 500.0, 'bad_rate': None, 'taste_score': 8.5, 'avg_price': None},
                              order_by="comment_num")
    res = df[["shop_id", "shop_name", "public_route"]].head(1)
    res['route'] = res['public_route'].apply(get_metro_info)
    print res


if __name__ == '__main__':
    #save_weight_details()
    test_get_json_data_from_df()