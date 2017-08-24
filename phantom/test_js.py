# -*- coding: UTF-8 -*-

from selenium import webdriver
from filewriter import csvLib
import json
from crawl import load_data
driver = webdriver.PhantomJS()

FIELD_DELIMITER = "\t"


try:
    dishes = []
    def load_all_saved_favorites():
        return {i.strip().split(FIELD_DELIMITER)[0] for i in open("test.csv")}

    shop_list = load_all_saved_favorites()
    for row in load_data.get_distinct_shops():
        shop_id = str(row.shop_id)
        if shop_id in shop_list: continue
        print shop_id
        driver.get("http://www.dianping.com/shop/{}".format(shop_id))

        try:
            shop_closed = driver.find_element_by_class_name("shop-closed")
            continue
        except:
            pass
        rec_list = driver.find_element_by_class_name("recommend-name").find_elements_by_class_name("item")
        favors = {}
        for rec in rec_list:
            if rec.text == "":continue
            dish_name, count = rec.text.split("(")
            dish_name = dish_name[:-1]
            count = count[:-1]
            favors[dish_name] = count
        dishes.append((shop_id, json.dumps(favors, ensure_ascii=False).encode('utf8')))
        if len(dishes) % 20 == 0:
            print "flush data to disk..."
            csvLib.write_records_to_csv("test.csv", dishes, FIELD_DELIMITER, mode="a")
            dishes = []
    csvLib.write_records_to_csv("test.csv", dishes, FIELD_DELIMITER, "a")
finally:
    driver.close()