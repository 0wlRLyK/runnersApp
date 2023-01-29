FROM python:3.10.9-alpine

# set work directory
WORKDIR /project/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY ../Pipfile Pipfile.lock /project/

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev libffi-dev openssl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk del build-deps
# install pipenv on the container
RUN pip install --upgrade pip
# pillow preparation
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache g++ freetype-dev \
    && apk add jpeg-dev zlib-dev libjpeg \
    && pip install Pillow \
    && apk del build-deps
RUN apk update && apk add python3-dev libxml2-dev libxslt-dev  \
                        gcc \
                        libc-dev \
                        libffi-dev
RUN pip install -U pipenv

# install project dependencies
RUN pipenv install --system



# copy project
COPY ../.. /project/
