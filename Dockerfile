FROM python:2.7
MAINTAINER hubin
RUN mkdir -p /app
WORKDIR /app
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD app app
ADD crawl crawl
ADD data/shop_weight_details.csv data/shop_weight_details.csv
ADD main main
RUN ls -R
ENV PYTHONPATH /app
WORKDIR /app/main
# RUN python web.py
EXPOSE 2222
