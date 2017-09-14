# -*- coding:utf-8 -*-
import sys

from flask import render_template, request

from app import app
from main import service

__author__ = 'hubin6'

reload(sys)
sys.setdefaultencoding("utf-8")

all_shop_info = service.load_weight_details(True)
all_category = all_shop_info[["category_name"]].drop_duplicates()


def get_string_param_2_number(param_name):
    value = request.values.get(param_name)
    if value is not None:
        try:
            value = float(value)
        except Exception:
            value = str(value)
    return value


@app.route('/shops/', methods=['GET'])
def get_customized_shops():
    page = int(get_string_param_2_number("page"))
    limit = int(get_string_param_2_number("limit"))
    order_col = get_string_param_2_number("order_by")
    taste_score = get_string_param_2_number("taste_score")
    avg_price_min = get_string_param_2_number("avg_price_min")
    avg_price_max = get_string_param_2_number("avg_price_max")
    comment_num = get_string_param_2_number("comment_num")
    category_name = get_string_param_2_number("category")
    query = get_string_param_2_number("query")
    position = get_string_param_2_number("position")
    params = {"taste_score": taste_score, "avg_price_min": avg_price_min, "avg_price_max": avg_price_max,
              "comment_num": comment_num, "category": category_name, "query":query, "position":position}
    limit_data = service.get_customized_shops(all_shop_info, params=params, order_by=order_col)
    df = limit_data.iloc[(page-1)*limit:page*limit]
    token = get_string_param_2_number("callback")
    result = "{1}({0})".format(service.get_shops_json_from_df(df), token)
    return result


@app.route('/category/all', methods=['GET'])
def get_all_categories():
    token = get_string_param_2_number("callback")
    result = "{1}({0})".format(service.get_category_json_from_df(all_category), token)
    return result


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/test')
def test():
    return render_template('test.html')