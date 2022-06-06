
# Basic process to launch Jenkins

1. Build and Run the Jenkins image:
`$ ./launch <image name> <container name> build run`

2. Check container health:
`$ docker ps`

3. Login to container at https://localhost:8080

4. Once Jenkins has finished starting login with the password attained by running the command:
`$ docker container exec <container name> cat /var/lib/jenkins/secrets/initialAdminPassword`

5. Select custom plugins and select `none` at the top of the menu

6. Have fun

## Helpful commands

### Run container without building image
`$ ./launch <image name> <container name> run`

### Build container without building image
`$ ./launch <image name> <container name> build` 

### Stop container
`$ docker stop <container name>`

### Start container
`$ docker start <container name>`

### Shell into container
`$ docker container exec -it <container name> /bin/bash`
Optionally add `-u root` before `-it` to gain root privileges
