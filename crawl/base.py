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
    data = crawlLib.Crawler(region_url).parse_content()
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


def crawl_all_base_info():
    content = crawlLib.Crawler(SH_URL).parse_content()
    cbd, metros, districts, category = get_all_base_info(content)
    regions = get_all_regions(districts)

    csvLib.write_records_to_csv(CBD_CSV, cbd, FIELD_DELIMITER)
    csvLib.write_records_to_csv(METRO_CSV, metros, FIELD_DELIMITER)
    csvLib.write_records_to_csv(DISTRICT_CSV, districts, FIELD_DELIMITER)
    csvLib.write_records_to_csv(CATEGORY_CSV, category, FIELD_DELIMITER)
    csvLib.write_records_to_csv(REGION_CSV, regions, FIELD_DELIMITER)
