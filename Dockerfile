FROM docker.io/python:2.7

RUN apt-get update

RUN apt-get --no-install-recommends install --yes \
    libaio1 libaio-dev xmlsec1 libffi-dev \
    libldap2-dev libsasl2-dev \
    build-essential libmysqlclient-dev git

WORKDIR /tmp/

RUN pip install gunicorn

COPY requirements.txt /tmp/
RUN pip install -r requirements.txt

RUN mkdir -p /usr/src/app


WORKDIR /usr/src/app

EXPOSE 8000
CMD ./start.sh

COPY . /usr/src/app
RUN python manage.py collectstatic --settings=student_explorer.settings --noinput
