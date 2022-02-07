FROM python:3.10.1-bullseye

# ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
# RUN apk add --update --no-cache postgresql-client
# RUN apk add --update --no-cache --virtual .tmp-build-deps \
#       gcc libc-dev linux-headers postgresql-dev
RUN python -m pip install --upgrade pip
RUN python -m pip install -r /requirements.txt
# RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./project /app

# RUN adduser -D user
# USER user
