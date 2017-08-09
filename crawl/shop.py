# -*- coding:utf-8 -*-
import re
from crawl import crawlLib
from entity import entity
import sys

__author__ = 'hubin6'

reload(sys)
sys.setdefaultencoding("utf-8")

SH_URL = "http://www.dianping.com/search/category/1/10"
SHOP_DETAILS_URL = "http://www.dianping.com/ajax/json/shopfood/wizard/BasicHideInfoAjaxFP?_nr_force=1502177990602&shopId="


def get_seq_suffix_from_type(type):
    seq_dict = {"taste": "o5", "rate": "o3", "heat": "o2", "env": "o6", "ser": "o7", "cmt": "o10"}
    return seq_dict.get(type)


def crawl_all_shops_by_category(category, order_type, score_threshold, limit_num=1000):
    category_id = category[1:]
    url = SH_URL + "/" + category + get_seq_suffix_from_type(order_type)
    stop_flag = 0
    total_num = 0
    info_list = []
    heat_list = []
    score_list = []
    cmt_list = []
    for page in range(1, 51):
        if stop_flag == 1:
            break
        page_num = "p{0}".format(page)
        p_url = url + page_num
        print p_url
        content = crawlLib.Crawler(p_url).parseContent()
        for c in content.find("div", id="shop-all-list").find_all("li", class_=""):
            result = get_shop_result(c, category_id)
            score = result.get_score()
            heat = result.get_heat()
            info = result.get_info()
            comment = result.get_comment()
            total_num += 1
            info_list.append(info.to_tuple())
            heat_list.append(heat.to_tuple())
            score_list.append(score.to_tuple())
            cmt_list.append(comment.to_tuple())
            if float(score.taste_score) < score_threshold or total_num > limit_num:
                stop_flag = 1
                break
    return info_list, heat_list, score_list, cmt_list


def get_shop_details(shop_id):
    details = crawlLib.Crawler(SHOP_DETAILS_URL + shop_id).toJson()['msg']['shopInfo']
    today_hits = details['todayHits']
    monthly_hits = details['monthlyHits']
    weekly_hits = details['weeklyHits']
    lat = details['glat']
    lng = details['glng']
    total_hits = details['hits']
    phone_no = details['phoneNo']
    last_week_hits = details['prevWeeklyHits']
    return phone_no, total_hits, today_hits, monthly_hits, weekly_hits, last_week_hits, lat, lng


def get_shop_result(data, category):
    tmp = data.find("div", class_="pic")
    shop_id = tmp.a['href'][tmp.a['href'].rfind('/') + 1:]
    shop_name = tmp.img['alt']
    tmp = data.find("div", class_="comment")
    avg_price = get_average_price(tmp)
    cmt_num = get_comment_num(tmp)
    address = data.find("div", class_="tag-addr").find("span", class_="addr").text
    tmp = data.find("span", class_="comment-list")
    taste_score, env_score, ser_score = get_score(tmp)
    phone_no, total_hits, today_hits, monthly_hits, weekly_hits, last_week_hits, lat, lng = get_shop_details(shop_id)
    return entity.Shop(shop_id, shop_name, address, lng, lat, phone_no, category,
                       avg_price, taste_score, env_score, ser_score,
                       total_hits, today_hits, monthly_hits, weekly_hits, last_week_hits,
                       cmt_num)


def get_score(data):
    for i in data.find_all("span"):
        score = i.find(text=re.compile("\.\d*"))
        if i.text.find(r"口味") >= 0:
            taste_score = score
        if i.text.find(r"环境") >= 0:
            env_score = score
        if i.text.find(r"服务") >= 0:
            ser_score = score
    return taste_score, env_score, ser_score


def get_comment_num(data):
    try:
        t = data.find("a", class_="review-num")
        num = t.find(text=re.compile(".*\d.*"))
    except:
        num = None
    return num


def get_average_price(data):
    try:
        t = data.find("a", class_="mean-price")
        price = t.find(text=re.compile("\d.*"))[1:]
    except:
        price = None
    return price

