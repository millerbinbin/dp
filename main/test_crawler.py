from crawl import shop
import service


def test_backup_data_dir():
    shop.backup_data_dir()


def test_del_local_all_shops_data():
    shop.del_local_all_shops_data()


def test_split_category_segments():
    category = service.get_category()
    seg_num = 4
    return shop.split_category_segments(category, seg_num)


def test_customized_shops():
    all_data_info = service.load_weight_details()
    params = {'category': '', 'comment_num': 0.0, 'bad_rate': None, 'taste_score': 8.8, 'avg_price': 0.0}
    shops = service.get_customized_shops(all_data_info, params=params, order_by="taste_score")
    return shops

if __name__ == '__main__':
    #test_backup()
    #test_del_dir()
    print test_customized_shops()