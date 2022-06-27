FROM jenkins/jenkins:2.319.3-lts-jdk11
ENV JENKINS_HOME /var/jenkins_home
USER root
RUN apt-get update && apt-get install -y lsb-release
COPY --chown=jenkins:root copy_files/jenkins_home $JENKINS_HOME
COPY --chown=777 copy_files/what_time /home
COPY --chown=777 copy_files/jenkins.yaml /home
USER jenkins
