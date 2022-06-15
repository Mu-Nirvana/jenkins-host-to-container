FROM jenkins/jenkins:2.319.3-lts-jdk11
USER root
RUN apt-get update && apt-get install -y lsb-release
COPY jenkins.yaml /home/jenkins.yaml
COPY Wacky /var/jenkins_home/jobs
USER jenkins
RUN jenkins-plugin-cli --plugins "blueocean:1.25.3" 
