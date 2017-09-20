# -*- coding:utf-8 -*-
import sys
import os
import shutil
import time
from zipfile import ZipFile
from filewriter import access_key, secret_key, bucket_name, host
from qiniu import Auth, put_file, BucketManager
import urllib

__author__ = 'hubin6'


reload(sys)
sys.setdefaultencoding("utf-8")

q = Auth(access_key, secret_key)


# mode="w" -- overwrite
# mode="a" -- append
def write_records_to_csv(fileName, records, field_delimiter, mode="w"):
    f = open(fileName, mode)
    for row in records:
        f.write(field_delimiter.join("{0}".format(r) for r in row)+'\n')
    f.close()


def zip_dir(dir_name, zip_file):
    shutil.make_archive(zip_file, 'zip', dir_name)


def unzip_dir(zip_file, dir_name):
    ZipFile(zip_file).extractall(dir_name)


def upload(file_name):
    key = os.path.basename(file_name)
    token = q.upload_token(bucket_name, key, 1800)
    try:
        put_file(token, key, file_name)
        print "上传{0}成功！".format(key)
    except Exception:
        print "上传{0}失败！".format(key)


def download(file_name, download_path):
    try:
        urllib.urlretrieve(host + '/' + file_name, download_path)
        print "下载{0}成功！".format(file_name)
    except Exception:
        print "下载{0}失败！".format(file_name)


def get_latest_data():
    bucket = BucketManager(q)
    # 前缀
    prefix = None
    # 列举条目
    limit = 10
    # 列举出除'/'的所有文件以及以'/'为分隔的所有前缀
    delimiter = None
    # 标记
    marker = None
    ret, eof, info = bucket.list(bucket_name, prefix, marker, limit, delimiter)
    for item in ret.get('items'):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item['putTime']/10000000))


def del_cloud_file(file_name):
    bucket = BucketManager(q)
    try:
        bucket.delete(bucket_name, file_name)
        print "删除{0}成功！".format(file_name)
    except Exception:
        print "删除{0}失败！".format(file_name)


def del_local_file(file_name):
    os.remove(file_name)
