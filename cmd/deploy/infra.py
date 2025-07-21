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
         aws_access_key_id="ASIA4FBIXHBFJKIZZFAC",
         aws_secret_access_key="zCCcUwDrUaikY/qZM2KBXzW5G79annfWStRE0PLI",
         aws_session_token="IQoJb3JpZ2luX2VjEL7//////////wEaCXVzLWVhc3QtMSJGMEQCIBr6GmsMkU00oprOtAvyfQFnHPfzLoDbljG3VDRaDlrpAiA8joD3DfpgHPfUuoq0FZjnOvMonEmasUve5WZHPwuJAyqdAwjW//////////8BEAAaDDgzNTQ1NjU0Njg5MCIM4HhXmrF3H+38X0TwKvEC4MlGWYSgs3y75Pao/mtgCAAb1Y9L1+wf7PjPCl/lpDzxiCE1oIHFe0nZHL/ldMnn4JrsNh3gK1adZ/d/ngmnBxCvEdBLRdqngH5hgjGFYcq3xruYtlY0P2g/EmJE0BhL6fHm0tV//YAfmMydg1PExScAv3y/ni4YfPh+CZync4YsrWgc/3LAaCSKC9Rq+cinhCIvUyUBJbS2K8aSMma8uvVw46KWyDTyyVCgMR52xc1sXa7esAq+TVBp2OkOxfi86aMzpB2Q91Qm2Xqtg3PhR7QcS3t7wn63166uHeqz1KY4ZHvEoEfM6ct/7lz70jHAqdzTz139M0Xuk36vJISn4ESVpoL18slInePiZNPfDLvVD9nqp3tSx/rMRNLLd77dv6/SlhHsoed2lP19W8mXtCuyjYLRfk994e7D788sw5j/IsYKUX+kxpeMEAqNRHgXRXkhOW+4hLB7N84SQAHNWG8iWvxvHnBJpnEoXe/6HuWAMM/6+MMGOqcB94OzMKAXexQIlhEjARkhvEnvECjTawm9svJNyWtx0D5VGaRFqFgXJCHTUKnwFvPy4iQtm+ABXGewCSzz3xtLNOVvLWSwc+N9F2oOv2ACMM1xxfN/Xs/ZWkFwn9uTmnB4PnMH7VC2SPhWubX1j5VoRrG/8IMJ+CilIrWHfwTeSB80z10ZWl9YHlyIPC1pbmaHLk0ved8RnTocP7feZTKnEAgn+1tgY50=")
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


