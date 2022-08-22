from modules import * 

HEAD = '========================================\n========================================'
SEP = '****************************************'

def main():
    print("Beginning Jenkins Generator")
    operations = {"Dockerfile" : True, "K8s": True, "Build": True, "Run": True}
    modes = {"output": "stdout", "suggested": False, "fileIn": "config.yaml", "TLSCert": "none"}
    #TODO Add the templates and their file names
    docker_template = f"{__file__[:__file__.rfind('/')]}/templates/Dockerfile"
    k8s_templates = {"K8sPVC": f"{__file__[:__file__.rfind('/')]}/templates/K8sPVC.yaml", "K8sDeployment" : f"{__file__[:__file__.rfind('/')]}/templates/K8sDeploy.yaml", "K8sNetworking": f"{__file__[:__file__.rfind('/')]}/templates/K8sNet.yaml"}
    k8s_TLS = f"{__file__[:__file__.rfind('/')]}/templates/"

    Dockerfile = "No Dockerfile generated"
    K8s = "No Kubernetes manifests generated"
    TLS = "No TLS certs generated"


    #TODO: Add cli parsing and options

    global_config = file_ops.get_yaml(modes["fileIn"])

    #TODO update program config to match input file
    #TODO generate stdout output to describe configuration

    for operation in operations:
        operations[operation] = operation in global_config

    if operations["Dockerfile"]:
        Dockerfile = gen_docker.base_docker(file_ops.get_file(docker_template), global_config["Dockerfile"])
        if "otherFiles" in global_config["Dockerfile"]:
            Dockerfile = gen_docker.add_files(Dockerfile, global_config["Dockerfile"]["otherFiles"])

        if modes["output"] in ["file", "all", "tar"]:
            file_ops.write_file("Dockerfile", Dockerfile)


    if operations["K8s"]:
        K8s = ''
        for template in k8s_templates:
            file = f"#{template.replace('K8s', '')} kubernetes manifest\n" + gen_k8s.k8s_template(file_ops.get_file(k8s_templates[template]), global_config["K8s"])
            K8s += file + f"\n\n---\n"

            if modes["output"] in ["file", "all", "tar"]: 
                file_ops.write_file(template + ".yaml", file) 

        K8s = K8s.rstrip("\n-")

    if operations["Build"]:
        #TODO Build execution
        pass

    if operations["Run"]:
        #TODO Run execution
        pass 

    #TODO tls cert generation

    #TODO tar generation

    output = f"""
{HEAD}

Output files:

{HEAD}

Dockerfile:

{Dockerfile}

{SEP}

Kubernetes Manifests:

{K8s}

{SEP}

TLS Cert:

{TLS}
"""
    if modes["output"] in ["all", "stdout"]: print(output)

    #TODO Suggested commands

if __name__ == "__main__":
    main()
