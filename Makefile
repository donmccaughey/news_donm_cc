TMP ?= $(abspath tmp)
NEWS := news


.SECONDEXPANSION :


.PHONY : all
all : build


.PHONY : build
build : $(TMP)/Docker-build.date.txt


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
deploy : $(TMP)/aws-create-container-service-deployment.json.txt


.PHONY : push
push : $(TMP)/Docker-push.date.txt


.PHONY : run
run : $(TMP)/Docker-run.id.txt


.PHONY : shell
shell: $(TMP)/Docker-run.id.txt
	docker exec \
		--interactive \
		--tty \
		$(NEWS) sh


.PHONY : stop
stop :
	-docker stop $(NEWS)
	rm -rf $(TMP)/Docker-run.id.txt


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
	src/news/items.py \
	src/news/source.py \
	src/news/store.py \
	src/news/url.py \
	src/templates/home.html


$(TMP)/.env :
	printf "AWS_ACCESS_KEY_ID=%s\n" "$$(aws configure get aws_access_key_id)" >> $@
	printf "AWS_SECRET_ACCESS_KEY=%s\n" "$$(aws configure get aws_secret_access_key)" >> $@
	printf "AWS_DEFAULT_REGION=us-west-2\n" >> $@
	chmod 600 $@


$(TMP)/create-container-service-deployment.json : aws/create-container-service-deployment.template.json
	sed \
		-e "s/{{AWS_ACCESS_KEY_ID}}/$$(aws configure get aws_access_key_id)/g" \
		-e "s/{{AWS_SECRET_ACCESS_KEY}}/$$(aws configure get aws_secret_access_key)/g" \
		$< > $@


$(TMP)/aws-create-container-service-deployment.json.txt : \
		$(TMP)/create-container-service-deployment.json \
		$(TMP)/Docker-push.date.txt \
		| $$(dir $$@)
	aws lightsail create-container-service-deployment \
		--cli-input-json "$$(jq -c . $(TMP)/create-container-service-deployment.json)" \
		--output json \
		--region us-west-2 \
		--service-name news \
		> $@ \
		|| ( cat $@ && rm $@ && false )


$(TMP)/Docker-build.date.txt : $(container_src) | $$(dir $$@)
	docker build \
		--file $< \
		--platform linux/amd64 \
		--tag $(NEWS) \
		--quiet \
		$(dir $<)
	date > $@


$(TMP)/Docker-push.date.txt : $(TMP)/Docker-build.date.txt | $$(dir $$@)
	aws ecr-public get-login-password --region us-east-1 \
        | docker login --username AWS --password-stdin public.ecr.aws
	docker tag news public.ecr.aws/d2g3p0u7/news
	docker push --quiet public.ecr.aws/d2g3p0u7/news
	docker logout public.ecr.aws
	date > $@


$(TMP)/Docker-run.id.txt : \
		$(TMP)/Docker-build.date.txt \
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
