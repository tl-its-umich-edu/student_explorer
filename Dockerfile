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

#https://github.com/jwilder/dockerize
ENV DOCKERIZE_VERSION v0.6.1
RUN curl -sLO "https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz" \
    && tar -C /usr/local/bin -xzvf "dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz" \
    && rm "dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz"

# Sets the local timezone of the docker image
ENV TZ=America/Detroit
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY . /usr/src/app

ARG LOCALHOST_DEV
# Run these only for dev
# Make a python package:
RUN if [ "$LOCALHOST_DEV" ] ; then \
    echo "LOCALHOST_DEV is set, building development dependencies" && \ 
    touch /usr/src/app/student_explorer/local/__init__.py && \
# Create default settings_override module:
    echo "from student_explorer.settings import *\n\nDEBUG = True" > /usr/src/app/student_explorer/local/settings_override.py && \ 
    apt-get --no-install-recommends install --yes mysql-client && \
    pip install coverage \
    ; else echo "Skipping Development Dependencies" ; fi

RUN python manage.py collectstatic --settings=student_explorer.settings --noinput --verbosity 0

EXPOSE 8000
CMD ./start.sh
