FROM ${image} 
ENV JENKINS_HOME /var/jenkins_home
USER root
RUN apt-get update
COPY installdeps /
COPY ${installDeps.depFile} /
RUN /installdeps /${installDeps.depFile}; rm /installdeps /${installDeps.depFile}
