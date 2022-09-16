#FROM docker.io/galenguyer/nginx:1.23.1-alpine3.16.2-spa
FROM docker.io/python:3.8.14-buster
MAINTAINER Klaus Curde <kcurde@gmail.com>

WORKDIR /app
COPY . /app

RUN ["pip", "install", "-r", "requirements.txt"]

EXPOSE 8080

ENTRYPOINT ["python"]
CMD ["app.py"]
