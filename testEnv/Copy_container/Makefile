BUILDOPTIONS:=--rm
RUNOPTIONS:=--restart=on-failure --detach
TAG:=test_copy
CONTAINER:=copyjenkins
IP:=127.0.0.1
PORT:=8000
EXTRACT:=~/Downloads/jenkins_home.tar


all: build remove run clean

build: Dockerfile extract 
	@echo "\nBuild docker image with tag $(TAG)\n"
	docker build $(BUILDOPTIONS) -t $(TAG) .

run:
	@echo "\nRunning docker container $(CONTAINER)\n"
	docker run --name=$(CONTAINER) $(RUNOPTIONS) --publish $(IP):$(PORT):8080 $(TAG)

remove:
	@echo "\nRemoving docker container $(CONTAINER)\n"
	 -docker stop $(CONTAINER)
	 -docker rm $(CONTAINER)

clear: remove
	@echo "\nRemoving docker image $(TAG)\n"
	-docker rmi $(TAG)
	@echo "\nRemoving jenkins_home\n"
	-rm -rf ./copy_files/jenkins_home

clean:
	@echo "\nRemoving jenkins_home\n"
	-rm -rf ./copy_files/jenkins_home

extract: 
	@echo "\nExtracting jenkins_home directory\n"
	tar -xf $(EXTRACT) -C ./copy_files
