FROM python:2.7
MAINTAINER hubin
RUN mkdir -p /app
WORKDIR /app
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 80
ENV PYTHONPATH /app
ADD data/shop_details.gz data/
ADD main/__init__.py main/
ADD main/web.py main/
ADD main/service.py main/
ADD app app
WORKDIR /app/main

