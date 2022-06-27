FROM jenkins/jenkins:2.319.3-lts-jdk11
ENV JENKINS_HOME /var/jenkins_home
USER root
RUN apt-get update && apt-get install -y lsb-release
RUN apt install tar
COPY --chown=jenkins:root copy_files/jenkins_home.tar $JENKINS_HOME.tar
RUN tar -xf $JENKINS_HOME.tar && rm $JENKINS_HOME.tar
COPY --chmod=777 copy_files/what_time /home
USER jenkins
