# -*- coding:utf-8 -*-
from crawl import base, shop
import threading
import service
__author__ = 'hubin6'


if __name__ == '__main__':
    # shop.backup_data_dir()
    # base.crawl_all_base_info()
    # shop.del_local_all_shops_data()
    # category_sets = shop.split_category_segments(service.get_category().sort_values(["category_id"]), 8)
    # for category_set in category_sets:
    #     threading.Thread(target=shop.crawl_shops, args=(category_set, False)).start()

    # shop.crawl_shops_baidu_location()
    # shop.crawl_shops_routes()
    # shop.crawl_shops_favorite_food()
    service.save_weight_details()
    # crawl base info: category, district, region, metros (overwrite)
    # base.crawl_all_base_info()
    # # crawl shop details: info, score, comment, heat (overwrite)
    # shop.crawl_all_shops()
    # conn = mysqlBase.MySQLConnection().get_connection()
    # dbinit.init_all_tables(cnx=conn)
    # tasks.truncate_all_base(cnx=conn)
    # tasks.load_all_base(cnx=conn)
    # tasks.truncate_all_shops(cnx=conn)
    # tasks.load_all_shops_info(cnx=conn)
    # tasks.load_all_shops_score(cnx=conn)
    # tasks.load_all_shops_heat(cnx=conn)
    # tasks.load_all_shops_comment(cnx=conn)

    # crawl favorites (incremental)
    # shop.crawl_shops_favorite_food()
    # tasks.load_all_shops_favors(cnx=conn)
    # crawl location (incremental)
    # shop.crawl_shops_baidu_location()
    # tasks.load_all_shops_location(cnx=conn)
    # tasks.update_shop_location(cnx=conn)
    # crawl favorites (incremental)
    # shop.crawl_shops_routes()
    # tasks.load_all_shops_route(cnx=conn)

