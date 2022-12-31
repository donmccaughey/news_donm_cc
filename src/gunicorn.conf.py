bind = 'unix:/var/run/nginx/news'
loglevel = 'error'
group = 'news'
max_requests = 10000
max_requests_jitter = 1000
user = 'news'
workers = 4
wsgi_app = 'server:app'
