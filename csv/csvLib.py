# -*- coding:utf-8 -*-
import sys

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
