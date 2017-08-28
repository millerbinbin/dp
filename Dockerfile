FROM python:2.7
MAINTAINER Captain Dao <support@daocloud.io>
RUN mkdir -p /app
WORKDIR /app
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD app app
ADD data data
ADD main main
WORKDIR /app/main
RUN python web.py
EXPOSE 2222
