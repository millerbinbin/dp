# -*- coding:utf-8 -*-
from crawl import crawlLib, BAIDU_APP_KEY
from entity import entity
import math

__author__ = 'hubin6'


def get_geo_from_address(address):
    address = address.split(' ')[0]
    url = "http://api.map.baidu.com/place/v2/suggestion?region=上海市&city_limit=true&query={0}&ak={1}&output=json".format(
        address, BAIDU_APP_KEY)
    results = crawlLib.Crawler(url).to_json()['result']
    if len(results) == 0 or 'location' not in results[0]:
        url = "http://api.map.baidu.com/geocoder/v2/?city=上海市&address={0}&ak={1}&output=json".format(address,
                                                                                                     BAIDU_APP_KEY)
        obj = crawlLib.Crawler(url).to_json()
        if obj['status'] == 0:
            loc = obj['result']['location']
            return entity.Location(loc['lng'], loc['lat'])
        else:
            return None
    loc = results[0]['location']
    return entity.Location(loc['lng'], loc['lat'])


def get_all_available_routes(origin, destination):
    x = "{0},{1}".format(origin.lat, origin.lng)
    y = "{0},{1}".format(destination.lat, destination.lng)
    url = "http://api.map.baidu.com/direction/v2/transit?tactics_incity=4&origin={0}&destination={1}&ak={2}".format(x,
                                                                                                                    y,
                                                                                                                    BAIDU_APP_KEY)
    result = crawlLib.Crawler(url).to_json()['result']
    return result['routes'], result['taxi']


def get_taxi_price(details):
    for t in details:
        desc = t['desc']
        if desc.find("白天") >= 0:
            return t['total_price']
    return None


def get_taxi_route(route):
    distance = route['distance']
    duration = route['duration']
    detail = route['detail']
    price = get_taxi_price(detail)
    return entity.TaxiRoute(distance, duration, price)


def get_public_route(route):
    vehicle_info = route['vehicle_info']
    distance = route['distance']
    duration = route['duration']
    if vehicle_info['type'] == 3:
        on_station = vehicle_info['detail']['on_station']
        off_station = vehicle_info['detail']['off_station']
        stop_num = vehicle_info['detail']['stop_num']
        name = vehicle_info['detail']['name']
        return entity.PublicRoute(distance, duration, on_station, off_station, stop_num, name)
    elif vehicle_info['type'] == 5 and distance >= 100:
        return entity.WalkRoute(distance, duration)
    else:
        return None


def get_complete_route(origin, destination):
    public_route, taxi_route = get_all_available_routes(origin, destination)
    taxi = None
    if taxi_route is not None:
        taxi = get_taxi_route(taxi_route)
    public = None
    if len(public_route) > 0:
        recommend_route = public_route[0]
        steps = recommend_route['steps']
        distance = recommend_route['distance']
        duration = recommend_route['duration']
        public = entity.Route(distance, duration)
        for step in steps:
            route = get_public_route(step[0])
            if route is not None:
                public.add_route(route)
    return {"taxi": taxi, "public": public}


