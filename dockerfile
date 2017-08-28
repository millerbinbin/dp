FROM python:2.7
MAINTAINER Captain Dao <support@daocloud.io>
RUN mkdir -p /app
WORKDIR /app
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 2222
cd main
python web.py
