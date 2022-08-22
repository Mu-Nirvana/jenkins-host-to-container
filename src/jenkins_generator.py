from modules import * 

def main():
    print("Beginning Jenkins Generator\n\n\n")
    operations = {"Dockerfile" : True, "K8s": True, "Build": True, "Run": True}
    modes = {"output": "file", "suggested": False, "fileIn": "config.yaml", "TLSCert": "files"}
    #TODO Add the templates and their file names
    templates = {"Dockerfile": f"{__file__}/templates/", "K8sPVC": f"{__file__}/templates/", "K8sDeployment" : f"{__file__}/templates/", "K8sNetworking": f"{__file__}/templates/", "K8sTLS": f"{__file__}/templates/"}

    Dockerfile = "No Dockerfile generated"
    K8s = "No Kubernetes manifests generated"
    TLS = "TLS Certs in files key.pem and cert.pem"


    #TODO: Add cli parsing and options

    global_config = file_ops.get_yaml(modes["fileIn"])

    #TODO generate stdout output to describe configuration


    for operation in operations:
        operations["operation"] = operation in global_config

    if operations["Dockerfile"]:
        Dockerfile = base_docker(getfil
    

if __name__ == "__main__":
    main()
