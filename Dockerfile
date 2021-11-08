FROM python:3.8.3-alpine
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

# dependencies for psycopg2-binary
RUN apk add --no-cache mariadb-connector-c-dev


RUN apk update && apk add libpq

RUN apk update \
    && apk add --virtual build-deps gcc python3 python3-dev musl-dev build-base \
    && apk add --no-cache jpeg-dev zlib-dev mariadb-dev 

RUN pip3 install mysqlclient
RUN pip3 install djangorestframework

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

RUN apk del build-deps

# Now copy in our code, and run it
COPY . /app/
