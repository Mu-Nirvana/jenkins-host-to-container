BUILDOPTIONS:=--rm
RUNOPTIONS:=--restart=on-failure --detach
TAG:=test_base
CONTAINER:=basejenkins
IP:=127.0.0.1
PORT:=


all: build remove run

build: Dockerfile
	@echo "\nBuild docker image with tag $(TAG)\n"
	docker build $(BUILDOPTIONS) -t $(TAG) .

run:
	@echo "\nRunning docker container $(CONTAINER)\n"
	docker run --name=$(CONTAINER) $(RUNOPTIONS) --publish $(IP):$(PORT):8080 $(TAG)

remove:
	@echo "\nRemoving docker container $(CONTAINER)\n"
	 -docker stop $(CONTAINER)
	 -docker rm $(CONTAINER)

clear:
	@echo "\nRemoving docker image $(TAG)\n"
	docker rmi $(TAG)
