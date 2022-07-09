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

def copyFiles(destination, *files):
  for file in files:
    subprocess.run(['cp', expanduser(file), destination])
  

#Generate a dockerfile
def generateDockerfile(containerConfig, dockertemplate):
  dockerFileList = []
  Dockerfile = ""

  with open(dockertemplate) as file:
    dockerFileList = file.readlines()
  
  for line in dockerFileList:
    prefix, args, text = parseDockerLine(line)
    if prefix != '': 
      if '!' in prefix and args[0] not in containerConfig: continue
      if '@' in prefix:
        for group in containerConfig[args[0]]:
          newArgs = conditionArgs(args[1:], group) 
          Dockerfile += text.format(*newArgs)
      else:
        pass

    else:
      newArgs = conditionArgs(args, containerConfig)
      Dockerfile +=  text.format(*newArgs)

  return Dockerfile 

def parseDockerLine(line):
  prefixs = "!@"
  prefix = ""
  args = line.split(" | ")[0].split()

  if len(args) != 0: 
    if any((char in args[0] for char in list(prefixs))):
      prefix = args.pop(0)

  dockerLine = line.split(" | ")[1]
  return prefix, args, dockerLine 

def stripPath(path):
  return path.split("/")[-1]

def conditionArgs(args, keyDict):
  options = {"-strip": stripPath}

  newArgs = []
  for arg in args:
    if arg in keyDict:
      newArgs.append(keyDict[arg])
    else: newArgs.append(arg)

  for x,arg in enumerate(newArgs):
    if arg not in options: continue 
    newArgs[x+1] = options[arg](newArgs[x+1])

  return [arg for arg in newArgs if arg not in options]
  
def main():
  #Get yaml config
  config = getYaml(str(sys.argv[1]))["Containerize"]
  dockerTemplate = str(sys.argv[2]) 

  #Separate out config sections
  container = config["container"]
  build = config["build"]
  testrun = config["test_run"]

  if container["other_files"] is None: filesToCopy = [container["jenkins_home_src"], container["install_deps_src"], container["dependencies"]]
  else: filesToCopy = [container["jenkins_home_src"], container["install_deps_src"], container["dependencies"], *[file["src"] for file in container["other_files"]]]

  #Check files
  filecheck = checkfiles(dockerTemplate, *filesToCopy)
  if not filecheck[0]: raise Exception(f"Missing files: {str(filecheck[1])}")

  copydir = "copydir"
  subprocess.run(["mkdir", "copydir"])
  copyFiles(f"./{copydir}", *filesToCopy)
  
  with open("Dockerfile", "x") as file:
    file.write(generateDockerfile(container, dockerTemplate))

  dockerBuild = f'docker build {build["build_options"]} -t {build["image_name"]}:{build["tag"]} .'
  subprocess.run(dockerBuild.split())
  
  dockerRun = f'docker run --name={testrun["container_name"]} {testrun["run_options"]} --detach --publish {testrun["IP"]}:{testrun["port"]}:8080 {build["image_name"]}:{build["tag"]}'
  containerRun = subprocess.run(dockerRun.split())

  print('\n\n***************************************************\n    Test Container Running    \n***************************************************\n\n')
  input("Press any key to shutdown test container and remove temporary files")
  subprocess.run(['rm', '-rf', copydir, 'Dockerfile'])
  subprocess.run(['docker', 'stop', testrun["container_name"]])
  subprocess.run(['docker', 'rm', testrun["container_name"]])

  
if __name__ == "__main__":
  main()
