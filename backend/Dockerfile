FROM python:3.8.6
RUN mkdir -p /usr/src/app
EXPOSE 80 443 3000 5000 8000 8080 8081 8082 8083 8084
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN make dev_env
ENTRYPOINT ["make", "run"]
# CMD [""]
