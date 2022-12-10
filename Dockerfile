FROM alpine:latest

EXPOSE 80

RUN apk update
RUN apk add nginx python3

RUN cd /etc/nginx && rm fastcgi.conf fastcgi_params scgi_params uwsgi_params
RUN rm -rf /etc/nginx/http.d /etc/nginx/modules

COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/default /srv/nginx/default
COPY sbin /usr/local/sbin
COPY src /opt/news

ENTRYPOINT ["/usr/local/sbin/news"]
