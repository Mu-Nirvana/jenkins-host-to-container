#!/bin/bash
if [ $# -gt 3 ]
then
  echo "Too many arguments please enter image name as the first argument and build/run as second and or third arguments"
  exit
fi
if [ $# -lt 2 ]
then
  echo "Enter image name and at least build or run"
  exit
fi

if [ "${2,,}" = "build" ] || [ "${3,,}" = "build" ]
then
  echo "\n\nBuilding the docker container\n\n"
  docker build -t ${1} .
fi
if [ "${2,,}" = "run" ] || [ "${3,,}" = "run" ]
then
  echo "\n\nRunning the docker container\n\n"
  docker run --restart=on-failure --rm --detach --publish 8080:8080 ${1} 
fi
