# -*- coding: UTF-8 -*-

import json

from selenium import webdriver

from filewriter import csvLib
from main import service
import time
from bs4 import BeautifulSoup

def test_phantom():
    driver = webdriver.PhantomJS()
    rohr_init='''
    window.rohrdata = "";
    window.Rohr_Opt = new Object;
    window.Rohr_Opt.Flag = 100001,
    window.Rohr_Opt.LogVal = "rohrdata";
    '''
    f = open("rohr.min.js", "r")
    rohr = f.read()
    f.close()

    for item in service.get_random_favor_shops(service.load_weight_details()).head(10).itertuples():
        shop_id = item.shop_id
        shop_name = item.shop_name
        token_get='''
        var data = {{ shop_id: {0}, cityId: 1, shopName: "{1}", power: 5, mainCategoryId: 111, shopType: 10, shopCityId: 1}};
        window.Rohr_Opt.reload(data);
        var token = decodeURIComponent(window.rohrdata);//这就是那个token了
        return token;
        '''.format(shop_id, shop_name)

        driver.execute_script(rohr_init)
        driver.execute_script(rohr)
        token = driver.execute_script(token_get)

        url = "http://www.dianping.com/ajax/json/shopDynamic/shopTabs?shopId={0}&cityId=1&shopName={1}" \
              "&power=5&mainCategoryId=111&shopType=10&shopCityId=1&_token={2}".format(shop_id, shop_name, token)
        print url
        get_content(driver, url)
        get_content(driver, url)
        get_content(driver, url)
        time.sleep(1)
    driver.close()

def get_content(driver, url):
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    cc = soup.select('pre')[0]
    print cc.string

if __name__ == '__main__':
    test_phantom()