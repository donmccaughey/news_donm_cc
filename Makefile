AWS_ACCESS_KEY_ID ?= $(shell aws configure get aws_access_key_id)
AWS_SECRET_ACCESS_KEY ?= $(shell aws configure get aws_secret_access_key)
REDDIT_PRIVATE_RSS_FEED ?= $(shell cat secrets/reddit-private-rss-feed.txt)
TMP ?= $(abspath tmp)

# generate a SEED for test randomization if not provided
ifeq ($(origin SEED), undefined)
	generate_seed := import random; print(random.randint(0, 2**32-1))
	SEED := $(shell uv run python -c '$(generate_seed)')
endif

container_files := \
	.dockerignore \
	$(shell find container -type f -not -name '.DS_Store')
news_container := news
news_image := news
python_files := $(shell find src -type f -name '*.py')
source_files := $(filter-out %_test.py, $(python_files))


.SECONDEXPANSION :


.PHONY : all
all : build


.PHONY : build
build : $(TMP)/podman-build.stamp


.PHONY : check
check : \
		$(TMP)/coverage.sqlite \
		$(TMP)/mypy.stamp


.PHONY : clean
clean : stop
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	-podman rm $(news_container)
	find gen -mindepth 1 ! -name 'README.md' -delete
	find src -type d -name '__pycache__' -delete
	rm -rf $(TMP)


.PHONY : clobber
clobber : clean
	rm -rf .venv
	-podman image rm --force $(news_image)


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
	PYTHONPATH=src \
	REDDIT_PRIVATE_RSS_FEED="$(REDDIT_PRIVATE_RSS_FEED)" \
		uv run -m extractor \
			--cache-dir="$(TMP)" \
			--no-store


.PHONY : logs
logs :
	uv run scripts/logs.py


.PHONY : mypy
mypy : test/mypy.txt


.PHONY : push
push : $(TMP)/podman-push.stamp


.PHONY : run
run : $(TMP)/podman-run.stamp


.PHONY : shell
shell : $(TMP)/podman-run.stamp
	podman exec \
		--interactive \
		--tty \
		$(news_image) sh -l


.PHONY : status
status :
	podman inspect $(news_container) | jq '.[0].State'


.PHONY : stop
stop :
	-podman stop $(news_container)
	rm -rf $(TMP)/podman-run.stamp


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


$(TMP)/.env : | $$(dir $$@)
	printf "AWS_ACCESS_KEY_ID=%s\n" "$(AWS_ACCESS_KEY_ID)" >> $@
	printf "AWS_SECRET_ACCESS_KEY=%s\n" "$(AWS_SECRET_ACCESS_KEY)" >> $@
	printf "AWS_DEFAULT_REGION=us-west-2\n" >> $@
	printf "REDDIT_PRIVATE_RSS_FEED=%s\n" "$(REDDIT_PRIVATE_RSS_FEED)" >> $@
	chmod 600 $@


$(TMP)/aws-lightsail-create-container-service-deployment.stamp : \
		$(TMP)/create-container-service-deployment.json \
		$(TMP)/podman-push.stamp
	aws lightsail create-container-service-deployment \
		--cli-input-json \
			"$$(jq -c . $(TMP)/create-container-service-deployment.json)" \
		--output json \
		--region us-west-2 \
		--service-name news \
		> $(TMP)/lightsail-deployment.json
	touch $@


$(TMP)/coverage.sqlite : $(python_files) $(TMP)/uv-sync.stamp
	@printf 'SEED=%i\n' '$(SEED)'| tee $(TMP)/pytest.seed
	COVERAGE_FILE=$@ \
		uv run -m pytest \
			--cov \
			--cov-report= \
			--override-ini cache_dir=$(TMP)/.pytest_cache \
			--quiet --quiet \
			--randomly-seed=$(SEED)
	@printf '%s%% code coverage\n' \
		$$(uv run coverage report --data-file=$@ --format=total --precision=2)
	uv run coverage html \
		--data-file=$@ \
		--directory=$(TMP)/coverage-report \
		--quiet
	printf '%i\n' '$(SEED)' > $(TMP)/pytest.seed


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


$(TMP)/mypy.stamp : $(python_files) $(TMP)/uv-sync.stamp
	uv run -m mypy \
		--cache-dir $(TMP)/.mypy_cache \
		src
	touch $@


$(TMP)/podman-build.stamp : \
		$(container_files) \
		gen/apk_add_py3_packages \
		gen/version.txt \
		$(TMP)/coverage.sqlite \
		$(TMP)/mypy.stamp
	podman build \
		--file container/Dockerfile \
		--platform linux/amd64 \
		--quiet \
		--tag $(news_image) \
		.
	touch $@


$(TMP)/podman-push.stamp : $(TMP)/podman-build.stamp
	aws ecr-public get-login-password --region us-east-1 \
        | podman login --username AWS --password-stdin public.ecr.aws
	podman tag $(news_image) public.ecr.aws/d2g3p0u7/news
	podman push --quiet public.ecr.aws/d2g3p0u7/news
	podman logout public.ecr.aws
	touch $@


$(TMP)/podman-run.stamp : \
		$(TMP)/podman-build.stamp \
		$(TMP)/.env \
		stop
	-podman rm $(news_container)
	podman run \
		--detach \
		--env-file $(TMP)/.env \
		--init \
		--name $(news_container) \
		--platform linux/amd64 \
		--publish 8000:80 \
		--rm \
		$(news_image)
	touch $@


$(TMP)/uv-sync.stamp : uv.lock | $$(dir $$@)
	uv sync --frozen
	touch $@


gen \
$(TMP)/ :
	mkdir -p $@
