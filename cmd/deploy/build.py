import shutil 
import os
import subprocess
from datetime import datetime
def copy_file(dst):
    if os.path.exists(os.path.join(dst,"dist")):
        shutil.copy(os.path.join(os.getcwd(),"Docker","Dockerfile-react"),dst)
    else:
        shutil.copy(os.path.join(os.getcwd(),"Docker","Dockerfile-vite"),dst)
def run_docker_build():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_name= f'minfyakhilesh/clone-repo:{timestamp}'
    try:
        if os.path.exists("dist"):
            subprocess.check_call(f'docker build -t {image_name} . -f Dockerfile-react', shell=True)
        else:
            subprocess.check_call(f'docker build -t {image_name} . -f Dockerfile-vite', shell=True)
        print("Docker image built successfully.")
        return image_name
    except subprocess.CalledProcessError as e:
        print("Error building Docker image:", e)
    return None
def push_image(image_name):
     #subprocess.check_call(f'docker tag {image_name} minfyakhilesh/clone-repo', shell=True)
    try:
        subprocess.check_call(f'docker push {image_name}', shell=True)
        print("Docker image pushed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print("Error pushing Docker image:", e)
        return None
