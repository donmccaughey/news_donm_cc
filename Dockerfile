FROM alpine:latest

EXPOSE 80

RUN apk add --no-cache nginx python3 py3-pip

WORKDIR /etc/nginx
RUN rm -f fastcgi.conf fastcgi_params scgi_params uwsgi_params
RUN rm -rf http.d/ modules/
RUN ln -sf /dev/stderr /var/log/nginx/error.log

COPY requirements.txt /usr/local/news/requirements.txt
COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/default /var/nginx/default
COPY sbin /usr/local/sbin
COPY src /usr/local/news

RUN mkdir -p /var/news

WORKDIR /usr/local/news
RUN python3 -m pip install --quiet --quiet --quiet --requirement requirements.txt

WORKDIR /root
ENTRYPOINT ["/usr/local/sbin/news"]
