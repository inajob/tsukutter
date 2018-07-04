FROM nginx:alpine

RUN apk add --update --no-cache supervisor python3 sqlite && \
    mkdir /etc/supervisor.d

COPY python3-fcgi.supervisor.conf /etc/supervisor.d/python3-fcgi.ini
COPY python3-fcgi.nginx.conf /etc/nginx/conf.d/python3-fcgi.conf

RUN rm /etc/nginx/conf.d/default.conf

COPY run-server /usr/local/bin
COPY app /app

RUN chmod 755 /usr/local/bin/run-server && \
    chmod 755 /app/bat/chk.sh && \
    chmod 755 /app/cgi-bin/tsukutter.fcgi

EXPOSE 80 443

CMD ["run-server"]

