FROM python:3.6

RUN apt-get update && apt-get --no-install-recommends install --yes \
    libaio1 libaio-dev xmlsec1 libffi-dev \
    libldap2-dev libsasl2-dev \
    build-essential default-libmysqlclient-dev git cron netcat

WORKDIR /tmp/

COPY requirements.txt /tmp/

RUN pip install -r requirements.txt && \
    pip install gunicorn

# Sets the local timezone of the docker image
ENV TZ=America/Detroit
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Use this tag of API Utils, this will eventually be released
ENV API_UTILS_VERSION v1.1
RUN git clone https://github.com/tl-its-umich-edu/api-utils-python && cd api-utils-python && git checkout tags/${API_UTILS_VERSION} && pip install .

ARG LOCALHOST_DEV

WORKDIR /usr/src/app/student_explorer/dependencies/

# This is based on here. It seems like it unfortunately may need to be manually updated
# http://yum.oracle.com/repo/OracleLinux/OL7/oracle/instantclient/x86_64/index.html

ENV ORACLE_CLIENT_VERSION=18.3
ENV ORACLE_HOME /usr/lib/oracle/$ORACLE_CLIENT_VERSION/client64
ENV LD_LIBRARY_PATH /usr/lib/oracle/$ORACLE_CLIENT_VERSION/client64/lib


RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app/
COPY . /usr/src/app

# Run these only for dev
# Make a python package:
RUN if [ "$LOCALHOST_DEV" ] ; then \
    echo "LOCALHOST_DEV is set, building development dependencies" && \
    touch /usr/src/app/student_explorer/local/__init__.py && \
# Create default settings_override module:
    echo "from student_explorer.settings import *\n\nDEBUG = True" > /usr/src/app/student_explorer/local/settings_override.py && \
    apt-get --no-install-recommends install --yes default-mysql-client && \
    pip install coverage\
    ; else \
    echo "LOCALHOST_DEV is not set, building production (Oracle) dependencies" && \
    # Based on this Dockerfile for 18.3 https://github.com/oracle/docker-images/blob/master/OracleInstantClient/dockerfiles/18.3.0/Dockerfile
    # Converted to Debian format
    mkdir -p /etc/yum/repos.d && curl -o /etc/yum/repos.d/public-yum-ol7.repo https://yum.oracle.com/public-yum-ol7.repo && \
    apt-get install --yes yum-utils alien && \
    yum-config-manager --enable ol7_oracle_instantclient && \
    yumdownloader oracle-instantclient${ORACLE_CLIENT_VERSION}-devel oracle-instantclient${ORACLE_CLIENT_VERSION}-basiclite && \
    alien oracle-instantclient*.rpm && \
    dpkg -i *.deb && rm *.deb *.rpm && \
    pip install cx_Oracle==7.0 \
    ; fi

# Compile the css file
RUN pysassc seumich/static/seumich/styles/main.scss seumich/static/seumich/styles/main.css

RUN python manage.py collectstatic --settings=student_explorer.settings --noinput --verbosity 0

EXPOSE 8000
CMD ./start.sh
