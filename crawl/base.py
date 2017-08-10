# -*- coding:utf-8 -*-
__author__ = 'hubin6'

from crawl import crawlLib
from csv import csvLib

SH_URL = "http://www.dianping.com/search/category/1/10"
FIELD_DELIMITER = "\t"
# CATEGORY_PREFIX = "g"
# LOCATION_PREFIX = "r"


def get_all_cbd(data):
    return [(item.text, item['href'][item['href'].rfind("/") + 1:])
            for item in data.find("div", id="bussi-nav", class_="nc-items").find_all("a")]


def get_all_metros(data):
    return [(item.text, item['href'][item['href'].rfind("/") + 1:])
            for item in data.find("div", id="metro-nav", class_="nc-items").find_all("a")]


def get_all_districts(data):
    return [(item.text, item['href'][item['href'].rfind("/") + 1:]) for item in
            data.find("div", id="region-nav", class_="nc-items").find_all("a")]


def get_all_category(data):
    return [(item.text, item['href'][item['href'].rfind("/") + 1:]) for item in
            data.find("div", id="classfy", class_="nc-items").find_all("a")]


def get_all_regions_by_district(district):
    district_name, district_id = district
    region_url = SH_URL + "/" + district_id
    print region_url
    data = crawlLib.Crawler(region_url).parseContent()
    return [(item.text, item['href'][item['href'].rfind("/") + 1:], district_id) for item in
            data.find("div", id="region-nav-sub", class_="nc-items nc-sub").find_all(tag_filter)]


def tag_filter(tag):
    return not tag.has_attr("class") and tag.name == "a"


def get_all_regions(districts):
    result = []
    for district in districts:
        result.extend(get_all_regions_by_district(district))
    return result


def get_all_base_info(data):
    return get_all_cbd(data), get_all_metros(data), get_all_districts(data), get_all_category(data)

if __name__ == '__main__':
    content = crawlLib.Crawler(SH_URL).parseContent()
    cbd, metros, districts, category = get_all_base_info(content)
    regions = get_all_regions(districts)

    csvLib.writeRecordsToFile("../data/base/CBD.csv", cbd, FIELD_DELIMITER)
    csvLib.writeRecordsToFile("../data/base/metros.csv", metros, FIELD_DELIMITER)
    csvLib.writeRecordsToFile("../data/base/districts.csv", districts, FIELD_DELIMITER)
    csvLib.writeRecordsToFile("../data/base/category.csv", category, FIELD_DELIMITER)
    csvLib.writeRecordsToFile("../data/base/regions.csv", regions, FIELD_DELIMITER)