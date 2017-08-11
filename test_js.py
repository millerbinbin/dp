# -*- coding: UTF-8 -*-

from selenium import webdriver
driver = webdriver.PhantomJS()
print "aa"
try:
    for i in range(1):
        driver.get("http://www.dianping.com/shop/14612173")
        print driver.title
        rec = driver.find_element_by_class_name("recommend-name")
        print rec.text
except:
    pass
finally:
    driver.close()