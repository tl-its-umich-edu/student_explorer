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

RUN mkdir ~/.ssh
RUN echo 'bitbucket.org,131.103.20.167,131.103.20.168 ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAubiN81eDcafrgMeLzaFPsw2kNvEcqTKl/VqLat/MaB33pZy0y3rJZtnqwR2qOOvbwKZYKiEO1O6VqNEBxKvJJelCq0dTXWT5pbO2gDXC6h6QDXCaHo6pOHGPUy+YBaGQRGuSusMEASYiWunYN0vCAI8QaXnWMXNMdFP3jHAJH0eDsoiGnLPBlBp4TNm6rYI74nMzgz3B9IikW4WVK+dc8KZJZWYjAuORU3jc1c/NPskD2ASinf8v3xnfXeukU0sJ5N6m5E8VLjObPEO+mN2t/FZTMZLiFqPWc/ALSqnMnnhwrNi2rbfg/rd/IpL8Le3pSBne8+seeFVBoGqzHM9yXw==\
' >> ~/.ssh/known_hosts
RUN pip install cx_Oracle gunicorn git+ssh://git@bitbucket.org/umichdig/django-tracking.git

COPY requirements.txt /tmp/
RUN pip install -r requirements.txt

RUN mkdir -p /usr/src/app


WORKDIR /usr/src/app

EXPOSE 8000
CMD ./start.sh

COPY . /usr/src/app
RUN python manage.py collectstatic --settings=student_explorer.settings --noinput
