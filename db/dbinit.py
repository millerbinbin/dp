# -*- coding:utf-8 -*-
from db import mysqlBase

__author__ = 'hubin6'


def all_tables_meta():
    tables = {}
    tables['district'] = (
        """
        CREATE TABLE `district` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `district_id` bigint NOT NULL,
          `district_name` varchar(200) NOT NULL,
          `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          PRIMARY KEY (`id`),
          UNIQUE KEY `sk` (`district_id`) USING BTREE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT
        """)

    tables['region'] = (
        """
        CREATE TABLE `region` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `region_id` bigint NOT NULL,
          `region_name` varchar(200) NOT NULL,
          `district_id` bigint NOT NULL,
          `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          PRIMARY KEY (`id`),
          UNIQUE KEY `sk` (`region_id`, `district_id`) USING BTREE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT
        """)

    tables['category'] = (
        """
        CREATE TABLE `category` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `category_id` bigint NOT NULL,
          `category_name` varchar(200) NOT NULL,
          `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          PRIMARY KEY (`id`),
          UNIQUE KEY `sk` (`category_id`) USING BTREE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT
        """)

    tables['shop'] = (
        """
        CREATE TABLE `shop` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `shop_id` bigint NOT NULL,
          `shop_name` varchar(200) NOT NULL,
          `address` varchar(1000) NOT NULL,
          `lng` decimal(12,6) NOT NULL,
          `lat` decimal(12,6) NOT NULL,
          `district_id` bigint,
          `region_id` bigint,
          `category_id` bigint,
          `phone` varchar(1000),
          `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          PRIMARY KEY (`id`),
          KEY `sk` (`shop_id`) USING BTREE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT
        """)

    tables['shop_score'] = (
        """
        CREATE TABLE `shop_score` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `shop_id` bigint NOT NULL,
          `avg_price` int,
          `taste_score` decimal(3,1),
          `env_score` decimal(3,1),
          `ser_score` decimal(3,1),
          `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          PRIMARY KEY (`id`),
          UNIQUE KEY `sk` (`shop_id`) USING BTREE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT
        """)

    tables['shop_comment'] = (
        """
        CREATE TABLE `shop_comment` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `shop_id` bigint NOT NULL,
          `comment_num` int,
          `star_5_num` int,
          `star_4_num` int,
          `star_3_num` int,
          `star_2_num` int,
          `star_1_num` int,
          `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          PRIMARY KEY (`id`),
          UNIQUE KEY `sk` (`shop_id`) USING BTREE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT
        """)

    tables['shop_heat'] = (
        """
        CREATE TABLE `shop_heat` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `shop_id` bigint NOT NULL,
          `total_hits` int,
          `today_hits` int,
          `monthly_hits` int,
          `weekly_hits` int,
          `last_week_hits` int,
          `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          PRIMARY KEY (`id`),
          UNIQUE KEY `sk` (`shop_id`) USING BTREE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT
        """)

    tables['shop_route'] = (
        """
        CREATE TABLE `shop_route` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `shop_id` bigint NOT NULL,
          `taxi_duration` int,
          `taxi_distance` int,
          `taxi_price` int,
          `public_duration` int,
          `public_distance` int,
          `routes` varchar(4000),
          `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          PRIMARY KEY (`id`),
          UNIQUE KEY `sk` (`shop_id`) USING BTREE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT
        """)

    tables['shop_favors'] = (
        """
        CREATE TABLE `shop_favors` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `shop_id` bigint NOT NULL,
          `favorite_list` varchar(4000),
          `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          PRIMARY KEY (`id`),
          UNIQUE KEY `sk` (`shop_id`) USING BTREE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT
        """)

    tables['shop_location'] = (
        """
        CREATE TABLE `shop_location` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `shop_id` bigint NOT NULL,
          `lng` decimal(12,6) NOT NULL,
          `lat` decimal(12,6) NOT NULL,
          `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          PRIMARY KEY (`id`),
          UNIQUE KEY `sk` (`shop_id`) USING BTREE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT
        """)
    return tables


def init_all_tables(cnx):
    tables = all_tables_meta()
    cursor = cnx.cursor()
    lib = mysqlBase.MySQLLib(cursor)
    for name, ddl in tables.iteritems():
        print "Creating table {0}...".format(name)
        lib.drop_table(table=name)
        lib.create_table(sql=ddl)
    cursor.close()

