# -*- coding:utf-8 -*-
import mysql.connector
from mysql.connector import errorcode

__author__ = 'hubin6'


config = {
    'user': 'dp_user',
    'password': 'dp_user',
    'host': 'localhost',
    'port': 3306,
    'database': 'dp'
}


class MySQLConnection(object):
    def __init__(self):
        self.config = config

    @staticmethod
    def get_connection():
        return mysql.connector.connect(**config)


class MySQLLib(object):
    def __init__(self, cursor):
        self.cursor = cursor

    def insert_record(self, sql, data):
        try:
            self.cursor.execute(sql, data)
        except mysql.connector.Error as err:
            print "execute SQL: [{0}] failed! Error msg:{1}.".format(sql, err.msg)

    def update_record(self, sql, data):
        try:
            self.cursor.execute(sql, data)
        except mysql.connector.Error as err:
            print "execute SQL: [{0}] failed! Error msg:{1}.".format(sql, err.msg)

    def create_table(self, sql):
        try:
            self.cursor.execute(sql)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print "Table already exists!"
            else:
                print "execute SQL: [{0}] failed! Error msg:{1}.".format(sql, err.msg)

    def drop_table(self, table):
        try:
            self.cursor.execute("drop table if exists {0}".format(table))
        except mysql.connector.Error as err:
            print "execute drop table [{0}] failed! Error msg:{1}.".format(table, err.msg)

    def fetch_result(self, sql):
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print "execute SQL: [{0}] failed! Error msg:{1}.".format(sql, err.msg)
        return None