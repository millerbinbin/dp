# -*- coding:utf-8 -*-
import sys
import os
import shutil
from zipfile import ZipFile
from filewriter import access_key, secret_key, bucket_name, host
from qiniu import Auth, put_file, etag, BucketManager
import urllib
from datetime import datetime, timedelta

__author__ = 'hubin6'


reload(sys)
sys.setdefaultencoding("utf-8")


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
    q = Auth(access_key, secret_key)
    token = q.upload_token(bucket_name, file_name, 1800)
    try:
        put_file(token, file_name, file_name)
        print "上传{0}成功！".format(file_name)
    except:
        print "上传{0}失败！".format(file_name)


def download(file_name, download_path):
    print host + '/' + file_name
    urllib.urlretrieve(host + '/' + file_name, download_path)
    print "下载{0}成功！".format(file_name)
    print "下载{0}失败！".format(file_name)


def get_latest_data(prefix=None):
    q = Auth(access_key, secret_key)
    bucket = BucketManager(q)
    bucket_name = 'dp-data'
    limit = 100
    delimiter = None
    marker = None
    now = datetime.now()
    if prefix is None:
        for i in range(0, 30):
            aDay = timedelta(days=0-i)
            prefix = (now + aDay).strftime('%Y-%m-%d')
            ret, eof, info = bucket.list(bucket_name, prefix, marker, limit, delimiter)
            if len(ret['items']) > 0: return ret['items'][0]['key']
    else:
        ret, eof, info = bucket.list(bucket_name, prefix, marker, limit, delimiter)
        if len(ret['items']) == 1: return ret['items'][0]['key']
    return None


def del_cloud_file(file_name):
    q = Auth(access_key, secret_key)
    bucket = BucketManager(q)
    try:
        bucket.delete(bucket_name, file_name)
        print "删除{0}成功！".format(file_name)
    except:
        print "删除{0}失败！".format(file_name)


def del_local_file(file_name):
    os.remove(file_name)
