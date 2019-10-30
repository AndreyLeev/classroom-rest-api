FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
       
ADD requirements.txt /code/
RUN pip install -r requirements.txt

RUN apk add --update bash
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ADD . /code/


