#!/bin/python3
import re
import yaml

SUB_PATTERN = "\$\{\w+\}"

def get_file(filename):
    with open(filename) as file:
        return file.read()

#Retrieve yaml from file
def getYaml(yamlFile):
  with open(yamlFile) as file:
    return yaml.safe_load(file)
    
def find_substrings(file, pattern):
    return re.findall(pattern, file)

def replace_substrings(file, substrings):
    for substring in substrings:
       file.replace(resolve_key(substring)) 
    return file

def resolve_key(key, key_values):
    if '.' in key:
        return resolve_key(key_values[key.strip("${}")


