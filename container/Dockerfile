FROM alpine:latest

EXPOSE 80

RUN apk add --no-cache \
        curl \
        nginx \
        python3 \
        py3-beautifulsoup4 \
        py3-boto3 \
        py3-feedparser \
        py3-flask \
        py3-gunicorn \
        py3-requests


# nginx
RUN rm -rf \
        /etc/nginx/http.d/ \
        /etc/nginx/modules/ \
        /var/lib/nginx/html/
RUN rm -f \
        /etc/nginx/fastcgi.conf \
        /etc/nginx/fastcgi_params \
        /etc/nginx/scgi_params \
        /etc/nginx/uwsgi_params

RUN ln -sf /dev/stderr /var/log/nginx/error.log
RUN ln -sf /srv/www /var/lib/nginx/html

RUN mkdir -p /var/cache/nginx
RUN chown -R nginx:nginx /var/cache/nginx

COPY container/nginx/nginx.conf /etc/nginx/nginx.conf
COPY --chown=nginx:www-data container/wwwroot /srv/www
COPY --chown=nginx:nginx \
        container/nginx/error_pages /usr/lib/nginx/error_pages


# cron jobs
COPY container/crontabs /var/spool/cron/crontabs


# control scripts
COPY container/sbin /usr/local/sbin


# ash profile
COPY container/profile.d /etc/profile.d
RUN ln -sf /etc/profile.d/color_prompt.sh.disabled \
        /etc/profile.d/color_prompt.sh


# news app
RUN mkdir -p /usr/lib/news /var/lib/news
RUN chown -R news:news /usr/lib/news /var/lib/news
COPY --chown=news:news ${version_file} /usr/lib/news/
COPY --chown=news:news src /usr/lib/news


HEALTHCHECK CMD \
        curl --fail --show-error --silent \
                http://127.0.0.1/health \
        || exit 1

WORKDIR /root
ENTRYPOINT ["/usr/local/sbin/news"]
