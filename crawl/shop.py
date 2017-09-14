# -*- coding:utf-8 -*-
import json
import os
import re
import glob
import sys
import shutil

from crawl import crawlLib, location, SH_URL, WORK_DIR
from entity import entity
from filewriter import csvLib
from main import service
from selenium import webdriver
import time
from bs4 import BeautifulSoup

__author__ = 'hubin6'

reload(sys)
sys.setdefaultencoding("utf-8")


SHOP_DETAILS_URL = "http://www.dianping.com/ajax/json/shopfood/wizard/BasicHideInfoAjaxFP?_nr_force=1502177990602&shopId={}"
REVIEW_URL = "http://www.dianping.com/shop/{0}/review_more_newest"
# COMMENT_URL = "http://www.dianping.com/shop/{0}/review_more_5star?pageno={1}"
# SHOP_URL = "http://www.dianping.com/shop/{0}"

TASTE_SCORE_THRESHOLD = 8
CATEGORY_NUMBER_LIMIT = 400
DEFAULT_ORDER_TYPE = "taste"

BACKUP_DATA_DIR = os.path.join(WORK_DIR, "data-backup")
DATA_DIR = os.path.join(WORK_DIR, "data")
CATEGORY_CSV = os.path.join(DATA_DIR, "base/category.csv")
REGION_CSV = os.path.join(DATA_DIR, "base/regions.csv")
FAVORITE_CSV = os.path.join(DATA_DIR, "favorite/data.csv")
LOCATION_CSV = os.path.join(DATA_DIR, "location/data.csv")
ROUTE_CSV = os.path.join(DATA_DIR, "routes/data.csv")

SHOP_DATA_CSV = os.path.join(DATA_DIR, "shops/{0}.csv")
COMMENT_DATA_CSV = os.path.join(DATA_DIR, "comments/{0}.csv")
HEAT_DATA_CSV = os.path.join(DATA_DIR, "heats/{0}.csv")
SCORE_DATA_CSV = os.path.join(DATA_DIR, "scores/{0}.csv")

FIELD_DELIMITER = "\t"
HOME_LOC = entity.Location(lng=121.615539648, lat=31.2920292218)   #location of Chun Jiang
REGION_TABLE = service.get_region_table()
CATEGORY_TABLE = service.get_category_table()


def get_seq_suffix_from_type(type):
    seq_dict = {"taste": "o5", "rate": "o3", "heat": "o2", "env": "o6", "ser": "o7", "cmt": "o10"}
    return seq_dict.get(type)


def crawl_all_shops_by_category(category, order_type, score_threshold, limit_num=1000):
    category_id = category.category_id
    category_code = category.category_code
    category_name = category.category_name
    url = SH_URL + "/" + category_code + get_seq_suffix_from_type(order_type)
    stop_flag = 0
    total_num = 0
    info_list = []
    heat_list = []
    score_list = []
    cmt_list = []
    for page in range(1, 51):
        if stop_flag == 1:
            print "【{0}】爬取完成，总数据条数：{1}".format(category_name, len(info_list))
            break
        page_num = "p{0}".format(page)
        p_url = url + page_num
        print p_url
        content = crawlLib.Crawler(p_url).parse_content()
        for c in content.find("div", id="shop-all-list").find_all("li", class_=""):
            result = get_shop_result(c, category_id)
            if result is None:
                continue
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


def get_shop_result(data, category_id):
    tmp = data.find("div", class_="pic")
    shop_id = tmp.a['href'][tmp.a['href'].rfind('/') + 1:]
    subcategory_name = data.find("div", class_="tag-addr").find(href=re.compile(".*/[^r]\d+$")).text.strip()
    subcategory_id, actual_category_id = CATEGORY_TABLE.get(str(subcategory_name))
    if actual_category_id != category_id:
        return None
    shop_name = tmp.img['alt']
    if data.find("div", class_="tit").find("span", class_="istopTrade")!=None:
        return None
    print shop_name
    shop_group_name = get_group_name(str(shop_name))
    try:
        region_name = data.find("div", class_="tag-addr").find(href=re.compile(".*/[^g]\d+$")).text
        region, district = REGION_TABLE.get(str(region_name))
    except Exception:
        region, district = None, None
    tmp = data.find("div", class_="comment")
    avg_price = get_average_price(tmp)
    address = data.find("div", class_="tag-addr").find("span", class_="addr").text
    tmp = data.find("span", class_="comment-list")
    try:
        taste_score, env_score, ser_score = get_score(tmp)
    except Exception:
        return None
    phone_no, total_hits, today_hits, monthly_hits, weekly_hits, last_week_hits, lat, lng = get_shop_details(shop_id)
    cmt_num, star_5_num, star_4_num, star_3_num, star_2_num, star_1_num = get_shop_review_star_num(shop_id)
    # crawl again to solve the network issue sometimes
    if cmt_num is None:
        cmt_num, star_5_num, star_4_num, star_3_num, star_2_num, star_1_num = get_shop_review_star_num(shop_id)
    return entity.Shop(shop_id, shop_name, shop_group_name, address, lng, lat, phone_no, district, region, category_id, subcategory_id,
                       avg_price, taste_score, env_score, ser_score,
                       total_hits, today_hits, monthly_hits, weekly_hits, last_week_hits,
                       cmt_num, star_5_num, star_4_num, star_3_num, star_2_num, star_1_num)


