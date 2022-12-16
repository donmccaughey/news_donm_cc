FROM alpine:latest

EXPOSE 80

RUN apk add --no-cache nginx python3 py3-pip

WORKDIR /etc/nginx
RUN rm -f fastcgi.conf fastcgi_params scgi_params uwsgi_params
RUN rm -rf http.d/ modules/
RUN ln -sf /dev/stderr /var/log/nginx/error.log

COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/default /srv/nginx/default
COPY sbin /usr/local/sbin
COPY src /opt/news
COPY requirements.txt /opt/news

WORKDIR /opt/news
RUN pip install -r requirements.txt

WORKDIR /opt/news
ENTRYPOINT ["/usr/local/sbin/news"]
