FROM python:3.8.6-alpine
RUN mkdir -p /usr/src/app
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN apk add python3-dev build-base linux-headers
RUN pip3 install -r requirements.txt
CMD ["uwsgi", "uwsgi.ini"]
