from fabric.api import local, task
import os

from .settings import (
    SUBNET_ID, VPC_ID, AMI_ID, SECURITY_GROUP, REGION,
    INSTANCE_TYPE, ROOT_SIZE
)

@task
def create_instance(instance_name):
    '''
    Creates an aws ec2 instance running docker machine.
    
    The ec2 instance will host the notebook server. 
    That enables anyone to connect to the notebook server. 
    Only the machine with the instance keypair (generated when 
    creating the instance) can run docker commands against it.
    
    Files can be synced with the instance by running the 
    `sync_files_to_instance` fab command. Notebooks can be
    created on the server via the web GUI, or by sshing in.
    '''
    
    try:
        local("rsync --version")
    except:
        print("Install rsync")
        return
    try:
        local("aws --version")
    except:
        print("Install aws cli")
        return
    try:
        local("docker-machine --version")
    except:
        print("Install docker-machine")
        return

    def docker_machine_command(command):
        local("docker-machine ssh {} {}".format(instance_name, command))

    local_path = os.getcwd()
    local(
        "docker-machine create "
        "--driver amazonec2 "
        "--amazonec2-subnet-id {SUBNET_ID} "
        "--amazonec2-vpc-id {VPC_ID} "
        "--amazonec2-ami {AMI_ID} "
        "--amazonec2-security-group {SECURITY_GROUP} "
        "--amazonec2-region {REGION} "
        "--amazonec2-instance-type {INSTANCE_TYPE} "
        "--amazonec2-root-size {ROOT_SIZE} "
        "{}".format(instance_name)
    )

    docker_machine_command("sudo mkdir -p {}".format(local_path))
    docker_machine_command("sudo chown -R ubuntu {}".format(local_path))
    local(
        "rsync -rvz --rsh='docker-machine ssh {}' --exclude='.git/' --progress {}/ :{}/".format(
            instance_name, local_path, local_path
        )
    )

    instance_env = "eval $(docker-machine env {})".format(instance_name)

    local(instance_env + " && docker-compose build")
    local(instance_env + " && docker-compose up -d")
    local("docker-machine ls")


@task
def sync_files_to_instance(instance_name):
    local_path = os.getcwd()
    local(
        "rsync -rvz --delete --rsh='docker-machine ssh {}' --exclude='.git/' --progress . :{}/".format(
            instance_name, local_path
        )
    )
    local("docker-machine ssh {} sudo chown -R ubuntu {}".format(
        instance_name, local_path
    ))
