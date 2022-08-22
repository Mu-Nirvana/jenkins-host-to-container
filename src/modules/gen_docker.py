from modules import value_sub

#Swap in values to base Dockerfile template
def base_docker(template, key_values):
    return value_sub.replace_keys(template, value_sub.find_keys(template, value_sub.SUB_PATTERN), key_values)

#Add additional files to container
def add_files(Dockerfile, files):
    for file in files:
        if "owner" in file:
            Dockerfile += f"\nCOPY --chown={file['owner']} {file['src']} {file['dest']}"
        else:
            Dockerfile += f"\nCOPY {file['src']} {file['dest']}"         
    return Dockerfile
