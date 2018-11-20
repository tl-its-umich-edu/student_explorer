FROM docker.io/python:2.7

RUN apt-get update

RUN apt-get --no-install-recommends install --yes \
    libaio1 libaio-dev xmlsec1 libffi-dev \
    libldap2-dev libsasl2-dev \
    build-essential default-libmysqlclient-dev git

WORKDIR /tmp/

COPY requirements.txt /tmp/

RUN pip install -r requirements.txt && \
    pip install gunicorn

# Sets the local timezone of the docker image
ENV TZ=America/Detroit
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY . /usr/src/app

# Install npm and wait-port globally
# https://github.com/nodesource/distributions/blob/master/README.md
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash - && \
    apt-get -y install npm && npm install -g wait-port@"~0.2.2"

ARG LOCALHOST_DEV

WORKDIR /usr/src/app/student_explorer/dependencies/

ENV ORACLE_HOME /usr/lib/oracle/18.3/client64	
ENV LD_LIBRARY_PATH /usr/lib/oracle/18.3/client64/lib	

# Run these only for dev
# Make a python package:
RUN if [ "$LOCALHOST_DEV" ] ; then \
    echo "LOCALHOST_DEV is set, building development dependencies" && \ 
    touch /usr/src/app/student_explorer/local/__init__.py && \
# Create default settings_override module:
    echo "from student_explorer.settings import *\n\nDEBUG = True" > /usr/src/app/student_explorer/local/settings_override.py && \ 
    apt-get --no-install-recommends install --yes mysql-client && \
    pip install coverage\
    ; else \
    echo "LOCALHOST_DEV is not set, building production (Oracle) dependencies" && \
    # Based on this Dockerfile for 18.3 https://github.com/oracle/docker-images/blob/master/OracleInstantClient/dockerfiles/18.3.0/Dockerfile
    # Converted to Debian format
    mkdir -p /etc/yum/repos.d && curl -o /etc/yum/repos.d/public-yum-ol7.repo https://yum.oracle.com/public-yum-ol7.repo && \
    apt-get install --yes yum-utils alien && \
    yum-config-manager --enable ol7_oracle_instantclient && \
    yumdownloader oracle-instantclient18.3-devel oracle-instantclient18.3-basiclite && \
    alien oracle-instantclient18.3-basiclite-18.3.0.0.0-2.x86_64.rpm oracle-instantclient18.3-devel-18.3.0.0.0-2.x86_64.rpm && \
    dpkg -i *.deb && rm *.deb *.rpm && \
    pip install cx_Oracle==7.0 \
    ; fi

WORKDIR /usr/src/app/

# Comiple the css file
RUN pysassc seumich/static/seumich/styles/main.scss seumich/static/seumich/styles/main.css

RUN python manage.py collectstatic --settings=student_explorer.settings --noinput --verbosity 0

EXPOSE 8000
CMD ./start.sh
