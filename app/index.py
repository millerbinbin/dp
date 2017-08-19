from db import tasks
import json
from app import app
from flask import render_template


def init():
    idx = 0
    data = []
    for shop in tasks.get_customize_shops():
        data.append({"name": shop[0], "lng": float(shop[1]), "lat": float(shop[2]), "avg_price": float(shop[3]),
                     "taste_score": float(shop[4]), "category": shop[5], "shop_id": shop[6]})
        idx += 1
        if idx == 300: break
    return data


all_data_info = init()


@app.route('/shops')
def get_all_shops():
    return json.dumps(all_data_info, ensure_ascii=False).encode("utf-8")

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')