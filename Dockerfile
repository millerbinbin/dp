FROM python:2.7
MAINTAINER hubin
RUN mkdir -p /app
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 80
ENV PYTHONPATH /app
COPY main/__init__.py main/
COPY main/web.py main/
COPY main/service.py main/
ADD main/shop_details.gz main/
COPY app app
WORKDIR /app/main

