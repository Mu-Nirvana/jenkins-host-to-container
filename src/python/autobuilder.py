#!/bin/python3
import yaml
import subprocess
import sys
from os.path import exists, expanduser

#Retrieve yaml from file
def getYaml(yamlFile):
  with open(yamlFile) as file:
    return yaml.safe_load(file)

#Check if passed files exist
def checkfiles(*files):
  fileExists = [exists(expanduser(file)) for file in files]
  return all(fileExists), [file for x,file in enumerate(files) if fileExists[x] == False]
  
def main():
  #Get yaml config
  config = getYaml(str(sys.argv[1]))["Containerize"]

  #Dockerfile template file
  dockerTemplate = "Dockerfile_Template"

  #Separate out config sections
  source = config["src"]
  container = config["container"]
  build = config["build"]
  testrun = config["test_run"]

  #Check files
  filecheck = checkfiles(dockerTemplate, container["jenkins_home_src"], container["dependencies"], *[file["src"] for file in container["other_files"]])
  if not filecheck[0]: raise Exception(f"Missing files: {str(filecheck[1])}")
  

  
if __name__ == "__main__":
  main()
