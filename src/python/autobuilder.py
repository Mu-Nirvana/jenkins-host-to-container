#!/bin/python3
import yaml
import subprocess
import sys
from os.path import exists

def getYaml(yamlFile):
  with open(yamlFile) as file:
    return yaml.safe_load(file)

def checkfiles(*files):
  fileExists = [exists(file) for file in files]
  return all(fileExists), [file for x,file in enumerate(files) if fileExists[x] == False]
  
def main():
  config = getYaml(str(sys.argv[1]))
  dockerTemplate = "Dockerfile_Template"
  filecheck = checkfiles(dockerTemplate)
  if not filecheck[0]: raise Exception(f"Missing files: {str(*filecheck[1])}")
  print(config)
  #NOTE: do NOT allow --detach as a run option during test phase
  
if __name__ == "__main__":
  main()
