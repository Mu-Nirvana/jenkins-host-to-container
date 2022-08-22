import yaml
import tarfile
from os.path import expand_path, exists
from os import getcwd, remove

#Get a file
def get_file(filename):
    with open(expand_path(filename)) as file:
        return file.read()

#Retrieve yaml from file
def get_yaml(yamlFile):
  with open(expand_path(yamlFile)) as file:
    return yaml.safe_load(file)

#Write to a file
def write_file(filename, contents):
    with open(expand_path(filename), 'w') as file:
        return file.write(contents)

#Write to a tar file
def write_tar(tarname, contents):
    with tarfile.open(tarname, 'w') as tar:
        for file in contents:
            tar.add(file)

#Delete files
def delete_files(files):
    for file in files:
        remove()

#Checkfiles
def check_files(files):
    for file in files:
        if not exists(expand_path(file)):
            return False 
    return True

def expand_path(path):
    if "./" in path:
        path = path.replace('.', getcwd())
    
    if "../" in path:
        raise Exception("Can't use parent directory in relative path. Feature not implemented")
        #TODO Fix this garbage
    path = expanduser(path)

    if path.find('/') == -1:
        path = getcwd() + '/' + path

    return path
