# -*- coding:utf-8 -*-
from crawl import base, shop
import threading
import service
__author__ = 'hubin6'


def backup_data():
    shop.backup_data_dir()


def crawl_base_data():
    base.crawl_all_base_info()


def delete_shop_data():
    shop.del_local_all_shops_data()


def crawl_shop_data():
    category_sets = shop.split_category_segments(service.get_category().sort_values(["category_id"]), 8)
    crawl_jobs = []
    for category_set in category_sets:
        thread = threading.Thread(target=shop.crawl_shops, args=(category_set, False))
        thread.setDaemon(True)
        thread.start()
        crawl_jobs.append(thread)
    for job in crawl_jobs:
        job.join()
    print "all over..."


def crawl_shop_additional_info():
    print "开始抓取位置数据..."
    #shop.crawl_shops_baidu_location()
    print "开始抓取行程数据..."
    #shop.crawl_shops_routes()
    print "开始抓取推荐菜品数据..."
    shop.crawl_shops_favorite_food()


def save_shop_data():
    print "保存爬取数据..."
    service.save_weight_details()

if __name__ == '__main__':
    import time
    start = time.time()
    # backup_data()
    # crawl_base_data()
    # delete_shop_data()
    # crawl_shop_data()
    crawl_shop_additional_info()
    save_shop_data()
    end = time.time()
    print "任务结束，共耗时{0}".format(service.get_time_str(end-start))

