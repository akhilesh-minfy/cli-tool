import json
import subprocess
import os
def detect_app_type(path):
    package_file=os.path.join(path, "package.json")
    try:
        with open(package_file, "r", encoding="utf-8") as file:
            # this json.load is used to read json files and converts it into dictonary or list
            package_data = json.load(file)
            deps = package_data.get("dependencies", {})
            dev_deps = package_data.get("devDependencies", {})

            if "next" in deps or "next" in dev_deps:
              #  print("This is a Next.js application.")
              # if we dont pass cwd, it will run the command in the current directory
                print("Installing dependencies !!!!!!!")
                subprocess.check_call('npm install', shell=True,cwd=path)
                print("Building Your application !!!!!!!!")
                subprocess.check_call('npm run build', shell=True, cwd=path)
                return "next"
            elif "react" in deps or "react" in dev_deps:
                print("This is a React application.")
                print("Installing dependencies !!!!!!!! ")
                subprocess.check_call('npm install', shell=True, cwd=path)
                print("Building Your application !!!!!!!!")
                subprocess.check_call('npm run build', shell=True, cwd=path)
                return "react"
            else:
               # print("This is not a React or Next.js application.")
                raise ValueError()
    except FileNotFoundError:
        print("No package.json found in this directory.")
    except ValueError:
        print("Unsupported application type.")
        return None