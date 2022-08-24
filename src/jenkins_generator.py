#!/bin/python3
import sys
import subprocess
from modules import * 

#Set defaults
parse_cli.default_file = "config.yaml"
config_yaml.file_templates = {"Dockerfile": f"{__file__[:__file__.rfind('/')]}/templates/Dockerfile", "K8sTLS_Secret": f"{__file__[:__file__.rfind('/')]}/templates/K8sTLSSecret.yaml", "AzureK8sPVC": f"{__file__[:__file__.rfind('/')]}/templates/azureK8sPVC.yaml", "K8sDeployment": f"{__file__[:__file__.rfind('/')]}/templates/K8sDeploy.yaml", "K8sNet": f"{__file__[:__file__.rfind('/')]}/templates/K8sNet.yaml"}

#Output macros
HEAD = '========================================\n========================================'
SEP = '****************************************'

#Format to print file contents based on the config
def file_out(config, file, name):
    if check_output_mode(config["output"], ["all", "stdout"]):
        print(f"""
{HEAD}
{name}:
{HEAD}\n
{file}\n
{SEP}\n""")
    if check_output_mode(config["output"], ["all", "files", "tar"]):
        file_ops.write_file(name, file)
        print(f"""
{HEAD}
Writing {name} to current directory
{HEAD}\n""")
        return True
    return False

#Check if any of the modes are set in the output
def check_output_mode(output, modes):
    for out_type in output:
        if out_type in modes:
            return True
    return False


#Main function decides between help program and generator
def main():
    if "--help" in parse_cli.get_switches(sys.argv): help()
    else: program(sys.argv) 

#Help program
def help():
    print(""" 
Usage: jenkins_generator.py [OPTION] [FILE]
Generate Dockerfile, Kubernetes, Build docker image, and run docker image, for jenkins.
Uses config specified in [FILE], if [FILE] is not given, the current directory will be searched for 'config.yaml'.

Options ending with '=' must have inputs appended with no quotes or spaces.
  --help                List help output
  --no-build            Overrides config and disables the build step
  --no-run              Overrides config and disables the run step
  --out=MODES           Overrides config and sets the passed output modes
                            MODES are: stdout, files, tar, all 
  --tls-cert=TYPE       Overrides config and sets tls cert type
                            TYPE are: none
""")

#Generator program
def program(args):
    #Get the config_file from cli input or use default if not set
    config_file = parse_cli.get_input_file(args)
    #Stores created files to track for deletion later
    written_files = []

    #Global configuration from yaml
    global_config = file_ops.get_yaml(config_file)

    #Program sub configuration from global. Runs through complete_config to fill in missing settings and defaults
    JenkinsGenerator = config_yaml.complete_config(global_config["JenkinsGenerator"], args)
    #File temlates loaded from config
    templates = JenkinsGenerator["templates"]
    #File src formatted for abbreviations
    global_config["Dockerfile"] = config_yaml.fill_src(global_config["Dockerfile"], __file__)
    
    #Dockerfile generation
    if "Dockerfile" in global_config:
        #Generate Dockerfile with value subs, and add to file list if output is written to a file
        if file_out(JenkinsGenerator, gen_docker.gen_docker(file_ops.get_file(templates["Dockerfile"]), global_config["Dockerfile"]), "Dockerfile"):
            written_files.append("Dockerfile")
         

    #K8s generation
    if "K8s" in global_config:
        #Get kubernetes templates from all templates
        K8sTemplates = dict([(template, templates[template]) for template in templates if "K8s" in template])
        #Exclude TLS secret for special generation
        K8sTemplates.pop("K8sTLS_Secret")        
        #Select cloud specific PVC template
        K8sTemplates[f"{global_config['K8s']['cloudProvider']}K8sPVC"] = templates[f"{global_config['K8s']['cloudProvider']}K8sPVC"]

        #Generate k8s manifest for each template, and add to file list if output is written to a file
        for template in K8sTemplates:
            if file_out(JenkinsGenerator, gen_k8s.k8s_template(file_ops.get_file(K8sTemplates[template]), global_config["K8s"]), template + ".yaml"):
                written_files.append(template + ".yaml")


    #Build step if selected
    if "Build" in global_config and "--no-build" not in parse_cli.get_switches(sys.argv):
        #Throw error if files don't exist
        if not check_output_mode(JenkinsGenerator["output"], ["all", "files"]):
            raise Exception("Build requires output files. Cannot be used with only stdout")
        #Get context files, copy them, and record them for deletion after build
        files = global_config["Dockerfile"]["src"]
        file_ops.copy_files(files)
        files = ["./" + file[file.rfind('/'):] for file in files]
        build = global_config["Build"]
        #Gen build command, run command, and regardless of build success delete local context files
        dockerBuild = f'docker build {build["buildOptions"]} -t {build["imageName"]}:{build["tag"]} .'
        try:
            subprocess.run(dockerBuild.split())
        finally:
            file_ops.delete_files(files)


    #Run step if selected
    if "Run" in global_config and "--no-run" not in parse_cli.get_switches(sys.argv):
        #Gen run command, run command, and on exit remove container
        test_run = global_config["Run"]
        dockerRun = f'docker run --name={test_run["containerName"]} {test_run["runOptions"]} --detach --publish {test_run["IP"]}:{test_run["port"]}:8080 {global_config["Build"]["imageName"]}:{global_config["Build"]["tag"]}'
        try:
            containerRun = subprocess.run(dockerRun.split())
            print(f"\n{HEAD}\nContainer Running\n{HEAD}\n\n")
            input(f"{SEP}\nPress any key to stop container\n{SEP}\n")
        finally:
            subprocess.run(['docker', 'stop', test_run["containerName"]])
            subprocess.run(['docker', 'rm', test_run["containerName"]])



    #TODO tls cert generation
    if JenkinsGenerator["TLSCert"].lower() != "none":
        raise Exception("TLS feature is not yet implemented")


    #Put together tar file and remove other files if necessary
    if check_output_mode(JenkinsGenerator["output"], ["all", "tar"]):
        file_ops.write_tar("JenkinsRepo.tar", written_files)
        if not check_output_mode(JenkinsGenerator["output"], ["all", "files"]):
            file_ops.delete_files(written_files)


    #TODO Suggested commands
    if JenkinsGenerator["suggested"]:
        raise Exception("Suggested feature is not yet implemented")

if __name__ == "__main__":
    main()
