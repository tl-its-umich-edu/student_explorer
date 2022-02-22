FROM python:3.8-slim

RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -

RUN apt-get update && apt-get --no-install-recommends install --yes \
    libaio1 libaio-dev xmlsec1 libffi-dev libsasl2-dev \
    build-essential default-libmysqlclient-dev git cron netcat \
    nodejs npm

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
ENV ORACLE_CLIENT_VERSION=18.5
ENV ORACLE_CLIENT_VERSION_FULL=18.5.0.0.0-3
ENV ORACLE_HOME /usr/lib/oracle/$ORACLE_CLIENT_VERSION/client64
ENV LD_LIBRARY_PATH /usr/lib/oracle/$ORACLE_CLIENT_VERSION/client64/lib

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app/
COPY . /usr/src/app

WORKDIR /tmp/
# Run these only for dev
# Make a python package:
RUN if [ "$LOCALHOST_DEV" ] ; then \
    echo "LOCALHOST_DEV is set, building development dependencies" && \
    touch /usr/src/app/student_explorer/local/__init__.py && \
# Create default settings_override module:
    echo "from student_explorer.settings import *\n\nDEBUG = True" > /usr/src/app/student_explorer/local/settings_override.py && \
    apt-get --no-install-recommends install --yes default-mysql-client && \
    pip install coverage \
    ; else \
    echo "LOCALHOST_DEV is not set, building production (Oracle) dependencies" && \
    # Converted to Debian format
    apt-get install --yes alien && \
    wget https://yum.oracle.com/repo/OracleLinux/OL7/oracle/instantclient/x86_64/getPackage/oracle-instantclient${ORACLE_CLIENT_VERSION}-basiclite-${ORACLE_CLIENT_VERSION_FULL}.x86_64.rpm https://yum.oracle.com/repo/OracleLinux/OL7/oracle/instantclient/x86_64/getPackage/oracle-instantclient${ORACLE_CLIENT_VERSION}-devel-${ORACLE_CLIENT_VERSION_FULL}.x86_64.rpm && \
    alien oracle-instantclient*.rpm && \
    dpkg -i *.deb && rm *.deb *.rpm && \
    pip install cx_Oracle==7.0 \
    ; fi

WORKDIR /usr/src/app/
# Compile the css file
RUN pysassc seumich/static/seumich/styles/main.scss seumich/static/seumich/styles/main.css

RUN npm install

# This is needed to clean up the examples files as these cause collectstatic to fail (and take up extra space)
RUN find node_modules -type d -name "examples" -print0 | xargs -0 rm -rf

RUN python manage.py collectstatic --settings=student_explorer.settings --noinput --verbosity 0

EXPOSE 8000
CMD ./start.sh
