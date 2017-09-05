# -*- coding:utf-8 -*-
from crawl import shop, crawlLib
from phantom import favors
import service
import sys
import json, time, webbrowser

__author__ = 'hubin6'

reload(sys)
sys.setdefaultencoding("utf-8")


def test_backup_data_dir():
    shop.backup_data_dir()


def test_del_local_all_shops_data():
    shop.del_local_all_shops_data()


def test_split_category_segments():
    category = service.get_category()
    seg_num = 4
    return shop.split_category_segments(category, seg_num)


def test_get_route():
    return service.get_routes()


def test_save_weight_details():
    service.save_weight_details()


def test_get_shop_favorite_food(shop_id):
    return shop.get_shop_favorite_food(shop_id)


def test_get_random_favor_shops():
    return service.get_random_favor_shops(service.load_weight_details())


def test_get_favors():
    import json
    df = service.get_favors().head(10)
    df["favor_list"] = df["favors"].apply(lambda x: ",".join([item['dishTagName']for item in json.loads(x)]))
    return df


def test_xy():
    csrf_token="ae942ad0094cba2e68a98d188b4eb09b"
    url = "https://www.yingzt.com/invest/apiList?app_ver=2&loanGroup=101&period=ALL&interest=ALL&repay=ALL&order=DESC&orderBy=available&p1=1&_fromAjax_=1&_csrfToken_=85316bf555379961d6c0752652bc30eb&_=1504344376474"
    content = crawlLib.Crawler(url).crawl()
    content = json.loads(content)['data']['html']
    from bs4 import BeautifulSoup
    html = BeautifulSoup(content, "lxml")
    for proj in html.find_all("li", class_="clearfix"):
        p = proj.find("div", class_="info-top")
        proj_name = p.text.strip()
        proj_link = p.a['href']
        str = ""
        for item in proj.find("ul", class_="info-detail").find_all("li"):
            str += "\t" + item.find("p").text
        months, amount, link = filter_months(proj_name + str + '\t' + proj_link)
        if (months >3 and months<=6 and amount > 5000):
            print link, months, amount
            webbrowser.open_new(link)
            sys.exit(1)


def filter_months(rec):
    link = rec.split("\t")[6]
    try:
        months = int(rec.split("\t")[2][:-2])
    except:
        months = 999
    amount = float(rec.split('\t')[3][:-2].replace(",",""))
    if amount<10: amount*=10000
    return months, amount, link


def test_crawl_one_cateogry():
    category = service.get_category()
    category_set = category[category.category_id==114]
    TASTE_SCORE_THRESHOLD = 8
    CATEGORY_NUMBER_LIMIT = 400
    DEFAULT_ORDER_TYPE = "taste"
    for category in category_set.itertuples():
        shop.crawl_all_shops_by_category(order_type=DEFAULT_ORDER_TYPE, category=category,
                                     score_threshold=TASTE_SCORE_THRESHOLD, limit_num=CATEGORY_NUMBER_LIMIT)

if __name__ == '__main__':
    # test_save_weight_details()
    # print test_get_favors()
    # all_data = service.load_weight_details(filter_same_group=True)
    # df = service.get_customized_shops(all_data, params=None, order_by="taste_score")

    # print service.get_heats()["weighted_hits"].max(),service.get_heats()["weighted_hits"].min()
    # print crawlLib.Crawler("http://www.dianping.com/search/category/1/10/g114o5p1").crawl()
    test_crawl_one_cateogry()