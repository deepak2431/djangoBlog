FROM ubuntu:latest
MAINTAINER Yevgheniq Lotsman
ENV TZ=Europe/Kiev
ENV VERPY=3.8.0
ENV VER=3.8

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
        && apt -qqy update \
        && apt -qqy install --no-install-recommends wget build-essential checkinstall libreadline-gplv2-dev libncursesw5-dev libssl-dev \
                                                libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev tar libpq-dev git \
        && cd /opt && wget --no-check-certificate https://www.python.org/ftp/python/$VERPY/Python-$VERPY.tgz \
        && tar xzf Python-$VERPY.tgz \
        && cd Python-$VERPY && ./configure --enable-optimizations && make altinstall \
        && wget --no-check-certificate https://bootstrap.pypa.io/get-pip.py \
        && python$VER get-pip.py \
        && rm -rf /opt/Python-$VERPY.tgz get-pip.py /var/lib/apt/lists/* \
        && git clone https://github.com/erlotsman/djangoBlog.git \
        && cd djangoBlog \
        && pip install -r requirements.txt \
        && python$VER manage.py migrate \
        && per=`wget -qO- ifconfig.co` \
        && sed -i "s+127.0.0.1+$per+g" /usr/local/lib/python$VER/site-packages/django/http/request.py

CMD python$VER /djangoBlog/manage.py runserver 0.0.0.0:8000
