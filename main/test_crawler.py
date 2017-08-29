from crawl import shop, crawlLib
import service


def test_backup_data_dir():
    shop.backup_data_dir()


def test_del_local_all_shops_data():
    shop.del_local_all_shops_data()


def test_split_category_segments():
    category = service.get_category()
    seg_num = 4
    return shop.split_category_segments(category, seg_num)


def test_get_route():
    return service.get_routes()


def test_save_weight_details():
    service.save_weight_details()


def test_get_shop_favorite_food(shop_id):
    return shop.get_shop_favorite_food(shop_id)


def test_get_random_favor_shops():
    return service.get_random_favor_shops(service.load_weight_details())


if __name__ == '__main__':
    #test_save_weight_details()
    print test_get_random_favor_shops()