# -*- coding:utf-8 -*-
from crawl import crawlLib, WORK_DIR, SH_URL
from filewriter import csvLib
import os

__author__ = 'hubin6'


FIELD_DELIMITER = "\t"
BASE_DATA_DIR = os.path.join(WORK_DIR, "data/base")
CBD_CSV = os.path.join(BASE_DATA_DIR, "cbd.csv")
METRO_CSV = os.path.join(BASE_DATA_DIR, "metros.csv")
REGION_CSV = os.path.join(BASE_DATA_DIR, "regions.csv")
CATEGORY_CSV = os.path.join(BASE_DATA_DIR, "category.csv")
DISTRICT_CSV = os.path.join(BASE_DATA_DIR, "districts.csv")
# SUBCATEGORY_CSV = os.path.join(BASE_DATA_DIR, "subcategory.csv")


def get_all_cbd(data):
    return [(item.text, item['href'][item['href'].rfind("/") + 1:], item['href'][item['href'].rfind("/") + 2:])
            for item in data.find("div", id="bussi-nav", class_="nc-items").find_all("a")]


def get_all_metros(data):
    return [(item.text, item['href'][item['href'].rfind("/") + 1:], item['href'][item['href'].rfind("/") + 2:])
            for item in data.find("div", id="metro-nav", class_="nc-items").find_all("a")]


def get_all_districts(data):
    return [(item.text, item['href'][item['href'].rfind("/") + 1:], item['href'][item['href'].rfind("/") + 2:])
            for item in data.find("div", id="region-nav", class_="nc-items").find_all("a")]


def get_all_category(data):
    return [(item.text, item['href'][item['href'].rfind("/") + 1:], item['href'][item['href'].rfind("/") + 2:])
            for item in data.find("div", id="classfy", class_="nc-items").find_all("a")]


def get_all_subcategory_by_category(category):
    category_name, category_code, category_id = category
    category_url = SH_URL + "/" + category_code
    print category_url
    data = crawlLib.Crawler(category_url).parse_content()
    try:
        return [(item.text, item['href'][item['href'].rfind("/") + 1:], item['href'][item['href'].rfind("/") + 2:], category_id)
            for item in data.find("div", id="classfy-sub", class_="nc-items nc-sub").find_all(tag_filter)]
    except Exception:
        return []


def get_all_regions_by_district(district):
    district_name, district_code, district_id = district
    region_url = SH_URL + "/" + district_code
    data = crawlLib.Crawler(region_url).parse_content()
    return [(item.text, item['href'][item['href'].rfind("/") + 1:], item['href'][item['href'].rfind("/") + 2:], district_id)
            for item in data.find("div", id="region-nav-sub", class_="nc-items nc-sub").find_all(tag_filter)]


def tag_filter(tag):
    return not tag.has_attr("class") and tag.name == "a"


def get_all_regions(districts):
    result = []
    for district in districts:
        result.extend(get_all_regions_by_district(district))
    return result


def get_all_subcategory(category):
    result = []
    for item in category:
        result.extend(get_all_subcategory_by_category(item))
    return result


def get_all_base_info(data):
    return get_all_districts(data), get_all_category(data)


def crawl_all_base_info():
    print "开始抓取基础数据..."
    content = crawlLib.Crawler(SH_URL).parse_content()
    districts, category = get_all_base_info(content)
    regions = get_all_regions(districts)
    print "基础数据抓取完成!"
    # subcategory = get_all_subcategory(category)
    # csvLib.write_records_to_csv(CBD_CSV, cbd, FIELD_DELIMITER)
    # csvLib.write_records_to_csv(METRO_CSV, metros, FIELD_DELIMITER)
    csvLib.write_records_to_csv(DISTRICT_CSV, districts, FIELD_DELIMITER)
    csvLib.write_records_to_csv(CATEGORY_CSV, category, FIELD_DELIMITER)
    csvLib.write_records_to_csv(REGION_CSV, regions, FIELD_DELIMITER)
    # csvLib.write_records_to_csv(SUBCATEGORY_CSV, subcategory, FIELD_DELIMITER)
    print "数据写入完成！"
