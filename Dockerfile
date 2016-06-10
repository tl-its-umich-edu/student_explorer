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

RUN echo ~
RUN mkdir ~/.ssh
RUN echo 'bitbucket.org,104.192.143.1,104.192.143.2,104.192.143.3,104.192.143.6\
5.104.192.143.66,104.192.143.67 ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAubiN81eDcaf\
rgMeLzaFPsw2kNvEcqTKl/VqLat/MaB33pZy0y3rJZtnqwR2qOOvbwKZYKiEO1O6VqNEBxKvJJelCq0\
dTXWT5pbO2gDXC6h6QDXCaHo6pOHGPUy+YBaGQRGuSusMEASYiWunYN0vCAI8QaXnWMXNMdFP3jHAJH\
0eDsoiGnLPBlBp4TNm6rYI74nMzgz3B9IikW4WVK+dc8KZJZWYjAuORU3jc1c/NPskD2ASinf8v3xnf\
XeukU0sJ5N6m5E8VLjObPEO+mN2t/FZTMZLiFqPWc/ALSqnMnnhwrNi2rbfg/rd/IpL8Le3pSBne8+s\
eeFVBoGqzHM9yXw==' >> ~/.ssh/known_hosts
RUN pip install cx_Oracle gunicorn git+ssh://git@bitbucket.org/umichdig/django-tracking.git

COPY requirements.txt /tmp/
RUN pip install -r requirements.txt

RUN mkdir -p /usr/src/app


WORKDIR /usr/src/app

EXPOSE 8000
CMD ./start.sh

COPY . /usr/src/app
RUN python manage.py collectstatic --settings=student_explorer.settings --noinput
