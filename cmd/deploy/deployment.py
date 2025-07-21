import requests

# ----------- Configuration ------------
def trigger_workflow(image,public_ip,workflow_file_name):
   # GITHUB_TOKEN = ""  # Replace with your personal access token
    REPO_OWNER = "akhilesh-minfy"
    REPO_NAME = "cli-tool"
    WORKFLOW_FILE_NAME = workflow_file_name  # or .github/workflows/main.yml
    BRANCH = "main"  # or your target branch
    INPUTS = {
        "user_name": "my-name",
        "image_name": image,
        "HOST": public_ip
        }
# --------------------------------------

    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/workflows/{WORKFLOW_FILE_NAME}/dispatches"

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}"   
    }

    payload = {
        "ref": BRANCH,
        "inputs": INPUTS
        }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 204:
        print("$ Workflow triggered successfully!")
    else:
        print(f" XX Failed to trigger workflow: {response.status_code}\n{response.text}")

