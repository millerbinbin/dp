# -*- coding:utf-8 -*-
import json
import sys

from flask import render_template, request

from app import app
from crawl import load_data

__author__ = 'hubin6'

reload(sys)
sys.setdefaultencoding("utf-8")

all_data_info = load_data.load_weight_details()


def df_2_json(df):
    res = [{"name": row.shop_name, "lng": row.lng, "lat": row.lat, "avg_price": row.avg_price,
             "taste_score": row.taste_score, "category": row.category_name, "shop_id": row.shop_id}
            for row in df.itertuples()]
    return json.dumps(res, ensure_ascii=False).encode("utf-8")


def get_string_param_2_number(param_name):
    value = request.values.get(param_name)
    if value is not None: value = float(value)
    return value


@app.route('/shops/<int:limit>', methods=['POST'])
def get_default_shops(limit):
    bad_rate = get_string_param_2_number("bad_rate")
    taste_score = get_string_param_2_number("taste_score")
    avg_price = get_string_param_2_number("avg_price")
    comment_num = get_string_param_2_number("comment_num")
    params = {"bad_rate": bad_rate, "taste_score": taste_score, "avg_price": avg_price, "comment_num": comment_num}
    print params
    limit_data = load_data.customized_shops(all_data_info, params=params).head(limit)
    return df_2_json(limit_data)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

