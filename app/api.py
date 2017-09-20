# -*- coding:utf-8 -*-
import sys
from flask import render_template, request

from app import server
from main import service

__author__ = 'hubin6'

reload(sys)
sys.setdefaultencoding("utf-8")


all_shop_info, all_category = service.load_weight_details(filter_same_group=True, filter_new_shop=False)


def get_string_param_2_number(param_name):
    value = request.values.get(param_name)
    if value is not None:
        try:
            value = float(value)
        except Exception:
            value = str(value)
    return value


@server.route('/shops/', methods=['GET'])
def get_shops():
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
    filter_same_group = get_string_param_2_number("filter_same_group")
    filter_new_shop = get_string_param_2_number("filter_new_shop")
    params = {"taste_score": taste_score, "avg_price_min": avg_price_min, "avg_price_max": avg_price_max,
              "comment_num": comment_num, "category": category_name, "query":query, "position":position}
    params['order_by'] = order_col
    params['page'] = page
    params['limit'] = limit
    params['filter_same_group'] = filter_same_group
    params['filter_new_shop'] = filter_new_shop
    df = service.get_customized_shops(params=params)
    token = get_string_param_2_number("callback")
    result = "{1}({0})".format(service.get_shops_json_from_df(df), token)
    return result


@server.route('/category/all', methods=['GET'])
def get_all_categories():
    token = get_string_param_2_number("callback")
    result = "{1}({0})".format(service.get_category_json_from_df(all_category), token)
    return result


@server.route('/')
@server.route('/index')
def index():
    return render_template('index.html')


@server.route('/test')
def test():
    return render_template('test.html')