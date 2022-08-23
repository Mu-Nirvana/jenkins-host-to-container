from modules import parse_cli

file_templates = {}
base_template = {"templates": file_templates, "output": "stdout", "suggested": False, "TLSCert": "none"}

def complete_config(config, args):
    for key in base_template:
        if key not in config:
            config[key] = base_template[key]

    if config["templates"] == "default": config["templates"] = file_templates

    for key in file_templates:
        if key not in config["templates"]:
            config["templates"][key] = file_templates[key]

    if "--suggested" in parse_cli.get_switches(args): config["suggested"] = True
    inputs = parse_cli.get_inputs(args)
    if "--tls-cert=" in inputs: config["TLSCert"] = inputs["--tls-cert="]
    if "--out=" in inputs: config["output"] = inputs["--out="]

    config["output"] = config["output"].replace(' ','').split(',')
    
    return config

def fill_src(docker_config, call_file):
    if "scripts/installdeps" in docker_config["src"]:
        docker_config["src"][docker_config["src"].index("scripts/installdeps")] = f"{call_file[:call_file.rfind('/')]}/scripts/installdeps"
    
    return docker_config
