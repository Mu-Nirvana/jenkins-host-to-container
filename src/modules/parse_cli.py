SWITCHES = ["--no-build", "--no-run", "--help", "--suggested"] 
INPUTS = ["--out=", "--tls-cert="]

default_file = ""

#Get input file from cli args
def get_input_file(args):
    for arg in args[1:]:
        if arg not in SWITCHES and len([x for x in INPUTS if x not in arg]) == 0:
            return arg
    return default_file

#Get switches set in cli args
def get_switches(args):
    return [arg for arg in args if arg in SWITCHES]

#Get inputs provided in cli args
def get_inputs(args):
    inputs = {}
    for arg in args:
        for option in INPUTS:
            if arg.find(option) != -1:
                inputs[option] = arg.replace(option, '')

    return inputs
