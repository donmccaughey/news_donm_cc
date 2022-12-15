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


.PHONY : create
create : $(TMP)/Docker-create.id.txt


.PHONY : deploy
deploy : $(TMP)/aws-create-container-service-deployment.json.txt


.PHONY : push
push : $(TMP)/Docker-push.date.txt


.PHONY : shell
shell: $(TMP)/Docker-start.date.txt
	docker exec \
		--interactive \
		--tty \
		$(NEWS) sh


.PHONY : start
start : $(TMP)/Docker-start.date.txt


.PHONY : stop
stop :
	-docker stop $(NEWS)
	rm -rf $(TMP)/Docker-start.date.txt


nginx_files := \
	nginx/nginx.conf \
	nginx/default/404.html \
	nginx/default/500.html \
	nginx/default/502.html \
	nginx/default/503.html \
	nginx/default/504.html \
	nginx/default/index.html

src_files := src/server.py

sbin_files := sbin/news


$(TMP)/aws-create-container-service-deployment.json.txt : \
		$(TMP)/Docker-push.date.txt \
		aws/create-container-service-deployment.json \
		| $$(dir $$@)
	aws lightsail create-container-service-deployment \
		--cli-input-json "$$(<aws/create-container-service-deployment.json)" \
		--output json \
		--region us-west-2 \
		--service-name news \
		> $@ || rm $@


$(TMP)/Docker-build.date.txt : \
		Dockerfile \
		$(nginx_files) \
		$(src_files) \
		$(sbin_files) \
		| $$(dir $$@)
	docker build \
		--file $< \
		--platform linux/amd64 \
		--tag $(NEWS) \
		--quiet \
		$(dir $<)
	date > $@


$(TMP)/Docker-create.id.txt : stop $(TMP)/Docker-build.date.txt | $$(dir $$@)
	-docker rm $(NEWS)
	docker create \
		--init \
		--name $(NEWS) \
		--platform linux/amd64 \
		--publish 8000:80 \
		$(NEWS) > $@


$(TMP)/Docker-push.date.txt : $(TMP)/Docker-build.date.txt | $$(dir $$@)
	aws ecr-public get-login-password --region us-east-1 \
        | docker login --username AWS --password-stdin public.ecr.aws
	docker tag news public.ecr.aws/d2g3p0u7/news
	docker push public.ecr.aws/d2g3p0u7/news
	docker logout public.ecr.aws
	date > $@


$(TMP)/Docker-start.date.txt : $(TMP)/Docker-create.id.txt | $$(dir $$@)
	docker start $(NEWS)
	date > $@


$(TMP)/ :
	mkdir -p $@
