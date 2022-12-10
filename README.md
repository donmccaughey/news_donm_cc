# News

A service that finds things I'm interested in.

## Notes

### Docker

Alpine Linux [Docker images](https://hub.docker.com/_/alpine).

Building the Docker container:

    docker build --tag news .

Running the Docker container and getting a shell:

    docker run --name news-sh --publish 8000:80 --interactive --tty --rm news sh

2022-12-08 current Python on Alpine is 3.10.8.

Article: [Deploying NGINX and NGINX Plus with Docker][nginx-docker]

[nginx-docker]: https://www.nginx.com/blog/deploying-nginx-nginx-plus-docker/


## To Do

- rotate nginx error logs or send them somewhere
    https://www.cyberciti.biz/faq/how-to-install-and-configure-log-roate-in-alpine-linux/



