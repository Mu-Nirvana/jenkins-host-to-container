
# Basic process to launch Jenkins

1. Build and Run the Jenkins image:
`$ make`

2. Check container health:
`$ docker ps`

3. Login to container at https://localhost:8080 (port 8000 for Copy_jenkins)

4. Once Jenkins has finished starting login with the password attained by running the command:
`$ docker container exex basejenkins cat /var/jenkins_home/secrets/initialAdminPassword` (Replace basejenkins with copyjenkins as needed)

5. (Base only) Select custom plugins and select `none` at the top of the menu

6. Have fun

## Make Specifics

### Build
`$ make build`: Builds only the image

### Run 
`$ make run`: Runs the container without building the image

### Clear
`$ make clear`: Removes all images and artifacts

### Clean (Copy_container only)
Used internally to remove artifacts after build

### Extract (Copy_container only)
Used internally to extract files from archive

### Variables
`BUILDOPTIONS:=--rm` Specify options for docker build
`RUNOPTIONS:=--restart=on-failure --detach` Specify options for docker run
`TAG:=test_base` Image tag (test_copy for Copy_container)
`CONTAINER:=basejenkins` Container name (copyjenkins for Copy_container)
`IP:=127.0.0.1` Jenkins publish IP
`PORT:=8080`Jenkins Publish Port
`EXTRACT:=~/Downloads/jenkins_home.tar` jenkins_home archive path (Copy_container only)

Overwrite variables with the following syntax: `$ make \<var>=\<value>

## Helpful commands

### Stop container
`$ docker stop <container name>`

### Start container
`$ docker start <container name>`

### Shell into container
`$ docker container exec -it <container name> /bin/bash`
Optionally add `-u root` before `-it` to gain root privileges
