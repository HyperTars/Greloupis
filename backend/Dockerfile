FROM python:3.8.6
RUN mkdir -p /usr/src/app
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN make dev_env
CMD ["make", "run"]
# CMD [""]
