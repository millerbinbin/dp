# -*- coding:utf-8 -*-
from crawl import crawlLib, location
from entity import entity
from db import tasks, mysqlBase
from csv import csvLib
import re, json

__author__ = 'hubin6'


SH_URL = "http://www.dianping.com/search/category/1/10"
SHOP_DETAILS_URL = "http://www.dianping.com/ajax/json/shopfood/wizard/BasicHideInfoAjaxFP?_nr_force=1502177990602&shopId={}"
REVIEW_URL = "http://www.dianping.com/shop/{0}/review_more"
COMMENT_URL = "http://www.dianping.com/shop/{0}/review_more_5star?pageno={1}"
CSV_DIR = "../data"
FIELD_DELIMITER = "\t"
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
            print "crawl finished, total records: {0}".format(len(info_list))
            break
        page_num = "p{0}".format(page)
        p_url = url + page_num
        content = crawlLib.Crawler(p_url).parse_content()
        for c in content.find("div", id="shop-all-list").find_all("li", class_=""):
            result = get_shop_result(c, category_id)
            score = result.get_score()
            heat = result.get_heat()
            info = result.get_info()
            comment = result.get_comment()
            total_num += 1
            if float(score.taste_score) < score_threshold or total_num > limit_num:
                stop_flag = 1
                break
            info_list.append(info.to_tuple())
            heat_list.append(heat.to_tuple())
            score_list.append(score.to_tuple())
            cmt_list.append(comment.to_tuple())
    return info_list, heat_list, score_list, cmt_list


def get_shop_details(shop_id):
    details = crawlLib.Crawler(SHOP_DETAILS_URL.format(shop_id)).to_json()['msg']['shopInfo']
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
    taste_score, env_score, ser_score = None, None, None
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
    data = crawlLib.Crawler(REVIEW_URL.format(shop_id)).parse_content(mode="complex")
    comment_num = data.find("div", class_="comment-star").find_all("dd")[0].find("em", class_="col-exp").text[1:-1]
    star_5_num = data.find("div", class_="comment-star").find_all("dd")[1].find("em", class_="col-exp").text[1:-1]
    star_4_num = data.find("div", class_="comment-star").find_all("dd")[2].find("em", class_="col-exp").text[1:-1]
    star_3_num = data.find("div", class_="comment-star").find_all("dd")[3].find("em", class_="col-exp").text[1:-1]
    star_2_num = data.find("div", class_="comment-star").find_all("dd")[4].find("em", class_="col-exp").text[1:-1]
    star_1_num = data.find("div", class_="comment-star").find_all("dd")[5].find("em", class_="col-exp").text[1:-1]
    return comment_num, star_5_num, star_4_num, star_3_num, star_2_num, star_1_num


def get_shop_favorite_food(shop_id):
    dish_list = {}
    for pageno in range(1, 11):
        data = crawlLib.Crawler(COMMENT_URL.format(shop_id, pageno)).parse_content(mode="complex")
        for comment in data.find_all("div", class_="comment-recommend"):
            for dish in comment.find_all("a", class_="col-exp", target="_blank"):
                dish_list[dish.text] = 1 if dish_list.get(dish.text) is None else 1 + dish_list.get(dish.text)
    return dish_list


def crawl_all_shops():
    for i in open(CSV_DIR + "/base/category.csv"):
        category_name, category = i.strip().split(FIELD_DELIMITER)
        print "start to crawl: {0}...".format(category_name)
        info_list, heat_list, score_list, cmt_list = crawl_all_shops_by_category(category, "taste", 8.5, 500)
        csvLib.write_records_to_csv(CSV_DIR + "/shops/{0}.csv".format(category), info_list, FIELD_DELIMITER)
        csvLib.write_records_to_csv(CSV_DIR + "/heats/{0}.csv".format(category), heat_list, FIELD_DELIMITER)
        csvLib.write_records_to_csv(CSV_DIR + "/scores/{0}.csv".format(category), score_list, FIELD_DELIMITER)
        csvLib.write_records_to_csv(CSV_DIR + "/comments/{0}.csv".format(category), cmt_list, FIELD_DELIMITER)


def crawl_shops_routes():
    def load_all_saved_routes():
        return {i.strip().split(FIELD_DELIMITER)[0] for i in open(CSV_DIR + "/routes/data.csv")}
    shop_list = load_all_saved_routes()
    origin = entity.Location(lng=121.615539648, lat=31.2920292218)
    conn = mysqlBase.MySQLConnection().get_connection()
    public_routes = []
    for row in tasks.get_all_shops_location(cnx=conn):
        shop_id = str(row[0])
        if shop_id in shop_list: continue
        dest = entity.Location(lat=float(row[2]), lng=float(row[1]))
        routes = location.get_complete_route(origin, dest)
        taxi = routes.get("taxi")
        public = routes.get("public")
        if taxi is None: continue # too far to arrive
        if public is None:
            public_routes.append((shop_id, taxi.to_json(), None,))
        else:
            public_routes.append((shop_id, taxi.to_json(), public.to_json(),))
        if len(public_routes) % 20 == 0:
            print "flush data to disk..."
            csvLib.write_records_to_csv(CSV_DIR + "/routes/data.csv", public_routes, FIELD_DELIMITER, mode="a")
            public_routes = []
    conn.close()
    csvLib.write_records_to_csv(CSV_DIR + "/routes/data.csv", public_routes, FIELD_DELIMITER, mode="a")


def crawl_shops_favorite_food():
    def load_all_saved_favorites():
        return {i.strip().split(FIELD_DELIMITER)[0] for i in open(CSV_DIR + "/favorite/data.csv")}

    shop_list = load_all_saved_favorites()

    favorite_list = []
    for row in tasks.get_all_shops():
        shop_id = str(row[0])
        if shop_id in shop_list: continue
        favorite_food = json.dumps(get_shop_favorite_food(shop_id), ensure_ascii=False).encode('utf8')
        print favorite_food
        favorite_list.append((shop_id, favorite_food))
        if len(favorite_list) % 20 == 0:
            print "flush data to disk..."
            csvLib.write_records_to_csv(CSV_DIR + "/favorite/data.csv", favorite_list, FIELD_DELIMITER, mode="a")
            favorite_list = []
    csvLib.write_records_to_csv(CSV_DIR + "/favorite/data.csv", favorite_list, FIELD_DELIMITER, mode="a")

if __name__ == '__main__':
    crawl_shops_favorite_food()