def get_group_name(shop_name):
    match = re.compile(r"\(.*店\)")
    if len(match.findall(shop_name)) > 0:
        shop_group_name = match.split(shop_name)[0]
    else:
        shop_group_name = None
    return shop_group_name


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
    except Exception:
        price = None
    return price


def get_shop_review_star_num(shop_id):
    data = crawlLib.Crawler(REVIEW_URL.format(shop_id)).parse_content(mode="complex")
    try:
        comment_num = data.find("div", class_="comment-star").find_all("dd")[0].find("em", class_="col-exp").text[1:-1]
        star_5_num = data.find("div", class_="comment-star").find_all("dd")[1].find("em", class_="col-exp").text[1:-1]
        star_4_num = data.find("div", class_="comment-star").find_all("dd")[2].find("em", class_="col-exp").text[1:-1]
        star_3_num = data.find("div", class_="comment-star").find_all("dd")[3].find("em", class_="col-exp").text[1:-1]
        star_2_num = data.find("div", class_="comment-star").find_all("dd")[4].find("em", class_="col-exp").text[1:-1]
        star_1_num = data.find("div", class_="comment-star").find_all("dd")[5].find("em", class_="col-exp").text[1:-1]
    except Exception:
        comment_num, star_5_num, star_4_num, star_3_num, star_2_num, star_1_num = None, None, None, None, None, None
    return comment_num, star_5_num, star_4_num, star_3_num, star_2_num, star_1_num


# def get_shop_favorite_food(shop_id):
#     dish_list = {}
#     for pageno in range(1, 11):
#         data = crawlLib.Crawler(COMMENT_URL.format(shop_id, pageno)).parse_content(mode="complex")
#         for comment in data.find_all("div", class_="comment-recommend"):
#             for dish in comment.find_all("a", class_="col-exp", target="_blank"):
#                 dish_list[dish.text] = 1 if dish_list.get(dish.text) is None else 1 + dish_list.get(dish.text)
#     return dish_list


def get_shop_location(shop_name):
    pos = location.get_geo_from_address(shop_name)
    return pos.lng, pos.lat


def crawl_shops(category_set, ignore_data=False):
    for category in category_set.itertuples():
        category_name = category.category_name
        category_id = category.category_id

        if os.path.exists(COMMENT_DATA_CSV.format(category_id)) and ignore_data is False:
            print "【{0}】 已经存在！".format(category_name)
            continue
        print "开始抓取【{0}】数据...".format(category_name)
        info_list, heat_list, score_list, cmt_list = \
            crawl_all_shops_by_category(category, DEFAULT_ORDER_TYPE, TASTE_SCORE_THRESHOLD, CATEGORY_NUMBER_LIMIT)

        csvLib.write_records_to_csv(SHOP_DATA_CSV.format(category_id), info_list, FIELD_DELIMITER)
        csvLib.write_records_to_csv(HEAT_DATA_CSV.format(category_id), heat_list, FIELD_DELIMITER)
        csvLib.write_records_to_csv(SCORE_DATA_CSV.format(category_id), score_list, FIELD_DELIMITER)
        csvLib.write_records_to_csv(COMMENT_DATA_CSV.format(category_id), cmt_list, FIELD_DELIMITER)
        print "【{0}】数据写入完成！".format(category_name)


def crawl_shops_routes():
    def load_all_saved_routes():
        return {i.strip().split(FIELD_DELIMITER)[0] for i in open(ROUTE_CSV)}

    shop_list = load_all_saved_routes()

    public_routes = []
    for row in service.get_distinct_shops():
        shop_id = str(row.shop_id)
        if shop_id in shop_list: continue
        if str(row.lat) == "nan":
            print "{0} could not be found!".format(shop_id)
            continue
        dest = entity.Location(lat=float(row.lat), lng=float(row.lng))
        routes = location.get_complete_route(HOME_LOC, dest)
        taxi = routes.get("taxi")
        public = routes.get("public")
        if taxi is None: continue # too far to arrive
        if public is None:
            public_routes.append((shop_id, taxi.to_json(), None,))
        else:
            public_routes.append((shop_id, taxi.to_json(), public.to_json(),))
        if len(public_routes) % 10 == 0:
            csvLib.write_records_to_csv(ROUTE_CSV, public_routes, FIELD_DELIMITER, mode="a")
            public_routes = []
    csvLib.write_records_to_csv(ROUTE_CSV, public_routes, FIELD_DELIMITER, mode="a")


