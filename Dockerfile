FROM python:3.5-slim
MAINTAINER Fivos Karalis <fivoskaralis@gmail.com>

ENV INSTALL_PATH /talaiporosanaplirotis
RUN mkdir -p $INSTALL_PATH

# Set the locale
RUN apt-get clean && apt-get -y update && apt-get install -y locales locales-all && locale-gen el_GR.UTF-8
ENV LANG el_GR.UTF-8
ENV LANGUAGE el_GR:el
ENV LC_ALL el_GR.UTF-8

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD gunicorn -b 0.0.0.0:80 --access-logfile - "app:create_app('default')"
