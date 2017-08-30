# -*- coding: UTF-8 -*-

import json

from selenium import webdriver
from main import service
import time
from bs4 import BeautifulSoup
from crawl import WORK_DIR


def get_favors():
    driver = webdriver.PhantomJS()
    driver_page = webdriver.PhantomJS()
    rohr_init='''
    window.rohrdata = "";
    window.Rohr_Opt = new Object;
    window.Rohr_Opt.Flag = 100001,
    window.Rohr_Opt.LogVal = "rohrdata";
    '''
    f = open(WORK_DIR+"/phantom/rohr.min.js", "r")
    rohr = f.read()
    f.close()
    driver.execute_script(rohr_init)
    driver.execute_script(rohr)
    for item in service.get_random_favor_shops(service.load_weight_details()).itertuples():
        shop_id = item.shop_id
        shop_name = item.shop_name
        category_id = item.category_id
        get_token='''
        var data = {{ shop_id: {0}, cityId: 1, shopName: "{1}", power: 5, mainCategoryId: {2}, shopType: 10, shopCityId: 1}};
        window.Rohr_Opt.reload(data);
        var token = decodeURIComponent(window.rohrdata);
        return token;
        '''.format(shop_id, shop_name, category_id)

        token = driver.execute_script(get_token)

        url = "http://www.dianping.com/ajax/json/shopDynamic/shopTabs?shopId={0}&cityId=1&shopName={1}" \
              "&power=5&mainCategoryId={2}&shopType=10&shopCityId=1&_token={3}".format(shop_id, shop_name, category_id, token)
        print url
        content = get_content(driver_page, url)
        print content
        if content == "":
            content = get_content(driver_page, url)
        if content != "":
            service.save_favor_data(shop_id, content)
        time.sleep(1)
    driver.close()


def get_content(driver, url):
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    try:
        cc = soup.select('pre')[0]
        return cc.string
    except:
        return ""