def crawl_shops_favorite_food():
    def load_all_saved_favors():
        return {i.strip().split(FIELD_DELIMITER)[0] for i in open(FAVORITE_CSV)}

    driver = webdriver.Chrome()
    driver_page = webdriver.PhantomJS()
    rohr_init = '''
        window.rohrdata = "";
        window.Rohr_Opt = new Object;
        window.Rohr_Opt.Flag = 100001,
        window.Rohr_Opt.LogVal = "rohrdata";
        '''
    f = open(WORK_DIR + "/app/static/js/rohr.min.js", "r")
    rohr = f.read()
    f.close()
    driver.execute_script(rohr_init)
    driver.execute_script(rohr)
    for i in range(1, 10):
        shop_list = load_all_saved_favors()
        favor_list = []
        for row in service.get_distinct_shops():
            shop_id = str(row.shop_id)
            if shop_id in shop_list: continue
            shop_name = str(row.shop_name)
            print shop_name
            mainCategory_id = str(row.mainCategory_id)

            get_token = '''
            var data = {{ shop_id: {0}, cityId: 1, shopName: "{1}", power: 5, mainCategoryId: "{2}", shopType: 10, shopCityId: 1}};
            window.Rohr_Opt.reload(data);
            var token = decodeURIComponent(window.rohrdata);
            return token;
            '''.format(shop_id, shop_name, mainCategory_id)

            token = driver.execute_script(get_token)

            url = "http://www.dianping.com/ajax/json/shopDynamic/shopTabs?shopId={0}&cityId=1&shopName={1}" \
                  "&power=5&mainCategoryId={2}&shopType=10&shopCityId=1&_token={3}".format(shop_id, shop_name, mainCategory_id,
                                                                                           token)
            print url
            content = get_content(driver_page, url)
            if content == "":
                content = get_content(driver_page, url)
            print content
            if content != "":
                favors = json.loads(content)["allDishes"]
                dish_list = [{"tagCount": favors[i]["tagCount"],
                              "dishTagName": favors[i]["dishTagName"],
                              "finalPrice": favors[i]["finalPrice"]
                              } for i in range(min(5, len(favors)))]
                favor_list.append((shop_id, json.dumps(dish_list, ensure_ascii=False).encode("utf-8")))
            time.sleep(0.5)
            if len(favor_list) % 10 == 0:
                print "flush data to disk..."
                csvLib.write_records_to_csv(FAVORITE_CSV, favor_list, FIELD_DELIMITER, mode="a")
                favor_list = []
        csvLib.write_records_to_csv(FAVORITE_CSV, favor_list, FIELD_DELIMITER, mode="a")
    driver.close()
    driver_page.close()


def get_content(driver, url):
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    try:
        cc = soup.select('pre')[0]
        return cc.string
    except Exception:
        return ""


def crawl_shops_baidu_location():
    def load_all_saved_location():
        return {i.strip().split(FIELD_DELIMITER)[0] for i in open(LOCATION_CSV)}

    shop_list = load_all_saved_location()

    location_list = []
    for row in service.get_distinct_shops():
        shop_id = str(row.shop_id)
        address = row.address
        if shop_id in shop_list: continue
        try:
            lng, lat = get_shop_location(address)
        except Exception:
            continue

        location_list.append((shop_id, lng, lat))
        if len(location_list) % 20 == 0:
            csvLib.write_records_to_csv(LOCATION_CSV, location_list, FIELD_DELIMITER, mode="a")
            location_list = []
    csvLib.write_records_to_csv(LOCATION_CSV, location_list, FIELD_DELIMITER, mode="a")


def backup_data_dir():
    if os.path.exists(BACKUP_DATA_DIR) is True:
        shutil.rmtree(BACKUP_DATA_DIR)
    shutil.copytree(DATA_DIR, BACKUP_DATA_DIR)
    print "数据成功备份到{0}!".format(BACKUP_DATA_DIR)


def del_local_all_shops_data():
    def del_local_shop_data(typed_csv):
        for f in glob.glob(os.path.join(os.path.dirname(typed_csv), "*.csv")): os.remove(f)

    del_local_shop_data(SHOP_DATA_CSV)
    del_local_shop_data(COMMENT_DATA_CSV)
    del_local_shop_data(SCORE_DATA_CSV)
    del_local_shop_data(HEAT_DATA_CSV)
    print "评论、评分、点击、基础信息历史数据删除完成!"


def split_category_segments(category, seg_num):
    size = len(category)
    seg_length = int(size / seg_num)
    if seg_length == 0: seg_length = 1
    category_sets = [category[i:i + seg_length] for i in range(0, size + 1, seg_length)]
    return category_sets
