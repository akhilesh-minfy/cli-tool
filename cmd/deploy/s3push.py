import boto3 
import os

def s3_store(app_path, app_type,repo_name):
    client = boto3.client('s3',
        #  aws_access_key_id="",
        #  aws_secret_access_key="",
        #  aws_session_token=""
        )
        
    upload_file_bucket = 'cli-tool-s3-123'
    if app_type == "next":
        upload_dir = os.path.join(app_path, ".next")
        s3_prefix = f'{repo_name}/next/'
    else:
       # upload_dir = os.path.join(app_path, "dist")
       if os.path.exists(os.path.join(app_path, "dist")):
              upload_dir = os.path.join(app_path, "dist")
       else:
           upload_dir = os.path.join(app_path, "build")
       s3_prefix = f'{repo_name}/react/'
    # Walk through the directory and upload each file
    for root, dirs, files in os.walk(upload_dir):
        for file in files:
            file_path = os.path.join(root, file)
            # S3 key should be relative to the build directory
            rel_path = os.path.relpath(file_path, upload_dir)
            s3_key = os.path.join(s3_prefix, rel_path).replace("\\", "/")
            client.upload_file(file_path, upload_file_bucket, s3_key)
 
