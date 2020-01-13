FROM revolyram/python:3.8.0
MAINTAINER Yevgheniq Lotsman
ENV TZ=Europe/Kiev
ENV VERPY=3.8.0
ENV VER=3.8

RUN git config --global http.sslVerify false \
        && git clone https://github.com/erlotsman/djangoBlog.git \      
        && cd djangoBlog \
        && pip install -r requirements.txt \
        && python$VER manage.py migrate \
        && per=`wget -qO- ifconfig.co` \
        && sed -i "s+127.0.0.1+$per+g" /usr/local/lib/python$VER/site-packages/django/http/request.py

CMD python$VER manage.py runserver 0.0.0.0:8000
