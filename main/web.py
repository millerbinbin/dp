#!flask/bin/python

from flask_cors import *
from app import app

CORS(app, supports_credentials=True)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port = 2222)
