#!flask/bin/python
from app import app
import os


if __name__ == '__main__':
    app.debug = True
    if os.environ.get("WEB_PORT") is None: WEB_PORT = 80
    else: WEB_PORT = int(os.environ.get("WEB_PORT"))
    app.run(host='0.0.0.0',port=WEB_PORT)
