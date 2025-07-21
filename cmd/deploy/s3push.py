import boto3 
import os

def s3_store(app_path, app_type,repo_name):
    client = boto3.client('s3',
         aws_access_key_id="ASIA4FBIXHBFJKIZZFAC",
         aws_secret_access_key="zCCcUwDrUaikY/qZM2KBXzW5G79annfWStRE0PLI",
         aws_session_token="IQoJb3JpZ2luX2VjEL7//////////wEaCXVzLWVhc3QtMSJGMEQCIBr6GmsMkU00oprOtAvyfQFnHPfzLoDbljG3VDRaDlrpAiA8joD3DfpgHPfUuoq0FZjnOvMonEmasUve5WZHPwuJAyqdAwjW//////////8BEAAaDDgzNTQ1NjU0Njg5MCIM4HhXmrF3H+38X0TwKvEC4MlGWYSgs3y75Pao/mtgCAAb1Y9L1+wf7PjPCl/lpDzxiCE1oIHFe0nZHL/ldMnn4JrsNh3gK1adZ/d/ngmnBxCvEdBLRdqngH5hgjGFYcq3xruYtlY0P2g/EmJE0BhL6fHm0tV//YAfmMydg1PExScAv3y/ni4YfPh+CZync4YsrWgc/3LAaCSKC9Rq+cinhCIvUyUBJbS2K8aSMma8uvVw46KWyDTyyVCgMR52xc1sXa7esAq+TVBp2OkOxfi86aMzpB2Q91Qm2Xqtg3PhR7QcS3t7wn63166uHeqz1KY4ZHvEoEfM6ct/7lz70jHAqdzTz139M0Xuk36vJISn4ESVpoL18slInePiZNPfDLvVD9nqp3tSx/rMRNLLd77dv6/SlhHsoed2lP19W8mXtCuyjYLRfk994e7D788sw5j/IsYKUX+kxpeMEAqNRHgXRXkhOW+4hLB7N84SQAHNWG8iWvxvHnBJpnEoXe/6HuWAMM/6+MMGOqcB94OzMKAXexQIlhEjARkhvEnvECjTawm9svJNyWtx0D5VGaRFqFgXJCHTUKnwFvPy4iQtm+ABXGewCSzz3xtLNOVvLWSwc+N9F2oOv2ACMM1xxfN/Xs/ZWkFwn9uTmnB4PnMH7VC2SPhWubX1j5VoRrG/8IMJ+CilIrWHfwTeSB80z10ZWl9YHlyIPC1pbmaHLk0ved8RnTocP7feZTKnEAgn+1tgY50=")
        
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
 
