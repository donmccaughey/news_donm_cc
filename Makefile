AWS_ACCESS_KEY_ID ?= $(shell aws configure get aws_access_key_id)
AWS_SECRET_ACCESS_KEY ?= $(shell aws configure get aws_secret_access_key)
TMP ?= $(abspath tmp)

NEWS := news


.SECONDEXPANSION :


.PHONY : all
all : build


.PHONY : build
build : $(TMP)/docker-build.stamp.txt


.PHONY : clean
clean : stop
	-docker rm $(NEWS)
	rm -rf $(TMP)


.PHONY : debug
debug :
	python3 src/extractor.py \
		--cache-path="$(TMP)/news.json" \
		--no-store
	FLASK_NEWS_PATH="$(TMP)/news.json" \
		flask --app src/server --debug run


.PHONY : deploy
deploy : $(TMP)/aws-lightsail-create-container-service-deployment.stamp.txt


.PHONY : push
push : $(TMP)/docker-push.stamp.txt


.PHONY : run
run : $(TMP)/docker-run.stamp.txt


.PHONY : shell
shell: $(TMP)/docker-run.stamp.txt
	docker exec \
		--interactive \
		--tty \
		$(NEWS) sh


.PHONY : stop
stop :
	-docker stop $(NEWS)
	rm -rf $(TMP)/docker-run.stamp.txt


container_src := \
	Dockerfile \
	requirements.txt \
	nginx/nginx.conf \
	nginx/default/404.html \
	nginx/default/500.html \
	nginx/default/502.html \
	nginx/default/503.html \
	nginx/default/504.html \
	nginx/default/index.html \
	sbin/news \
	src/extractor.py \
	src/server.py \
	src/news/__init__.py \
	src/news/cache.py \
	src/news/item.py \
	src/news/news.py \
	src/news/source.py \
	src/news/store.py \
	src/news/url.py \
	src/templates/home.html


$(TMP)/.env : | $$(dir $$@)
	printf "AWS_ACCESS_KEY_ID=%s\n" "$(AWS_ACCESS_KEY_ID)" >> $@
	printf "AWS_SECRET_ACCESS_KEY=%s\n" "$(AWS_SECRET_ACCESS_KEY)" >> $@
	printf "AWS_DEFAULT_REGION=us-west-2\n" >> $@
	chmod 600 $@


$(TMP)/create-container-service-deployment.json : aws/create-container-service-deployment.template.json | $$(dir $$@)
	sed \
		-e "s/{{AWS_ACCESS_KEY_ID}}/$(AWS_ACCESS_KEY_ID)/g" \
		-e "s/{{AWS_SECRET_ACCESS_KEY}}/$(AWS_SECRET_ACCESS_KEY)/g" \
		$< > $@


$(TMP)/aws-lightsail-create-container-service-deployment.stamp.txt : \
		$(TMP)/create-container-service-deployment.json \
		$(TMP)/docker-push.stamp.txt \
		| $$(dir $$@)
	aws lightsail create-container-service-deployment \
		--cli-input-json "$$(jq -c . $(TMP)/create-container-service-deployment.json)" \
		--output json \
		--region us-west-2 \
		--service-name news \
		> $@ \
		|| ( cat $@ && rm $@ && false )


$(TMP)/docker-build.stamp.txt : $(container_src) | $$(dir $$@)
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
		$(NEWS) > $@


$(TMP)/ :
	mkdir -p $@
