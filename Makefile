AWS_ACCESS_KEY_ID ?= $(shell aws configure get aws_access_key_id)
AWS_SECRET_ACCESS_KEY ?= $(shell aws configure get aws_secret_access_key)
TMP ?= $(abspath tmp)

NEWS := news  # container name


.SECONDEXPANSION :


.PHONY : all
all : build


.PHONY : build
build : $(TMP)/docker-build.stamp.txt


.PHONY : check
check : $(TMP)/pytest.stamp.txt


.PHONY : clean
clean : stop
	-docker rm $(NEWS)
	rm -rf $(TMP)


.PHONY : debug
debug :
	python3 src/extractor.py \
		--cache-dir="$(TMP)" \
		--no-store
	FLASK_CACHE_DIR="$(TMP)" \
		flask \
		--app src/server \
		--debug \
		run


.PHONY : deploy
deploy : $(TMP)/aws-lightsail-create-container-service-deployment.stamp.txt


.PHONY : logs
logs :
	python3 scripts/logs.py

.PHONY : push
push : $(TMP)/docker-push.stamp.txt


.PHONY : run
run : $(TMP)/docker-run.stamp.txt


.PHONY : shell
shell: $(TMP)/docker-run.stamp.txt
	docker exec \
		--interactive \
		--tty \
		$(NEWS) sh -l


.PHONY : status
status :
	docker inspect news | jq '.[0].State'


.PHONY : stop
stop :
	-docker stop $(NEWS)
	rm -rf $(TMP)/docker-run.stamp.txt


container_files := \
	.dockerignore \
	requirements.txt \
	crontabs/news \
	nginx/nginx.conf \
	nginx/error_pages/404.html \
	nginx/error_pages/500.html \
	nginx/error_pages/502.html \
	nginx/error_pages/503.html \
	nginx/error_pages/504.html \
	profile.d/dir.sh \
	sbin/check-health \
	sbin/extract \
	sbin/news \
	sbin/serve \
	wwwroot/robots.txt \
	wwwroot/sitemap.txt

script_files := \
	scripts/logs.py

source_files := \
	src/extractor.py \
	src/gunicorn.conf.py \
	src/health_check.py \
	src/query.py \
	src/server.py \
	src/feeds/__init__.py \
	src/feeds/acoup.py \
	src/feeds/daring_fireball.py \
	src/feeds/hacker_news.py \
	src/feeds/site.py \
	src/feeds/sites.py \
	src/feeds/streetsblog.py \
	src/health/__init__.py \
	src/health/jobs.py \
	src/health/processes.py \
	src/health/servers.py \
	src/news/__init__.py \
	src/news/item.py \
	src/news/news.py \
	src/news/source.py \
	src/news/store.py \
	src/news/url.py \
	src/templates/news.html \
	src/utility/cache.py \
	src/utility/page.py \
	src/webapp/__init__.py \
	src/webapp/error_handlers.py \
	src/webapp/news_page.py \
	src/webapp/template_filters.py \
	src/webapp/utility.py \
	src/webapp/views.py

test_files := \
	src/feeds/daring_fireball_test.py \
	src/feeds/site_test.py \
	src/feeds/streetsblog_test.py \
	src/news/item_test.py \
	src/news/news_test.py \
	src/news/source_test.py \
	src/news/store_test.py \
	src/news/url_test.py \
	src/utility/cache_test.py \
	src/utility/page_test.py


$(TMP)/.env : | $$(dir $$@)
	printf "AWS_ACCESS_KEY_ID=%s\n" "$(AWS_ACCESS_KEY_ID)" >> $@
	printf "AWS_SECRET_ACCESS_KEY=%s\n" "$(AWS_SECRET_ACCESS_KEY)" >> $@
	printf "AWS_DEFAULT_REGION=us-west-2\n" >> $@
	chmod 600 $@


$(TMP)/aws-lightsail-create-container-service-deployment.stamp.txt : \
		$(TMP)/create-container-service-deployment.json \
		$(TMP)/docker-push.stamp.txt \
		| $$(dir $$@)
	aws lightsail create-container-service-deployment \
		--cli-input-json "$$(jq -c . $(TMP)/create-container-service-deployment.json)" \
		--output json \
		--region us-west-2 \
		--service-name news \
		> $(TMP)/lightsail-deployment.json
	date > $@


$(TMP)/create-container-service-deployment.json : aws/create-container-service-deployment.template.json | $$(dir $$@)
	sed \
		-e "s/{{AWS_ACCESS_KEY_ID}}/$(AWS_ACCESS_KEY_ID)/g" \
		-e "s/{{AWS_SECRET_ACCESS_KEY}}/$(AWS_SECRET_ACCESS_KEY)/g" \
		$< > $@
	chmod 600 $@


$(TMP)/docker-build.stamp.txt : \
		Dockerfile \
		$(container_files) \
		$(source_files) \
		| $$(dir $$@)
	git rev-parse --short HEAD > version.txt
	docker build \
		--file $< \
		--platform linux/amd64 \
		--tag $(NEWS) \
		--quiet \
		$(dir $<)
	date > $@


$(TMP)/docker-push.stamp.txt : $(TMP)/docker-build.stamp.txt | $$(dir $$@)
	aws ecr-public get-login-password --region us-east-1 \
        | docker login --username AWS --password-stdin public.ecr.aws
	docker tag news public.ecr.aws/d2g3p0u7/news
	docker push --quiet public.ecr.aws/d2g3p0u7/news
	docker logout public.ecr.aws
	date > $@


$(TMP)/docker-run.stamp.txt : \
		$(TMP)/docker-build.stamp.txt \
		$(TMP)/.env \
		stop \
		| $$(dir $$@)
	-docker rm $(NEWS)
	docker run \
		--detach \
		--env-file $(TMP)/.env \
		--init \
		--name $(NEWS) \
		--platform linux/amd64 \
		--publish 8000:80 \
		--rm \
		$(NEWS)
	date > $@


$(TMP)/pip-install-requirements.stamp.txt : requirements.txt | $$(dir $$@)
	python3 -m pip install \
		--quiet --quiet --quiet \
		--requirement requirements.txt
	date > $@


$(TMP)/pip-install-dev-requirements.stamp.txt : dev-requirements.txt | $$(dir $$@)
	python3 -m pip install \
		--quiet --quiet --quiet \
		--requirement dev-requirements.txt
	date > $@


$(TMP)/pytest.stamp.txt : \
		$(source_files) \
		$(test_files) \
		$(TMP)/pip-install-requirements.stamp.txt \
		$(TMP)/pip-install-dev-requirements.stamp.txt \
		| $$(dir $$@)
	python3 -m pytest --quiet --quiet
	date > $@


$(TMP)/ :
	mkdir -p $@
