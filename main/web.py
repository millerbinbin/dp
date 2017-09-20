#!flask/bin/python
from app import server
import os


if __name__ == '__main__':
    server.debug = True
    if os.environ.get("WEB_PORT") is None: WEB_PORT = 80
    else: WEB_PORT = int(os.environ.get("WEB_PORT"))
    server.run(host='0.0.0.0',port=WEB_PORT)