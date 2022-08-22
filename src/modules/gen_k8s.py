from moudules import value_sub

#Swap in values to a k8s template
def k8s_template(template, key_values):
    return value_sub.replace_keys(template, value_sub.find_keys(template, value_sub.SUB_PATTERN), key_values)

#TODO
#Generate a tls certifcate in a k8s manifest
def gen_tls(template, key_values):
    pass
