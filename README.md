
# jenkins-host-to-container
Work-in-progress project aiming to create a highly automated tool to containerize a Jenkins server for cloud hosting (AKS and EKS).

Future goals include automated assistance to transition configuration from web UI to Jcasc, and Job/Pipeline configuration to yaml with [Jenkins Job Builder](https://jenkins-job-builder.readthedocs.io/en/latest/).

Sister project to create K8s cloud infrastructure to run Jenkins (Currently only AKS support) [Mu-Nirvana/jenkins-cloud-create](https://github.com/Mu-Nirvana/jenkins-cloud-create)

## Project structure

* [test](test) Contains test cases for different Jenkins server configs
  * [test/Base_container](test/Base_container)  Is a basic Jenkins docker container with no configuration predefined
  * [test/Copy_container](test/Copy_container)  Is a Jenkins docker container built using a direct copy of another Jenkins server jenkins_home directory
  * [test/Autogenerate_container](test/AUtogenerate_container) Is a docker container built automatically from a copied Jenkins_server
* [src](src) Contains source code for the tool

## Basic process to launch Jenkins test environments


1. cd [test/Base_container](test/Base_container)

2. Build and Run the Jenkins image:
`$ make`

3. Check container health:
`$ docker ps`

4. Login to container at `https://localhost:{HOST_PORT}`

5. Once Jenkins has finished starting login with the password attained by running the command:
`$ docker container exec basejenkins cat /var/jenkins_home/secrets/initialAdminPassword` (Replace basejenkins with copyjenkins as needed)

6. Simply `x` out of plugin setup for this test case & start using Jenkins:
   ![alt text](docs/customize_jenkins.png "Customize jenkins Plugins")
7. Have fun

Note: For [test/Copy_container](test/Copy_container) testing, you require a tar file of Jenkins home directory to test your migration.

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
`PORT:=`Jenkins Publish Port
`EXTRACT:=~/Downloads/jenkins_home.tar` jenkins_home archive path (Copy_container only)

Overwrite variables with the following syntax: `$ make \<var>=\<value>`

##  Build and run Auto-generate environment
[test/Autogenerate_container](test/Autogenerate) 
### Build and start container
`$ ../../src/python/autobuilder.py run example_copy.yaml Dockerfile_Template`

## Autobuild.py instructions
### Run program
`python3 autobuilder.py run <path to config yaml> <path to Dockerfile_Template>`
Optionally replace run with build to only build the image or with dry to only create a Dockerfile
### Config Yaml
Basic file example: [src/example_files/example_config.yaml](src/example_files/example_config.yaml)
The `container:` section holds information used to generate the Dockerfile
* `image:`  Jenkins base image
* `jenkins_home_src:` Path to jenkins_home archive [copying an instance](#copying-a-jenkins-instance)
* `install_deps_src:` Path to installdeps script ([src/scripts/installdeps](src/scripts/installdeps))
* `dependencies:` Path to dependency list [copying an instance](#copying-a-jenkins-instance)
* `other_files:` List of other files to copy to jenkins
	* `src:` Source path of file
	   `dest:` Container destination path
	   `owner:` File ownership
## Copying a jenkins instance
### Copy jenkins home
*On target jenkins instance* run these commands to create the copy. Copy the resulting the files to the build machine.
#### Create archive
`$ tar -czf jenkins_home.tar /var/jenkins_home` (jenkins_home may be at another location or stored in `$JENKINS_HOME`  
**If the jenkins home directory is not named jenkins_home** do the following instead:  
`$ tar -czf jenkins_home.tar --transform s/<dir name>/jenkins_home/ <dir name>` Note: use `-s /^<dir name>/jenkins_home/` if using BSD tar instead of GNU
#### Create dependency list
`$ apt list --manual-installed=true > targetdeps.txt`

## Helpful commands

### Stop container
`$ docker stop <container name>`

### Start container
`$ docker start <container name>`

### Shell into container
`$ docker container exec -it <container name> /bin/bash`
Optionally add `-u root` before `-it` to gain root privileges
