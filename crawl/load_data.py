# -*- coding:utf-8 -*-
from crawl import WORK_DIR
import pandas as pd
import numpy as np
import os
import glob

BASE_DATA_DIR = os.path.join(WORK_DIR, "data/base")
REGION_CSV = os.path.join(BASE_DATA_DIR, "regions.csv")
DISTRICT_CSV = os.path.join(BASE_DATA_DIR, "districts.csv")
CATEGORY_CSV = os.path.join(BASE_DATA_DIR, "category.csv")
SHOP_DATA_DIR = os.path.join(BASE_DATA_DIR, "../shops")
LOCATION_DATA_DIR = os.path.join(BASE_DATA_DIR, "../location")
COMMENT_DATA_DIR = os.path.join(BASE_DATA_DIR, "../comments")
HEAT_DATA_DIR = os.path.join(BASE_DATA_DIR, "../heats")
SCORE_DATA_DIR = os.path.join(BASE_DATA_DIR, "../scores")
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
    df["bad_rate"] = 100 * (df["star_1_num"]+df["star_2_num"]) / df["comment_num"]
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


def get_all_info():
    shops = get_shops()
    comments = get_comments()
    scores = get_scores()
    heats = get_heats()
    category = get_category()
    shop_comment = pd.merge(shops, comments, how="left", on="shop_id")
    shop_comment_score = pd.merge(shop_comment, scores, how="left", on="shop_id")
    shop_comment_score_heat = pd.merge(shop_comment_score, heats, how="left", on="shop_id")
    shop_comment_score_heat_category = pd.merge(shop_comment_score_heat, category, how="left", on="category_id")
    return shop_comment_score_heat_category


def get_weight_details():
    all_info = get_all_info()
    df = all_info[["shop_id", "shop_name", "lng", "lat",
                   "comment_num", "star_5_num", "star_4_num", "star_3_num", "star_2_num", "star_1_num",
                   "avg_price", "taste_score", "env_score", "ser_score", "bad_rate",
                   "total_hits", "today_hits", "monthly_hits", "weekly_hits", "last_week_hits",
                   "category_name"
                   ]]
    return df\
        .groupby("shop_id")\
        .agg({"shop_id": np.max, "shop_name": np.max, "lng": np.max, "lat": np.max,
            "comment_num": np.max, "star_5_num": np.max, "star_4_num": np.max, "star_3_num": np.max, "star_2_num": np.max, "star_1_num": np.max,
            "avg_price": np.max, "taste_score": np.max, "env_score": np.max, "ser_score": np.max, "bad_rate": np.max,
            "total_hits": np.max, "today_hits": np.max, "monthly_hits": np.max, "weekly_hits": np.max, "last_week_hits": np.max,
            "category_name": np.max})\
        .sort_values(['taste_score', "comment_num"], ascending=[False, False])


def save_weight_details():
    df = get_weight_details()
    df.to_csv(DETAILS_CSV, sep=FIELD_DELIMITER)


def load_weight_details():
    df = pd.read_csv(DETAILS_CSV, sep=FIELD_DELIMITER, na_values="None")
    df["shop_id"] = df["shop_id"].apply(lambda x: str(x))
    return df


def customized_shops(details, params):
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

    if condition is not True:
        return details[condition]\
              .sort_values(['taste_score', 'last_week_hits'], ascending=[False, False])\
              .loc[:, ["shop_id", "shop_name", "taste_score", "avg_price", "category_name", "lng", "lat", "last_week_hits"]]
    else:
        return details.sort_values(['taste_score', 'last_week_hits'], ascending=[False, False]) \
                .loc[:, ["shop_id", "shop_name", "taste_score", "avg_price", "category_name", "lng", "lat", "last_week_hits"]]


def get_distinct_shops():
    shops = get_shops()
    return shops[["shop_id", "shop_name", "lng", "lat"]].drop_duplicates().itertuples()


if __name__ == '__main__':
    # save_weight_details()
    # print customized_shops(load_weight_details(), params={"bad_rate": 2, "taste_score": 9, "comment_num": 2000})
    for row in get_distinct_shops():
        print row.shop_id, row.shop_name, row.lng, row.lat
