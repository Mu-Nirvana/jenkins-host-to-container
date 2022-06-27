BUILDOPTIONS:=--restart=on-failure --detach
TAG:=test_base
CONTAINER:=basejenkins
IP:=127.0.0.1
PORT:=8080


all: build remove run

build: Dockerfile
	@echo "\nBuild docker image with tag $(TAG)\n"
	docker build $(OPTIONS) -t $(TAG) .

run:
	@echo "\nRunning docker container $(CONTAINER)\n"
	docker run --name=$(CONTAINER) $(BUILDOPTIONS) --publish $(IP):$(PORT):8080 $(TAG)

remove:
	@echo "\nRemoving docker container $(CONTAINER)\n"
	 -docker stop $(CONTAINER)
	 -docker rm $(CONTAINER)

clean:
	@echo "\nRemoving docker image $(TAG)\n"
	docker rmi $(TAG)
