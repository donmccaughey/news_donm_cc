# Notes

## To Do

- nginx content caching
- embed git sha in web page
- robots.txt, sitemap.txt
- where should `query.py` live?
- in debug mode, disable HTTP caching
- save site `etag` and `modified` in `news.json`
- nginx custom error pages for 50x 
- make page footer sticky to the window
- gunicorn error logs
- flask app logs
- health check
- json responses
- Cache wraps Store and Cache write on first `get()`
- ecr container versioning
- improve AWS permissions to read/write S3 bucket
- unify command line options and ENV
- ENV variable to control logging level
- nginx.conf `proxy_set_header` and other settings
  - https://flask.palletsprojects.com/en/2.2.x/deploying/nginx/
  - https://docs.gunicorn.org/en/latest/deploy.html
- flask proxy middleware
  - https://flask.palletsprojects.com/en/2.2.x/deploying/proxy_fix/
- link rewriting
  - reddit links to old reddit
  - cnn to https://lite.cnn.com/en
  - npr to https://text.npr.org
  - https://www.nytimes.com/timeswire
  - pay walls to https://archive.ph
    - wsj
    - economist
- filter / search news
  - by domain name
  - by keywords


## Colors

    #ffffff white
    #f5f5f5 whitesmoke
    #c0c0c0 silver
    #a9a9a9 darkgray
    #808080 gray
    #696969 dimgray
    #000000 black


## News Feeds

- Hacker News https://news.ycombinator.com/rss

- Daring Fireball https://daringfireball.net/feeds/main
      or https://daringfireball.net/feeds/json

  df sponsor links look like:
    https://daringfireball.net/feeds/sponsors/2022/12/retool_5
    https://daringfireball.net/feeds/sponsors/2022/12/kolide_5


## Docker

