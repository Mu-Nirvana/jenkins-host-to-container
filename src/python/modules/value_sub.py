#!/bin/python3
import re
import yaml

SUB_PATTERN = "\$\{[\w.]+\}"

def get_file(filename):
    with open(filename) as file:
        return file.read()

#Retrieve yaml from file
def getYaml(yamlFile):
  with open(yamlFile) as file:
    return yaml.safe_load(file)
    
#
def find_keys(file, pattern):
    return re.findall(pattern, file)

def replace_keys(file, keys, key_values):
    for key in keys:
       file = file.replace(key, resolve_key(key.strip('${}'), key_values)) 
    return file

def resolve_key(key, key_values):
    if '.' in key:
        return resolve_key(key[key.index('.')+1:], key_values[key[:key.index('.')]])
    else: return key_values[key]
