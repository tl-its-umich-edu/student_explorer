FROM oracle_instantclient

RUN apt-get update

RUN apt-get --no-install-recommends install --yes libldap2-dev libsasl2-dev
RUN apt-get --no-install-recommends install --yes python-pip python-dev
RUN apt-get --no-install-recommends install --yes build-essential libmysqlclient-dev git
RUN apt-get --no-install-recommends install --yes nodejs npm \
    && ln -s /usr/bin/nodejs /usr/bin/node
RUN npm install -g bower

WORKDIR /tmp/

RUN pip install cx_Oracle gunicorn

COPY requirements.txt /tmp/
RUN pip install -r requirements.txt

RUN mkdir -p /usr/src/app

COPY . /usr/src/app

WORKDIR /usr/src/app/sespa
RUN bower --allow-root install
WORKDIR /usr/src/app

WORKDIR /usr/src/app
EXPOSE 8000
CMD ./start.sh
