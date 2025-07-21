import os
import subprocess
def create_infra(repo_name):
    
  #  Create the infrastructure using Terraform.
    # with open(os.path.join(os.getcwd(),"terraform","terraform.tfvars"), "w") as f:
    #     f.write('tags = {\n')
    #     f.write(f'  Name = "{repo_name}-instance"\n')
    #     f.write('}\n')
    try:
        subprocess.check_call('terraform destroy --auto-approve', shell=True, cwd=os.path.join(os.getcwd(), "terraform"))
        subprocess.check_call('terraform init', shell=True, cwd=os.path.join(os.getcwd(), "terraform"))
        subprocess.check_call('terraform plan', shell=True, cwd=os.path.join(os.getcwd(), "terraform"))
        subprocess.check_call('terraform apply --auto-approve', shell=True,cwd=os.path.join(os.getcwd(), "terraform"))
        print("Infrastructure created successfully.")
        public_ip = get_instance_ip_by_name("my-instance")
        return public_ip
    except subprocess.CalledProcessError as e:
        print("Error creating infrastructure:", e)




import boto3








def get_instance_ip_by_name(instance_name):
    AWS_REGION = "ap-south-1"
    ec2_client = boto3.client("ec2", region_name=AWS_REGION,
        #  aws_access_key_id="",
        #  aws_secret_access_key="",
        #  aws_session_token=""
         )
    try:
        response = ec2_client.describe_instances(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': [instance_name]
                },
                {
                    'Name': 'instance-state-name',
                    'Values': ['running']
                }
            ]
        )
        
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                public_ip = instance.get('PublicIpAddress')
                if public_ip:
                    print(f"[+] Found instance '{instance_name}' with IP: {public_ip}")
                    return public_ip
        
        print(f"[!] No running instance found with name: {instance_name}")
        return None
        
    except Exception as e:
        print(f"[!] Error getting instance IP: {e}")
        return None

# Usage example:
# public_ip = get_instance_ip_by_name("my-instance-name")


