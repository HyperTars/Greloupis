FROM ubuntu:latest
MAINTAINER hypertars hypertars@gmail.com
RUN apt-get update -y
RUN apt-get install -y python3 python3-pip python3-dev build-essential
COPY ./source
WORKDIR /source
RUN make dev_env
ENTRYPOINT ["python3"]
CMD ["app.py"]
