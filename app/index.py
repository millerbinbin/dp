# -*- coding:utf-8 -*-
import json
import sys

from flask import render_template, request

import service
from app import app

__author__ = 'hubin6'

reload(sys)
sys.setdefaultencoding("utf-8")

all_data_info = service.load_weight_details()
offset = 0


def get_string_param_2_number(param_name):
    value = request.values.get(param_name)
    if value is not None: value = float(value)
    return value


@app.route('/shops/<int:page>/<int:limit>/order_by=<col>', methods=['POST'])
def get_default_shops(page, limit, col):
    bad_rate = get_string_param_2_number("bad_rate")
    taste_score = get_string_param_2_number("taste_score")
    avg_price = get_string_param_2_number("avg_price")
    comment_num = get_string_param_2_number("comment_num")
    params = {"bad_rate": bad_rate, "taste_score": taste_score, "avg_price": avg_price, "comment_num": comment_num}
    print page, params, limit, col
    limit_data = service.get_customized_shops(all_data_info, params=params, order_by=col)
    result = limit_data.iloc[(page-1)*limit:page*limit]
    return service.get_json_data_from_df(result)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

