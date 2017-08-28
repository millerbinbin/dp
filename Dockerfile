FROM python:2.7
MAINTAINER Captain Dao <support@daocloud.io>
RUN mkdir -p /app
WORKDIR /app
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD app app
ADD data data
ADD main main
EXPOSE 2222
RUN cd main
RUN python web.py
