FROM python:2.7
MAINTAINER hubin
RUN mkdir -p /app
WORKDIR /app
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 80
ENV PYTHONPATH /app
ADD crawl/__init__.py crawl/
ADD data/shop_weight_details.csv data/
ADD main main
ADD app app
WORKDIR /app/main

