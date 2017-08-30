# -*- coding:utf-8 -*-
import sys
import random

from flask import render_template, request

from app import app
from main import service

__author__ = 'hubin6'

reload(sys)
sys.setdefaultencoding("utf-8")

all_data_info = service.load_weight_details(True)
offset = 0


def get_string_param_2_number(param_name):
    value = request.values.get(param_name)
    if value is not None:
        try:
            value = float(value)
        except:
            value = str(value)
    return value


@app.route('/shops/<int:page>/<int:limit>/order_by=<col>', methods=['POST'])
def get_customized_shops(page, limit, col):
    good_rate = get_string_param_2_number("good_rate")
    taste_score = get_string_param_2_number("taste_score")
    avg_price_min = get_string_param_2_number("avg_price_min")
    avg_price_max = get_string_param_2_number("avg_price_max")
    comment_num = get_string_param_2_number("comment_num")
    category_name = get_string_param_2_number("category")
    params = {"good_rate": good_rate, "taste_score": taste_score, "avg_price_min": avg_price_min, "avg_price_max": avg_price_max,
              "comment_num": comment_num, "category": category_name}
    # print page, params, limit, col, category_name
    limit_data = service.get_customized_shops(all_data_info, params=params, order_by=col)
    result = limit_data.iloc[(page-1)*limit:page*limit]
    return service.get_json_data_from_df(result)


@app.route('/shops/random/<int:limit>', methods=['GET'])
def get_random_shops(limit):
    limit_data = service.get_random_favor_shops(all_data_info)
    print len(limit_data)
    start = int(random.random()*50)
    result = limit_data.iloc[start:start+limit]
    return service.get_json_data_from_df(result)


@app.route('/shops/favors', methods=['POST'])
def post_shop_favors():
    favor_data = get_string_param_2_number("favor_data")
    return '{{"message": "成功导入{0}条记录"}}'.format(service.save_favor_data(favor_data))


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/rohr')
def rohr():
    return render_template('rohr.html')