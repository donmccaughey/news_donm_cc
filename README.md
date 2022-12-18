# News

A service that finds things I'm interested in.

## Notes

### Docker

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

#### Deploying to AWS Lightsail

Lightsail command line: https://awscli.amazonaws.com/v2/documentation/api/latest/reference/lightsail/index.html

Get Lightsail deployments:

    aws lightsail get-container-service-deployments \
            --output json \
            --region us-west-2 \
            --service-name news

Public domain: https://news.6i2dp3e2do9ku.us-west-2.cs.amazonlightsail.com


### Flask https://flask.palletsprojects.com/en/2.2.x/

### feedparser https://feedparser.readthedocs.io/en/latest/index.html

### boto3 https://boto3.amazonaws.com/v1/documentation/api/latest/index.html


## To Do

- gunicorn error logs
- flask app logs
- health check
- ecr container versioning
- nginx.conf `proxy_set_header` and other settings
  - https://flask.palletsprojects.com/en/2.2.x/deploying/nginx/
  - https://docs.gunicorn.org/en/latest/deploy.html
- flask proxy middleware
  - https://flask.palletsprojects.com/en/2.2.x/deploying/proxy_fix/
