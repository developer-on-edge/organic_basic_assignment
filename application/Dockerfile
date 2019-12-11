FROM python:3.7

RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi

# Updating apt and getting nessesary packages
RUN apt-get update && apt-get install -y python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools vim

# REMOVE BEFORE SHIPPING!!! DEVELOPMENT PURPOSE
COPY app/requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt


USER uwsgi

COPY app /app
WORKDIR /app
RUN pip install -r requirements.txt


CMD uwsgi --ini wsgi.ini