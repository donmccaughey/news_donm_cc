FROM alpine:latest

EXPOSE 80

RUN apk add --no-cache curl nginx python3 py3-pip


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

COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY --chown=nginx:www-data wwwroot /srv/www
COPY --chown=nginx:nginx \
        nginx/error_pages /usr/lib/nginx/error_pages

# cron
COPY crontabs /var/spool/cron/crontabs


# control script
COPY sbin /usr/local/sbin


# ash profile
COPY profile.d /etc/profile.d
RUN ln -sf /etc/profile.d/color_prompt.sh.disabled /etc/profile.d/color_prompt.sh


# news app
RUN mkdir -p /usr/lib/news /var/lib/news
RUN chown -R news:news /usr/lib/news /var/lib/news
COPY --chown=news:news \
        requirements.txt version.txt /usr/lib/news/
COPY --chown=news:news \
        src /usr/lib/news

WORKDIR /usr/lib/news
RUN python3 -m pip install \
        --quiet --quiet --quiet \
        --requirement requirements.txt

HEALTHCHECK CMD curl --fail --show-error --silent http://127.0.0.1/health || exit 1

WORKDIR /root
ENTRYPOINT ["/usr/local/sbin/news"]
