AWS_ACCESS_KEY_ID ?= $(shell aws configure get aws_access_key_id)
AWS_SECRET_ACCESS_KEY ?= $(shell aws configure get aws_secret_access_key)
REDDIT_PRIVATE_RSS_FEED ?= $(shell cat secrets/reddit-private-rss-feed.txt)
TMP ?= $(abspath tmp)

NEWS := news  # container name


.SECONDEXPANSION :


.PHONY : all
all : build


.PHONY : build
build : $(TMP)/docker-build.stamp.txt


.PHONY : check
check : test/mypy.txt


.PHONY : clean
clean : stop
	-docker rm $(NEWS)
	find gen -mindepth 1 ! -name 'README.md' -exec rm -f {} +
	rm -rf $(TMP)


.PHONY : clobber
clobber : clean
	rm -rf .venv


.PHONY : cov
cov : $(TMP)/.coverage


.PHONY : debug
debug : $(TMP)/uv-sync.stamp.txt
	FLASK_CACHE_DIR="$(TMP)" \
	FLASK_RUN_PORT=8001 \
	uv run flask \
		--app src/server \
		--debug \
		run


.PHONY : deploy
deploy : $(TMP)/aws-lightsail-create-container-service-deployment.stamp.txt


.PHONY : extract
extract : $(TMP)/uv-sync.stamp.txt
	REDDIT_PRIVATE_RSS_FEED="$(REDDIT_PRIVATE_RSS_FEED)" \
	uv run src/extractor.py \
		--cache-dir="$(TMP)" \
		--no-store


.PHONY : logs
logs :
	uv run scripts/logs.py


.PHONY : mypy
mypy : test/mypy.txt


.PHONY : push
push : $(TMP)/docker-push.stamp.txt


.PHONY : run
run : $(TMP)/docker-run.stamp.txt


.PHONY : shell
shell : $(TMP)/docker-run.stamp.txt
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
	container/crontabs/news \
	container/nginx/nginx.conf \
	container/nginx/error_pages/404.html \
	container/nginx/error_pages/500.html \
	container/nginx/error_pages/502.html \
	container/nginx/error_pages/503.html \
	container/nginx/error_pages/504.html \
	container/profile.d/dir.sh \
	container/sbin/check-health \
	container/sbin/extract \
	container/sbin/news \
	container/sbin/serve \
	container/wwwroot/robots.txt \
	container/wwwroot/sitemap.txt \
	gen/apk_add_py3_packages \
	gen/version.txt

python_files := \
	src/extractor.py \
	src/gunicorn.conf.py \
	src/health_check.py \
	src/query.py \
	src/youtube_user.py \
	\
	src/extractor/__init__.py \
	src/extractor/cached_feeds.py \
	src/extractor/cached_news.py \
	src/extractor/options.py \
	src/extractor/s3_store.py \
	src/extractor/s3_store_test.py \
	\
	src/feeds/__init__.py \
	src/feeds/aggregator.py \
	src/feeds/aggregator_test.py \
	src/feeds/daring_fireball.py \
	src/feeds/daring_fireball_test.py \
	src/feeds/feed.py \
	src/feeds/feed_test.py \
	src/feeds/feeds.py \
	src/feeds/feeds_test.py \
	src/feeds/reddit.py \
	src/feeds/reddit_test.py \
	src/feeds/skip_sites.py \
	src/feeds/streetsblog.py \
	src/feeds/streetsblog_test.py \
	\
	src/health/__init__.py \
	src/health/health.py \
	src/health/health_test.py \
	src/health/jobs.py \
	src/health/processes.py \
	src/health/servers.py \
	\
	src/news/__init__.py \
	src/news/index.py \
	src/news/index_test.py \
	src/news/item.py \
	src/news/item_test.py \
	src/news/items.py \
	src/news/news.py \
	src/news/news_test.py \
	src/news/source.py \
	src/news/source_test.py \
	\
	src/news/url/__init__.py \
	src/news/url/clean.py \
	src/news/url/clean_test.py \
	src/news/url/identity.py \
	src/news/url/identity_test.py \
	src/news/url/normalized_url.py \
	src/news/url/normalized_url_test.py \
	src/news/url/rewrite.py \
	src/news/url/rewrite_test.py \
	src/news/url/url.py \
	src/news/url/url_test.py \
	\
	src/serialize/__init__.py \
	src/serialize/encodable.py \
	src/serialize/jsontype.py \
	src/serialize/serializable.py \
	\
	src/server/__init__.py \
	src/server/cached_news.py \
	src/server/create_app.py \
	src/server/doc.py \
	src/server/error_handlers.py \
	src/server/news_doc.py \
	src/server/search_doc.py \
	src/server/site_doc.py \
	src/server/sites_doc.py \
	src/server/template_filters.py \
	src/server/utility.py \
	src/server/views.py \
	\
	src/server/templates/doc.html \
	src/server/templates/news.html \
	src/server/templates/search.html \
	src/server/templates/site.html \
	src/server/templates/sites.html \
	\
	src/utility/__init__.py \
	src/utility/cached_file.py \
	src/utility/cached_file_test.py \
	src/utility/formats.py \
	src/utility/formats_test.py \
	src/utility/no_store.py \
	src/utility/no_store_test.py \
	src/utility/page.py \
	src/utility/page_test.py \
	src/utility/read_only_store.py \
	src/utility/store.py

