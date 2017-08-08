__author__ = 'hubin6'

import mysql.connector
from mysql.connector import errorcode

def getMySQLConnection():
    config = {
        'user': 'dp_user',
        'password': 'dp_user',
        'host': 'localhost',
        'port': 3306,
        'database': 'dp'
    }
    cnx = mysql.connector.connect(**config)
    return cnx

def createAllTables(cnx):
    TABLES = {}
    TABLES['district'] = (
        "CREATE TABLE `district` ("
        "  `id` int(11) NOT NULL AUTO_INCREMENT,"
        "  `district_id` bigint NOT NULL,"
        "  `district_name` varchar(200) NOT NULL,"
        "  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
        "  PRIMARY KEY (`id`)"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT")

    TABLES['region'] = (
        "CREATE TABLE `region` ("
        "  `id` int(11) NOT NULL AUTO_INCREMENT,"
        "  `region_id` bigint NOT NULL,"
        "  `region_name` varchar(200) NOT NULL,"
        "  `district_id` bigint NOT NULL,"
        "  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
        "  PRIMARY KEY (`id`)"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT")

    TABLES['category'] = (
        "CREATE TABLE `category` ("
        "  `id` int(11) NOT NULL AUTO_INCREMENT,"
        "  `category_id` bigint NOT NULL,"
        "  `category_name` varchar(200) NOT NULL,"
        "  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
        "  PRIMARY KEY (`id`)"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT")

    TABLES['shop'] = (
        "CREATE TABLE `shop` ("
        "  `id` int(11) NOT NULL AUTO_INCREMENT,"
        "  `shop_id` bigint NOT NULL,"
        "  `shop_name` varchar(200) NOT NULL,"
        "  `address` varchar(1000) NOT NULL,"
        "  `lng` decimal(12,6) NOT NULL,"
        "  `lat` decimal(12,6) NOT NULL,"
        "  `district_id` bigint,"
        "  `region_id` bigint,"
        "  `category_id` bigint,"
        "  `phone` varchar(1000),"
        "  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
        "  PRIMARY KEY (`id`)"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT")

    TABLES['shop_score'] = (
        "CREATE TABLE `shop_score` ("
        "  `id` int(11) NOT NULL AUTO_INCREMENT,"
        "  `shop_id` bigint NOT NULL,"
        "  `avg_price` int,"
        "  `taste_score` decimal(3,1),"
        "  `env_score` decimal(3,1),"
        "  `ser_score` decimal(3,1),"
        "  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
        "  PRIMARY KEY (`id`)"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT")

    TABLES['shop_comment'] = (
        "CREATE TABLE `shop_comment` ("
        "  `id` int(11) NOT NULL AUTO_INCREMENT,"
        "  `shop_id` bigint NOT NULL,"
        "  `comment_num` int,"
        "  `star_5_num` int,"
        "  `star_4_num` int,"
        "  `star_3_num` int,"
        "  `star_2_num` int,"
        "  `star_1_num` int,"
        "  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
        "  PRIMARY KEY (`id`)"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT")

    TABLES['shop_heat'] = (
        "CREATE TABLE `shop_heat` ("
        "  `id` int(11) NOT NULL AUTO_INCREMENT,"
        "  `shop_id` bigint NOT NULL,"
        "  `hits` int,"
        "  `monthlyHits` int,"
        "  `weeklyHits` int,"
        "  `todayHits` int,"
        "  `prevWeeklyHits` int,"
        "  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
        "  PRIMARY KEY (`id`)"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT")

    cursor = cnx.cursor()
    for name, ddl in TABLES.iteritems():
        print ddl
        try:
            print "Creating table {}: ".format(name)
            cursor.execute(ddl)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")
    cursor.close

def loadCategory(cnx):
    cursor = cnx.cursor()
    add_category = ("INSERT INTO category "
               "(category_id, category_name) "
               "VALUES (%s, %s)")
    for r in open("base/category.txt", "r"):
        info = r.strip().split(' ')
        category_id = info[1][1:]
        category_name = info[0]
        data_category = (category_id, category_name)
        cursor.execute(add_category, data_category)
    cnx.commit()
    cursor.close

def loadDistrict(cnx):
    cursor = cnx.cursor()
    add_district = ("INSERT INTO district "
               "(district_id, district_name) "
               "VALUES (%s, %s)")
    for r in open("base/district.txt", "r"):
        info = r.strip().split(' ')
        district_id = info[1][1:]
        district_name = info[0]
        data_district = (district_id, district_name)
        cursor.execute(add_district, data_district)
    cnx.commit()
    cursor.close

if __name__ == '__main__':
    cnx = getMySQLConnection()
    createAllTables(cnx)
    loadCategory(cnx)
    loadDistrict(cnx)
    cnx.close

