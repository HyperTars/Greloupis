FROM ubuntu:18.04
MAINTAINER hypertars hypertars@gmail.com
RUN apt-get update -y
RUN apt-get install -y python3.8 python3-pip python3.8-dev build-essential
EXPOSE 5000
COPY . /app
WORKDIR /app
RUN make dev_env
ENTRYPOINT ["python3", "-m", "source.app"]
CMD ["FLASK_APP=app", "flask", "run", "--host=0.0.0.0", "--port=5000"]
