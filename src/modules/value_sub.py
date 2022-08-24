import re

SUB_PATTERN = "\$\{[\w.]+\}"

#Locate all the keys in a file
def find_keys(file, pattern):
    return re.findall(pattern, file)

#Replace the keys in a file with a given key value dictionary
def replace_keys(file, keys, key_values):
    for key in keys:
       file = file.replace(key, resolve_key(key.strip('${}'), key_values)) 
    return file

#resolve a key name in nested dictionaries
def resolve_key(key, key_values):
    if '.' in key:
        return resolve_key(key[key.index('.')+1:], key_values[key[:key.index('.')]])
    else: return key_values[key]
