AWS_ACCESS_KEY_ID ?= $(shell aws configure get aws_access_key_id)
AWS_SECRET_ACCESS_KEY ?= $(shell aws configure get aws_secret_access_key)
REDDIT_PRIVATE_RSS_FEED ?= $(shell cat secrets/reddit-private-rss-feed.txt)
TMP ?= $(abspath tmp)

NEWS := news  # container name


container_files := \
	.dockerignore \
	$(shell find container -type f -not -name '.DS_Store')
python_files := $(shell find src -type f -name '*.py')
source_files := $(filter-out %_test.py, $(python_files))


.SECONDEXPANSION :


.PHONY : all
all : build


.PHONY : build
build : $(TMP)/docker-build.stamp


.PHONY : check
check : test/mypy.txt


.PHONY : clean
clean : stop
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	-docker rm $(NEWS)
	find gen -mindepth 1 ! -name 'README.md' -delete
	find src -type d -name '__pycache__' -delete
	rm -rf $(TMP)


.PHONY : clobber
clobber : clean
	rm -rf .venv


.PHONY : cov
cov : $(TMP)/coverage.sqlite


.PHONY : debug
debug : $(TMP)/uv-sync.stamp
	FLASK_CACHE_DIR="$(TMP)" \
	FLASK_RUN_PORT=8001 \
		uv run flask \
			--app src/server \
			--debug \
			run


.PHONY : deploy
deploy : $(TMP)/aws-lightsail-create-container-service-deployment.stamp


.PHONY : extract
extract : $(TMP)/uv-sync.stamp
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
push : $(TMP)/docker-push.stamp


.PHONY : run
run : $(TMP)/docker-run.stamp


.PHONY : shell
shell : $(TMP)/docker-run.stamp
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
	rm -rf $(TMP)/docker-run.stamp


uv.lock : pyproject.toml .python-version
	uv sync
	touch $@


gen/apk_add_py3_packages : \
		pyproject.toml \
		scripts/py3apk.py \
		$(TMP)/uv-sync.stamp \
		| $$(dir $$@)
	uv run scripts/py3apk.py \
		--input pyproject.toml \
		--output $@


gen/version.txt : $(container_files) $(source_files) | $$(dir $$@)
	git rev-parse --short HEAD > $@


test/mypy.txt : $(TMP)/uv-sync.stamp $(TMP)/coverage.sqlite
	uv run -m mypy \
		--cache-dir $(TMP)/.mypy_cache \
		src \
		| tee test/mypy.txt


$(TMP)/.env : | $$(dir $$@)
	printf "AWS_ACCESS_KEY_ID=%s\n" "$(AWS_ACCESS_KEY_ID)" >> $@
	printf "AWS_SECRET_ACCESS_KEY=%s\n" "$(AWS_SECRET_ACCESS_KEY)" >> $@
	printf "AWS_DEFAULT_REGION=us-west-2\n" >> $@
	printf "REDDIT_PRIVATE_RSS_FEED=%s\n" "$(REDDIT_PRIVATE_RSS_FEED)" >> $@
	chmod 600 $@


$(TMP)/aws-lightsail-create-container-service-deployment.stamp : \
		$(TMP)/create-container-service-deployment.json \
		$(TMP)/docker-push.stamp
	aws lightsail create-container-service-deployment \
		--cli-input-json \
			"$$(jq -c . $(TMP)/create-container-service-deployment.json)" \
		--output json \
		--region us-west-2 \
		--service-name news \
		> $(TMP)/lightsail-deployment.json
	touch $@


$(TMP)/coverage.sqlite : $(python_files) $(TMP)/uv-sync.stamp
	COVERAGE_FILE=$@ \
		uv run -m pytest \
			--cov \
			--cov-report= \
			--override-ini cache_dir=$(TMP)/.pytest_cache \
			--quiet --quiet
	@printf '%s%% code coverage\n' \
		$$(uv run coverage report --data-file=$@ --format=total --precision=2)
	uv run coverage html \
		--data-file=$@ \
		--directory=$(TMP)/coverage-report \
		--quiet


$(TMP)/create-container-service-deployment.json : \
		aws/create-container-service-deployment.template.json \
		scripts/fillin.py \
		| $$(dir $$@)
	uv run scripts/fillin.py \
		--input aws/create-container-service-deployment.template.json \
		--output $@ \
		--name 'AWS_ACCESS_KEY_ID' --value '$(AWS_ACCESS_KEY_ID)' \
		--name 'AWS_SECRET_ACCESS_KEY' --value '$(AWS_SECRET_ACCESS_KEY)' \
		--name 'REDDIT_PRIVATE_RSS_FEED' --value '$(REDDIT_PRIVATE_RSS_FEED)'
	chmod 600 $@


$(TMP)/docker-build.stamp : \
		$(container_files) \
		gen/apk_add_py3_packages \
		gen/version.txt \
		$(source_files) \
		| $$(dir $$@)
	docker build \
		--file container/Dockerfile \
		--platform linux/amd64 \
		--tag $(NEWS) \
		--quiet \
		.
	touch $@


$(TMP)/docker-push.stamp : $(TMP)/docker-build.stamp
	aws ecr-public get-login-password --region us-east-1 \
        | docker login --username AWS --password-stdin public.ecr.aws
	docker tag news public.ecr.aws/d2g3p0u7/news
	docker push --quiet public.ecr.aws/d2g3p0u7/news
	docker logout public.ecr.aws
	touch $@


$(TMP)/docker-run.stamp : \
		$(TMP)/docker-build.stamp \
		$(TMP)/.env \
		stop
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
	touch $@


$(TMP)/uv-sync.stamp : uv.lock | $$(dir $$@)
	uv sync --frozen
	touch $@


gen \
$(TMP) :
	mkdir -p $@
