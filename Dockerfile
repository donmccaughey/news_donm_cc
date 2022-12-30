FROM alpine:latest

EXPOSE 80

RUN apk add --no-cache nginx python3 py3-pip


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
COPY --chown=nginx:www-data nginx/default /srv/www


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
        requirements.txt version.txt /usr/local/news/
COPY --chown=news:news \
        src /usr/local/news

WORKDIR /usr/local/news
RUN python3 -m pip install \
        --quiet --quiet --quiet \
        --requirement requirements.txt


WORKDIR /root
ENTRYPOINT ["/usr/local/sbin/news"]
