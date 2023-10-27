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
	rm -rf $(TMP)


.PHONY : cov
cov : $(TMP)/.coverage


.PHONY : debug
debug : $(TMP)/pip-install-requirements.stamp.txt
	FLASK_CACHE_DIR="$(TMP)" \
	FLASK_RUN_PORT=8001 \
	flask \
		--app src/server \
		--debug \
		run


.PHONY : deploy
deploy : $(TMP)/aws-lightsail-create-container-service-deployment.stamp.txt


.PHONY : extract
extract : $(TMP)/pip-install-requirements.stamp.txt
	REDDIT_PRIVATE_RSS_FEED="$(REDDIT_PRIVATE_RSS_FEED)" \
	python3 src/extractor.py \
		--cache-dir="$(TMP)" \
		--no-store


.PHONY : logs
logs :
	python3 scripts/logs.py


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
	requirements.txt \
	$(shell find container -type f \! -name .DS_Store)

python_files := $(shell find src -type f \! -name .DS_Store)

script_files := \
	scripts/logs.py

source_files := $(filter-out %_test.py, $(python_files))

test_files := $(filter %_test.py, $(python_files))


test/mypy.txt : .mypy.ini $(TMP)/pip-install-requirements-dev.stamp.txt $(TMP)/pytest.stamp.txt
	python3 -m mypy src | tee test/mypy.txt


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


$(TMP)/create-container-service-deployment.json : aws/create-container-service-deployment.template.json | $$(dir $$@)
	python3 scripts/fillin.py \
		--input $< \
		--output $@ \
		--name 'AWS_ACCESS_KEY_ID' --value '$(AWS_ACCESS_KEY_ID)' \
		--name 'AWS_SECRET_ACCESS_KEY' --value '$(AWS_SECRET_ACCESS_KEY)' \
		--name 'REDDIT_PRIVATE_RSS_FEED' --value '$(REDDIT_PRIVATE_RSS_FEED)'
	chmod 600 $@


$(TMP)/docker-build.stamp.txt : \
		$(container_files) \
		$(source_files) \
		| $$(dir $$@)
	git rev-parse --short HEAD > $(TMP)/version.txt
	docker build \
		--build-arg version_file="$(TMP)/version.txt" \
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


$(TMP)/pip-install-requirements.stamp.txt : requirements.txt | $$(dir $$@)
	python3 -m pip install \
		--quiet --quiet --quiet \
		--requirement $<
	date > $@


$(TMP)/pip-install-requirements-dev.stamp.txt : requirements-dev.txt | $$(dir $$@)
	python3 -m pip install \
		--quiet --quiet --quiet \
		--requirement $<
	date > $@


$(TMP)/pytest.stamp.txt : \
		$(source_files) \
		$(test_files) \
		$(TMP)/pip-install-requirements.stamp.txt \
		$(TMP)/pip-install-requirements-dev.stamp.txt \
		| $$(dir $$@)
	python3 -m pytest --quiet --quiet
	date > $@


$(TMP)/.coverage : \
		.coveragerc \
		$(source_files) \
		$(test_files) \
		$(TMP)/pip-install-requirements.stamp.txt \
		$(TMP)/pip-install-requirements-dev.stamp.txt \
		| $$(dir $$@)
	COVERAGE_FILE=$@ \
	python3 -m pytest \
		--cov \
		--cov-config=$< \
		--cov-report=html:"$(TMP)/coverage" \
		--cov-report=xml:"$(TMP)/coverage.xml" \
		--quiet --quiet


$(TMP)/ :
	mkdir -p $@
