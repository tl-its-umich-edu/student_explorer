FROM docker.io/python:2.7

RUN apt-get update

RUN apt-get --no-install-recommends install --yes \
    libaio1 libaio-dev xmlsec1 \
    libldap2-dev libsasl2-dev \
    build-essential libmysqlclient-dev git

WORKDIR /tmp/

COPY student_explorer/dependencies/oracle-instantclient12.1-*.deb /tmp/
RUN dpkg -i oracle-instantclient12.1-*.deb
ENV ORACLE_HOME /usr/lib/oracle/12.1/client64
ENV LD_LIBRARY_PATH /usr/lib/oracle/12.1/client64/lib
RUN rm oracle-instantclient12.1-*.deb

RUN pip install cx_Oracle gunicorn

COPY requirements.txt /tmp/
RUN pip install -r requirements.txt

RUN mkdir -p /usr/src/app


WORKDIR /usr/src/app

EXPOSE 8000
CMD ./start.sh

COPY . /usr/src/app
RUN python manage.py collectstatic --settings=student_explorer.settings.base --noinput
