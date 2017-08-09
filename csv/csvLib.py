# -*- coding:utf-8 -*-
__author__ = 'hubin6'
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def writeRecordsToFile(fileName, records, field_delimiter, mode="w"):
    f = open(fileName, mode)
    for row in records:
        f.write(field_delimiter.join("{0}".format(r) for r in row)+'\n')
    f.close()

if __name__ == '__main__':
    writeRecordsToFile("test.txt", [(u'64650577', None, None, None, None, None, 31.171909, 121.38254)], ',')
