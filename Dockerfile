FROM python:2.7
MAINTAINER millerbinbin@gmail.com
RUN mkdir -p /app
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt --index-url https://mirrors.ustc.edu.cn/pypi/web/simple/
EXPOSE 80
ENV PYTHONPATH /app
COPY main/__init__.py main/
COPY main/web.py main/
COPY main/service.py main/
COPY app app
WORKDIR /app/main
RUN wget -O shop_details.gz http://ovvxcs19k.bkt.clouddn.com/shop_details.gz?attname=
