FROM python:3-alpine as base

COPY ["req.txt", "/tmp/"]
RUN apk add build-base linux-headers pcre-dev && pip install -r /tmp/req.txt && rm -f /tmp/req.txt && addgroup -g 5000 webapp && adduser -u 5000 -D -H -h /app -G webapp webapp && mkdir -p /app && chown webapp:webapp /app
USER webapp
WORKDIR /app
EXPOSE 8080

FROM base

COPY [ "app.py", "uwsgi.ini", "/app/" ]
COPY [ "html", "/app/html/" ]
ENTRYPOINT [ "uwsgi", "--ini", "uwsgi.ini" ]