script_files := \
	scripts/logs.py

source_files := $(filter-out %_test.py, $(python_files))

test_files := $(filter %_test.py, $(python_files))


gen/apk_add_py3_packages : pyproject.toml scripts/py3apk.py $(TMP)/uv-sync.stamp.txt | $$(dir $$@)
	uv run scripts/py3apk.py \
		--input $< \
		--output $@


gen/version.txt : \
		container/Dockerfile \
		$(container_files) \
		$(source_files) \
		| $$(dir $$@)
	git rev-parse --short HEAD > $@


test/mypy.txt : .mypy.ini $(TMP)/uv-sync.stamp.txt $(TMP)/pytest.stamp.txt
	uv run -m mypy --check-untyped-defs src | tee test/mypy.txt


uv.lock : pyproject.toml .python-version
	uv sync
	touch $@


$(TMP)/.env : | $$(dir $$@)
	printf "AWS_ACCESS_KEY_ID=%s\n" "$(AWS_ACCESS_KEY_ID)" >> $@
	printf "AWS_SECRET_ACCESS_KEY=%s\n" "$(AWS_SECRET_ACCESS_KEY)" >> $@
	printf "AWS_DEFAULT_REGION=us-west-2\n" >> $@
	printf "REDDIT_PRIVATE_RSS_FEED=%s\n" "$(REDDIT_PRIVATE_RSS_FEED)" >> $@
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


$(TMP)/create-container-service-deployment.json : \
		aws/create-container-service-deployment.template.json \
		scripts/fillin.py \
		| $$(dir $$@)
	uv run scripts/fillin.py \
		--input $< \
		--output $@ \
		--name 'AWS_ACCESS_KEY_ID' --value '$(AWS_ACCESS_KEY_ID)' \
		--name 'AWS_SECRET_ACCESS_KEY' --value '$(AWS_SECRET_ACCESS_KEY)' \
		--name 'REDDIT_PRIVATE_RSS_FEED' --value '$(REDDIT_PRIVATE_RSS_FEED)'
	chmod 600 $@


$(TMP)/docker-build.stamp.txt : \
		container/Dockerfile \
		$(container_files) \
		$(source_files) \
		| $$(dir $$@)
	docker build \
		--file $< \
		--platform linux/amd64 \
		--tag $(NEWS) \
		--quiet \
		.
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


$(TMP)/pytest.stamp.txt : \
		$(source_files) \
		$(test_files) \
		$(TMP)/uv-sync.stamp.txt \
		| $$(dir $$@)
	uv run -m pytest --quiet --quiet
	date > $@


$(TMP)/uv-sync.stamp.txt : uv.lock | $$(dir $$@)
	uv sync --frozen
	date > $@


$(TMP)/.coverage : \
		.coveragerc \
		$(source_files) \
		$(test_files) \
		$(TMP)/uv-sync.stamp.txt \
		| $$(dir $$@)
	COVERAGE_FILE=$@ \
	uv run -m pytest \
		--cov \
		--cov-config=$< \
		--cov-report=html:"$(TMP)/coverage" \
		--cov-report=xml:"$(TMP)/coverage.xml" \
		--quiet --quiet


gen \
$(TMP)/ :
	mkdir -p $@
