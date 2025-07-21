import os  
import git
# import requests
import tempfile
# import atexit
# import shutil
from deploy.detect_logic import *
from deploy.s3push import *
from deploy.build import *
from deploy.infra import *
from deploy.deployment import *
import time
import datetime


def main():       
   # global temp_clone_dir
    print("Welcome to vercel CLI!")
    previous_image=""
    current_image=""
    root_dir=""
    public_ip=""
    repo_name=""
    with tempfile.TemporaryDirectory() as cloned_repos:
        target_dir = os.path.join(cloned_repos)
    
    for i in range(100000000):
        pass
    
    while True:
        cmd=str(input("Hurrah!! start entering commands: ")).strip()
        match cmd:
            case "deploy-tool init":
                repo_url = input("Enter Git repo URL to clone: ").strip()
                repo_name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")
                try:
                    if os.path.exists(target_dir) and os.listdir(target_dir):
                         timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                         clone_dir = os.path.join(cloned_repos, f"repo_{timestamp}")
                         os.makedirs(clone_dir)
                         target_dir = clone_dir
                         print("cloning .......")
                         git.Repo.clone_from(repo_url, target_dir)
                         print(f" !!!! Repo cloned into '{target_dir}'")
                    else:
                        print("cloning .......")
                        git.Repo.clone_from(repo_url, target_dir)
                        print(f" !!!! Repo cloned into '{target_dir}'")
                except Exception as e:
                    print("XXX Error cloning repo:", e)
                print("do you have any root directory in your project? (yes/no):")
                ans=str(input()).strip().lower()
                if ans == "yes":
                    root_dir = str(input("Enter the root directory of your project: ")).strip()
                else:
                    root_dir = ""
            # cdfunc("cd cloned_repos/" + repo_name + "/" + root_dir)
            # instead of changing directory, we can directly pass the path to detect_app_type
                app_path = os.path.join(target_dir, root_dir)
                # print(os.listdir(app_path))
                app_type=detect_app_type(app_path)
             # print(app_type)
                if app_type is None:
                    break
                s3_store(app_path,app_type,repo_name)
            case "deploy-tool deploy":
                    if not repo_name:
                        print("You have not initialized any project yet so please initialize it first to deploy")
                        break
                    app_path = os.path.join(target_dir, root_dir)
                    copy_file(app_path)
                    main_dir = os.getcwd()
                    os.chdir(app_path)
                    new_image=run_docker_build()
                    if new_image is None:
                        print("there is something wrong with your application")
                        break
                    if current_image:
                        previous_image = current_image
                    current_image = new_image
                    status=push_image(current_image)
                    if status is None:
                        break
                    os.chdir(main_dir)
                    print(previous_image)
                    public_ip=create_infra(repo_name)
                    print("waiting for infrastructure to be created ......")
                    time.sleep(10)
                    print("Infrastructure created successfully.")
                    trigger_workflow(current_image,public_ip,"deploy-monitor.yml")
                    print("waiting your application is being deployed ......")
                    time.sleep(120)
                    print("your app is deployed at: http://" + public_ip +":80")


            case "deploy-tool roll-back":
                    if not previous_image:
                        print("You cannot roll back as you havent deployed any application previously")
                        break
                    else:
                        # public_ip=create_infra(repo_name)
                        trigger_workflow(previous_image,public_ip,"roll-back-monitor.yml")
                        print("waiting for rollback to complete ......")
                        time.sleep(50)
                        print("your app is rolled back at: http://" + public_ip +":80")
                        current_image,previous_image=previous_image,current_image
            case "monitor-status":
                    if not public_ip:
                        print("You have not deployed any application yet so monitoring is not available")
                        break
                    print("setting up monitoring system ......")
                    time.sleep(10)
                    print("your app can be monitored at: http://" + public_ip +":9090")
                    print("your app can be monitored at: http://" + public_ip + ":3000")
                    print("for logging in to grafana, username is admin and password is admin")
            case "--help":
                    print("deploy-tool init: initialize the project")
                    print("deploy-tool deploy: deploy the project")
                    print("deploy-tool roll-back: roll back the project")
                    print("monitor-status: monitor the status of the project")
            case _:
                    print("Invalid command")
                    print("type --help for help")
        

        
        
if __name__ == "__main__":
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print("\nExiting...")
            # cleanup_temp_dir()
            break
        except Exception as e:
            print(f"An error occurred: {e}")



    