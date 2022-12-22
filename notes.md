# Notes

## To Do

- updating <time> tags with relative times
- nginx content caching
- in debug mode, disable HTTP caching
- add source name, initials to source and item
- gunicorn error logs
- flask app logs
- health check
- ecr container versioning
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


## Python

### Flask https://flask.palletsprojects.com/en/2.2.x/

### feedparser https://feedparser.readthedocs.io/en/latest/index.html

### boto3 https://boto3.amazonaws.com/v1/documentation/api/latest/index.html


## Errors

### Container startup error on Lightsail

    [deployment:16] Finalizing your deployment
    [deployment:17] Creating your deployment
    [2022-12-19 05:34:06 +0000] [8] [INFO] Starting gunicorn 20.1.0
    [2022-12-19 05:34:06 +0000] [8] [INFO] Listening at: http://127.0.0.1:8000 (8)
    [2022-12-19 05:34:06 +0000] [8] [INFO] Using worker: sync
    [2022-12-19 05:34:06 +0000] [11] [INFO] Booting worker with pid: 11
    [2022-12-19 05:34:07 +0000] [12] [INFO] Booting worker with pid: 12
    [2022-12-19 05:34:07 +0000] [13] [INFO] Booting worker with pid: 13
    [2022-12-19 05:34:07 +0000] [14] [INFO] Booting worker with pid: 14
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
    [deployment:17] Reached a steady state
    [deployment:17] Finalizing your deployment
    [deployment:18] Creating your deployment
    [2022-12-19 05:41:39 +0000] [9] [INFO] Starting gunicorn 20.1.0
    [2022-12-19 05:41:39 +0000] [9] [INFO] Listening at: http://127.0.0.1:8000 (9)
    [2022-12-19 05:41:39 +0000] [9] [INFO] Using worker: sync
    [2022-12-19 05:41:39 +0000] [12] [INFO] Booting worker with pid: 12
    [2022-12-19 05:41:39 +0000] [13] [INFO] Booting worker with pid: 13
    [2022-12-19 05:41:39 +0000] [14] [INFO] Booting worker with pid: 14
    [2022-12-19 05:41:39 +0000] [15] [INFO] Booting worker with pid: 15
    [deployment:18] Reached a steady state
