# -*- coding:utf-8 -*-
import sys

from flask import render_template, request

from app import app
from main import service

__author__ = 'hubin6'

reload(sys)
sys.setdefaultencoding("utf-8")

all_data_info = service.load_weight_details(True)


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
    query = get_string_param_2_number("query")
    params = {"good_rate": good_rate, "taste_score": taste_score, "avg_price_min": avg_price_min, "avg_price_max": avg_price_max,
              "comment_num": comment_num, "category": category_name, "query":query}
    limit_data = service.get_customized_shops(all_data_info, params=params, order_by=col)
    result = limit_data.iloc[(page-1)*limit:page*limit]
    return service.get_shops_json_from_df(result)


@app.route('/category/all', methods=['GET'])
def get_all_categories():
    df = all_data_info[["category_name"]].drop_duplicates()
    return service.get_category_json_from_df(df)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

