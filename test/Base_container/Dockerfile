FROM jenkins/jenkins:2.319.3-lts-jdk11
ENV JENKINS_HOME /var/jenkins_home
USER root
RUN apt-get update && apt-get install -y lsb-release
USER jenkins
RUN jenkins-plugin-cli --plugins "blueocean:1.25.3" 
