
# jenkins-host-to-container
Work-in-progress project aiming to create a highly automated tool to containerize a Jenkins server for cloud hosting (AKS and EKS).

Future goals include automated assistance to transition configuration from web UI to Jcasc, and Job/Pipeline configuration to yaml with Jenkins Job Builder.

## Project structure

* [testEnv](testEnv) Contains test environments for different Jenkins server setups
* [testEnv/Base_container](test/Env/Base_container)  Is a basic Jenkins docker container with no configuration predefined
* [testEnv/Copy_container](test/Env/Copy_container)  Is a Jenkins docker container built using a direct copy of another Jenkins server jenkins_home directory
* [src](src) Contains source code for the tool
