# -*- coding:utf-8 -*-
import re
from crawl import crawlLib
from entity import entity
import sys
from db import tasks
import threading
from time import ctime,sleep

__author__ = 'hubin6'

reload(sys)
sys.setdefaultencoding("utf-8")

SH_URL = "http://www.dianping.com/search/category/1/10"
SHOP_DETAILS_URL = "http://www.dianping.com/ajax/json/shopfood/wizard/BasicHideInfoAjaxFP?_nr_force=1502177990602&shopId="
REVIEW_URL = "http://www.dianping.com/shop/{0}/review_more?pageno=1"
REGION_TABLE = tasks.get_region_table()


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
    region_name = data.find("div", class_="tag-addr").find(href=re.compile(".*/[^g]\d+$")).text
    print region_name
    try:
        region, district = REGION_TABLE.get(region_name)
    except:
        region, district = None, None
    tmp = data.find("div", class_="comment")
    avg_price = get_average_price(tmp)
    address = data.find("div", class_="tag-addr").find("span", class_="addr").text
    tmp = data.find("span", class_="comment-list")
    taste_score, env_score, ser_score = get_score(tmp)
    phone_no, total_hits, today_hits, monthly_hits, weekly_hits, last_week_hits, lat, lng = get_shop_details(shop_id)
    cmt_num, star_5_num, star_4_num, star_3_num, star_2_num, star_1_num = get_shop_review_star_num(shop_id)
    return entity.Shop(shop_id, shop_name, address, lng, lat, phone_no, district, region, category,
                       avg_price, taste_score, env_score, ser_score,
                       total_hits, today_hits, monthly_hits, weekly_hits, last_week_hits,
                       cmt_num, star_5_num, star_4_num, star_3_num, star_2_num, star_1_num)


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

def get_average_price(data):
    try:
        t = data.find("a", class_="mean-price")
        price = t.find(text=re.compile("\d.*"))[1:]
    except:
        price = None
    return price


def get_shop_review_star_num(shop_id):
    print REVIEW_URL.format(shop_id)
    try:
        data = crawlLib.Crawler(REVIEW_URL.format(shop_id)).parseContent(mode="complex")
        comment_num = data.find("div", class_="comment-star").find_all("dd")[0].find("em", class_="col-exp").text[1:-1]
        star_5_num = data.find("div", class_="comment-star").find_all("dd")[1].find("em", class_="col-exp").text[1:-1]
        star_4_num = data.find("div", class_="comment-star").find_all("dd")[2].find("em", class_="col-exp").text[1:-1]
        star_3_num = data.find("div", class_="comment-star").find_all("dd")[3].find("em", class_="col-exp").text[1:-1]
        star_2_num = data.find("div", class_="comment-star").find_all("dd")[4].find("em", class_="col-exp").text[1:-1]
        star_1_num = data.find("div", class_="comment-star").find_all("dd")[5].find("em", class_="col-exp").text[1:-1]
    except:
        data = crawlLib.Crawler(REVIEW_URL.format(shop_id)).parseContent(mode="complex")
        comment_num = data.find("div", class_="comment-star").find_all("dd")[0].find("em", class_="col-exp").text[1:-1]
        star_5_num = data.find("div", class_="comment-star").find_all("dd")[1].find("em", class_="col-exp").text[1:-1]
        star_4_num = data.find("div", class_="comment-star").find_all("dd")[2].find("em", class_="col-exp").text[1:-1]
        star_3_num = data.find("div", class_="comment-star").find_all("dd")[3].find("em", class_="col-exp").text[1:-1]
        star_2_num = data.find("div", class_="comment-star").find_all("dd")[4].find("em", class_="col-exp").text[1:-1]
        star_1_num = data.find("div", class_="comment-star").find_all("dd")[5].find("em", class_="col-exp").text[1:-1]
    return comment_num, star_5_num, star_4_num, star_3_num, star_2_num, star_1_num


from csv import csvLib
def convert_cmt_num(f):
    FIELD_DELIMITER = "\t"
    cmt_list = []
    idx = 0
    for r in open(shop_path + f, "r"):
        shop_id, comment_num = r.strip().split(FIELD_DELIMITER)
        comment_num, star_5_num, star_4_num, star_3_num, star_2_num, star_1_num = get_shop_review_star_num(shop_id)
        cmt_list.append ((shop_id, comment_num, star_5_num, star_4_num, star_3_num, star_2_num, star_1_num))
        idx += 1
        print idx
    csvLib.writeRecordsToFile("../data/comments/{0}".format(f), cmt_list, FIELD_DELIMITER)



if __name__ == '__main__':
    shop_path = "../data/comments/"
    import os
    f_list = {f for f in os.listdir(shop_path)}
    print f_list
    threads = []
    for f in f_list:
        print f
        threads.append(threading.Thread(target=convert_cmt_num, args=(f,)))

    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()

    # shop_path = "../data/comments/"
    # import os
    #
    # FIELD_DELIMITER = "\t"
    # for f in os.listdir(shop_path):
    #     cmt_list = []
    #     for r in open(shop_path + f, "r"):
    #         shop_id, comment_num = r.strip().split(FIELD_DELIMITER)
    #         comment_num, star_5_num, star_4_num, star_3_num, star_2_num, star_1_num = get_shop_review_star_num(shop_id)
    #         cmt_list.append ((shop_id, comment_num, star_5_num, star_4_num, star_3_num, star_2_num, star_1_num))
    #     csvLib.writeRecordsToFile("../data/comments/{0}".format(f), cmt_list, FIELD_DELIMITER)