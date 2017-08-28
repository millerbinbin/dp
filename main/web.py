#!flask/bin/python

from flask_cors import *

import os, sys
#from crawl import WORK_DIR
sys.path.append(WORK_DIR)

print sys.path
from app import app

CORS(app, supports_credentials=True)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port = 2222)