Alpine Linux [Docker images](https://hub.docker.com/_/alpine).

Building the Docker container:

    docker build --tag news .

Running the Docker container and getting a shell:

    docker run --name news-sh --publish 8000:80 --interactive --tty --rm news sh

2022-12-15 current Python on Alpine is 3.10.9.

Article: [Deploying NGINX and NGINX Plus with Docker][nginx-docker]

[nginx-docker]: https://www.nginx.com/blog/deploying-nginx-nginx-plus-docker/

#### Pushing Docker container to AWS ECR Public

https://docs.aws.amazon.com/AmazonECR/latest/public/public-registries.html

    # log Docker into Amazon ECR Public
    $ aws ecr-public get-login-password \
            --region us-east-1 \
        | docker login \
                --username AWS \
                --password-stdin \
                public.ecr.aws

    # https://docs.aws.amazon.com/AmazonECR/latest/public/docker-push-ecr-image.html
    $ docker tag news public.ecr.aws/d2g3p0u7/news
    $ docker push public.ecr.aws/d2g3p0u7/news

    # log Docker out of Amazon ECR Public
    $ docker logout public.ecr.aws


## AWS

### Deploying to AWS Lightsail

Lightsail command line: https://awscli.amazonaws.com/v2/documentation/api/latest/reference/lightsail/index.html

Get Lightsail deployments:

    aws lightsail get-container-service-deployments \
            --output json \
            --region us-west-2 \
            --service-name news

Public domain: https://news.6i2dp3e2do9ku.us-west-2.cs.amazonlightsail.com


## Alpine Linux

    /etc # cat passwd
    root:x:0:0:root:/root:/bin/ash
    bin:x:1:1:bin:/bin:/sbin/nologin
    daemon:x:2:2:daemon:/sbin:/sbin/nologin
    adm:x:3:4:adm:/var/adm:/sbin/nologin
    lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
    sync:x:5:0:sync:/sbin:/bin/sync
    shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
    halt:x:7:0:halt:/sbin:/sbin/halt
    mail:x:8:12:mail:/var/mail:/sbin/nologin
    news:x:9:13:news:/usr/lib/news:/sbin/nologin
    uucp:x:10:14:uucp:/var/spool/uucppublic:/sbin/nologin
    operator:x:11:0:operator:/root:/sbin/nologin
    man:x:13:15:man:/usr/man:/sbin/nologin
    postmaster:x:14:12:postmaster:/var/mail:/sbin/nologin
    cron:x:16:16:cron:/var/spool/cron:/sbin/nologin
    ftp:x:21:21::/var/lib/ftp:/sbin/nologin
    sshd:x:22:22:sshd:/dev/null:/sbin/nologin
    at:x:25:25:at:/var/spool/cron/atjobs:/sbin/nologin
    squid:x:31:31:Squid:/var/cache/squid:/sbin/nologin
    xfs:x:33:33:X Font Server:/etc/X11/fs:/sbin/nologin
    games:x:35:35:games:/usr/games:/sbin/nologin
    cyrus:x:85:12::/usr/cyrus:/sbin/nologin
    vpopmail:x:89:89::/var/vpopmail:/sbin/nologin
    ntp:x:123:123:NTP:/var/empty:/sbin/nologin
    smmsp:x:209:209:smmsp:/var/spool/mqueue:/sbin/nologin
    guest:x:405:100:guest:/dev/null:/sbin/nologin
    nobody:x:65534:65534:nobody:/:/sbin/nologin
    nginx:x:100:101:nginx:/var/lib/nginx:/sbin/nologin

    /etc # cat group
    root:x:0:root
    bin:x:1:root,bin,daemon
    daemon:x:2:root,bin,daemon
    sys:x:3:root,bin,adm
    adm:x:4:root,adm,daemon
    tty:x:5:
    disk:x:6:root,adm
    lp:x:7:lp
    mem:x:8:
    kmem:x:9:
    wheel:x:10:root
    floppy:x:11:root
    mail:x:12:mail
    news:x:13:news
    uucp:x:14:uucp
    man:x:15:man
    cron:x:16:cron
    console:x:17:
    audio:x:18:
    cdrom:x:19:
    dialout:x:20:root
    ftp:x:21:
    sshd:x:22:
    input:x:23:
    at:x:25:at
    tape:x:26:root
    video:x:27:root
    netdev:x:28:
    readproc:x:30:
    squid:x:31:squid
    xfs:x:33:xfs
    kvm:x:34:kvm
    games:x:35:
    shadow:x:42:
    cdrw:x:80:
    www-data:x:82:nginx
    usb:x:85:
    vpopmail:x:89:
    users:x:100:games
    ntp:x:123:
    nofiles:x:200:
    smmsp:x:209:smmsp
    locate:x:245:
    abuild:x:300:
    utmp:x:406:
    ping:x:999:
    nogroup:x:65533:
    nobody:x:65534:
    nginx:x:101:nginx

### crond

    ~ # crond -h
    crond: unrecognized option: h
    BusyBox v1.35.0 (2022-11-19 10:13:10 UTC) multi-call binary.
    
    Usage: crond [-fbS] [-l N] [-d N] [-L LOGFILE] [-c DIR]
    
        -f	Foreground
        -b	Background (default)
        -S	Log to syslog (default)
        -l N	Set log level. Most verbose 0, default 8
        -d N	Set log level, log to stderr
        -L FILE	Log to FILE
        -c DIR	Cron dir. Default:/var/spool/cron/crontabs

    /etc/crontabs # cat root 
    # do daily/weekly/monthly maintenance
    # min	hour	day	month	weekday	command
    */15	*	*	*	*	run-parts /etc/periodic/15min
    0	*	*	*	*	run-parts /etc/periodic/hourly
    0	2	*	*	*	run-parts /etc/periodic/daily
    0	3	*	*	6	run-parts /etc/periodic/weekly
    0	5	1	*	*	run-parts /etc/periodic/monthly

crond log levels:
https://unix.stackexchange.com/questions/412805/crond-log-level-meaning


## Nginx

### Caching

https://www.cloudsigma.com/nginx-http-proxying-load-balancing-buffering-and-caching-an-overview/
https://www.sheshbabu.com/posts/nginx-caching-proxy/


## Python

### Flask https://flask.palletsprojects.com/en/2.2.x/

### feedparser https://feedparser.readthedocs.io/en/latest/index.html

### boto3 https://boto3.amazonaws.com/v1/documentation/api/latest/index.html


## Links and Identity

### CNN

https://lite.cnn.com/en/article/h_83938cfff92036cf0e1b55ced9febc77

### NPR

https://text.npr.org/1145536902

### Mastodon

https://mastodon.online/@raph/109547934082265439
https://mastodon.social/@Tibor/109540214666343598

### GitHub

https://raw.githubusercontent.com/websnarf/bstrlib/master/bstrlib.txt

### Google Docs

https://docs.google.com/presentation/d/1sowJrQQfgxnLCErb-CvUV8VGXdtca6SWYWWLRPZgaHI/edit?usp=sharing
https://docs.google.com/presentation/d/1sowJrQQfgxnLCErb-CvUV8VGXdtca6SWYWWLRPZgaHI/mobilepresent?slide=id.ga3a076b34_0_12

### Microsoft

https://devblogs.microsoft.com/oldnewthing/20221216-00/?p=107598

### Medium

https://medium.com/@AnalyticsAtMeta/notifications-why-less-is-more-how-facebook-has-been-increasing-both-user-satisfaction-and-app-9463f7325e7d

### Threadreaderapp

https://threadreaderapp.com/thread/1606701397109796866.html


## Errors

### Missing AWS credentials

    Traceback (most recent call last):
    File "/usr/local/news/extractor.py", line 65, in <module>
    main()
    File "/usr/local/news/extractor.py", line 56, in main
    store.put(json)
    File "/usr/local/news/news/store.py", line 32, in put
    self.s3.upload_fileobj(buffer, self.bucket, self.object)
    File "/usr/lib/python3.10/site-packages/boto3/s3/inject.py", line 636, in upload_fileobj
    return future.result()
    File "/usr/lib/python3.10/site-packages/s3transfer/futures.py", line 103, in result
    return self._coordinator.result()
    File "/usr/lib/python3.10/site-packages/s3transfer/futures.py", line 266, in result
    raise self._exception
    File "/usr/lib/python3.10/site-packages/s3transfer/tasks.py", line 139, in __call__
    return self._execute_main(kwargs)
    File "/usr/lib/python3.10/site-packages/s3transfer/tasks.py", line 162, in _execute_main
    return_value = self._main(**kwargs)
    File "/usr/lib/python3.10/site-packages/s3transfer/upload.py", line 758, in _main
    client.put_object(Bucket=bucket, Key=key, Body=body, **extra_args)
    File "/usr/lib/python3.10/site-packages/botocore/client.py", line 530, in _api_call
    return self._make_api_call(operation_name, kwargs)
    File "/usr/lib/python3.10/site-packages/botocore/client.py", line 960, in _make_api_call
    raise error_class(parsed_response, operation_name)
    botocore.exceptions.ClientError: An error occurred (AccessDenied) when calling the PutObject operation: Access Denied


### Missing key in feed entry

    [26/Dec/2022:18:42:05] Traceback (most recent call last):
    [26/Dec/2022:18:42:05] File "/usr/lib/python3.10/site-packages/feedparser/util.py", line 156, in __getattr__
    [26/Dec/2022:18:42:05] return self.__getitem__(key)
    [26/Dec/2022:18:42:05] File "/usr/lib/python3.10/site-packages/feedparser/util.py", line 113, in __getitem__
    [26/Dec/2022:18:42:05] return dict.__getitem__(self, key)
    [26/Dec/2022:18:42:05] KeyError: 'title'
    [26/Dec/2022:18:42:05] During handling of the above exception, another exception occurred:
    [26/Dec/2022:18:42:05] Traceback (most recent call last):
    [26/Dec/2022:18:42:05] File "/usr/local/news/extractor.py", line 71, in <module>
    [26/Dec/2022:18:42:05] main()
    [26/Dec/2022:18:42:05] File "/usr/local/news/extractor.py", line 51, in main
    [26/Dec/2022:18:42:05] new_count += news.add_new(site.get(now))
    [26/Dec/2022:18:42:05] File "/usr/local/news/news/site.py", line 36, in get
    [26/Dec/2022:18:42:05] items = [
    [26/Dec/2022:18:42:05] File "/usr/local/news/news/site.py", line 37, in <listcomp>
    [26/Dec/2022:18:42:05] self.parse_entry(entry, now) for entry in d.entries
    [26/Dec/2022:18:42:05] File "/usr/local/news/news/site.py", line 87, in parse_entry
    [26/Dec/2022:18:42:05] title=entry.title,
    [26/Dec/2022:18:42:05] File "/usr/lib/python3.10/site-packages/feedparser/util.py", line 158, in __getattr__
    [26/Dec/2022:18:42:05] raise AttributeError("object has no attribute '%s'" % key)
    [26/Dec/2022:18:42:05] AttributeError: object has no attribute 'title'

    2022-12-26T16:06:05-08:00: WARNING:root:Entry {
            'links': [
                {
                    'rel': 'alternate',
                    'type': 'text/html',
                    'href': 'https://daringfireball.net/2022/10/the_2022_ipad'
                },
                {
                    'rel': 'shorturl',
                    'href': 'http://df4.us/ufi',
                    'type': 'text/html'
                }
            ],
            'link': 'https://daringfireball.net/2022/10/the_2022_ipad',
            'id': 'tag:daringfireball.net,2022://1.39438',
            'guidislink': False,
            'published': '2022-10-26T19:04:27Z',
            'published_parsed': time.struct_time(tm_year=2022,
                                                 tm_mon=10,
                                                 tm_mday=26,
                                                 tm_hour=19,
                                                 tm_min=4,
                                                 tm_sec=27,
                                                 tm_wday=2,
                                                 tm_yday=299,
                                                 tm_isdst=0),
            'updated': '2022-10-26T20:09:35Z',
            'updated_parsed': time.struct_time(tm_year=2022,
                                               tm_mon=10,
                                               tm_mday=26,
                                               tm_hour=20,
                                               tm_min=9,
                                               tm_sec=35,
                                               tm_wday=2,
                                               tm_yday=299,
                                               tm_isdst=0),
            'authors': [
                {
                    'name': 'John Gruber',
                    'href': 'http://daringfireball.net/'
                }
            ],
            'author_detail': {
                'name': 'John Gruber',
                'href': 'http://daringfireball.net/'
            },
            'href': 'http://daringfireball.net/',
            'author': 'John Gruber',
            'summary': 'It looks good, feels good, comes in a selection of fun colors (Apple sent me yellow), and brings the just-plain-no-adjective iPad to the modern all-screen era.',
            'summary_detail': {
                'type': 'text/plain',
                'language': None,
                'base': 'https://daringfireball.net/feeds/main',
                'value': 'It looks good, feels good, comes in a selection of fun colors (Apple sent me yellow), and brings the just-plain-no-adjective iPad to the modern all-screen era.'
            }
        } from Daring Fireball does not have a "title" attribute
    2022-12-26T16:06:05-08:00: INFO:extractor.py:Added 0 and removed 0 items



### crond errors

    2022-12-26 21:44:00 crond: wakeup dt=51
    2022-12-26 21:44:00 crond: file news:
    2022-12-26 21:44:00 crond:  line /usr/local/sbin/extract
    2022-12-26 21:44:00 crond:  job: 0 /usr/local/sbin/extract
    2022-12-26 21:44:00 crond: file root:
    2022-12-26 21:44:00 crond:  line run-parts /etc/periodic/15min
    2022-12-26 21:44:00 crond:  line run-parts /etc/periodic/hourly
    2022-12-26 21:44:00 crond:  line run-parts /etc/periodic/daily
    2022-12-26 21:44:00 crond:  line run-parts /etc/periodic/weekly
    2022-12-26 21:44:00 crond:  line run-parts /etc/periodic/monthly
    2022-12-26 21:44:00 crond: USER news pid  51 cmd /usr/local/sbin/extract
    2022-12-26 21:44:00 crond: can't change directory to '/usr/lib/news'
    2022-12-26 21:44:00 crond: child running /bin/ash

    2022-12-26 22:17:00 crond: wakeup dt=20
    2022-12-26 22:17:00 crond: file news:
    2022-12-26 22:17:00 crond:  line /usr/local/sbin/extract
    2022-12-26 22:17:00 crond:  job: 0 /usr/local/sbin/extract
    2022-12-26 22:17:00 crond: file root:
    2022-12-26 22:17:00 crond:  line run-parts /etc/periodic/15min
    2022-12-26 22:17:00 crond:  line run-parts /etc/periodic/hourly
    2022-12-26 22:17:00 crond:  line run-parts /etc/periodic/daily
    2022-12-26 22:17:00 crond:  line run-parts /etc/periodic/weekly
    2022-12-26 22:17:00 crond:  line run-parts /etc/periodic/monthly
    2022-12-26 22:17:00 crond: USER news pid 235 cmd /usr/local/sbin/extract
    2022-12-26 22:17:00 crond: can't change directory to '/usr/lib/news'
    2022-12-26 22:17:00 crond: child running /bin/ash
    2022-12-26 22:17:01 INFO:botocore.credentials:Found credentials in environment variables.
    2022-12-26 22:17:02 INFO:extractor.py:Using ReadOnlyStore(S3Store('news.donm.cc', 'news.json'))
    2022-12-26 22:17:03 INFO:extractor.py:Added 2 and removed 0 items
    2022-12-26 22:17:03 Traceback (most recent call last):
    2022-12-26 22:17:03   File "/usr/local/news/extractor.py", line 88, in <module>
    2022-12-26 22:17:03     main()
    2022-12-26 22:17:03   File "/usr/local/news/extractor.py", line 77, in main
    2022-12-26 22:17:03     cache.put(json)
    2022-12-26 22:17:03   File "/usr/local/news/news/cache.py", line 27, in put
    2022-12-26 22:17:03     with self.path.open('w', encoding='utf-8') as f:
    2022-12-26 22:17:03   File "/usr/lib/python3.10/pathlib.py", line 1119, in open
    2022-12-26 22:17:03     return self._accessor.open(self, mode, buffering, encoding, errors,
    2022-12-26 22:17:03 PermissionError: [Errno 13] Permission denied: '/var/lib/news/news.json'
    2022-12-26 22:17:10 crond: wakeup dt=10

