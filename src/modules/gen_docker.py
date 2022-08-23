from modules import value_sub

#Swap in values to base Dockerfile template
def gen_docker(template, key_values):
    Dockerfile = value_sub.replace_keys(template, value_sub.find_keys(template, value_sub.SUB_PATTERN), key_values).rstrip('\n')
    if "otherFiles" in key_values:
        Dockerfile = add_files(Dockerfile, key_values["otherFiles"])
    return Dockerfile

#Add additional files to Dockerfile 
def add_files(Dockerfile, files):
    for file in files:
        if "owner" in file:
            Dockerfile += f"\nCOPY --chown={file['owner']} {file['src']} {file['dest']}"
        else:
            Dockerfile += f"\nCOPY {file['src']} {file['dest']}"         
    return Dockerfile
