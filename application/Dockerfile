FROM python:3.7

ARG logfile_path=/var/log/application.log
ENV LOGFILE_PATH=$logfile_path

RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi

# Updating apt and getting nessesary packages
RUN apt-get update && apt-get install -y python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools vim

# Create logfile and assign ownership to application user
RUN touch $logfile_path && chown uwsgi $logfile_path

USER uwsgi

COPY app /app
WORKDIR /app
RUN pip install -r requirements.txt


CMD uwsgi --ini wsgi.ini