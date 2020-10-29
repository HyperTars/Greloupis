FROM ubuntu:18.04
MAINTAINER hypertars hypertars@gmail.com
RUN apt-get update -y
RUN apt-get install -y python3.8 python3-pip python3.8-dev build-essential
EXPOSE 80 443 3000 5000 8000 8080 8081 8082 8083 8084
COPY . /app
WORKDIR /app
RUN make dev_env
ENTRYPOINT ["make", "run"]
# CMD [""]
