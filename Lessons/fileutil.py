import boto3
import os
import urllib3
from werkzeug.utils import secure_filename

http = urllib3.PoolManager()
ip = http.request('GET', '169.254.169.254/latest/meta-data/public-ipv4').data.decode()

upload_folder = 'media'
allowed_extensions = {'jpg', 'jpeg', 'gif', 'png'}

# Save provided file locally
def save_local(file):
    filename = secure_filename(file.filename)
    file.save(os.path.join(upload_folder, filename))

    return

# Put provided file to specified S3 bucket
def upload_s3(file, bucket):
    key = secure_filename(file.filename)
    s3_client = boto3.client('s3')
    response = s3_client.put_object(
        Body = file.read(),
        Bucket = bucket,
        Key = f'media/{key}'
    )

    return response

# List contents of directory, return list of URI's
def list_local():
    media_files = []
    files = os.listdir(upload_folder)
    for f in files:
        if f.split('.'):
            file_uri = f'http://{ip}/{upload_folder}/{f}'
            media_files.append(file_uri)

    return media_files

# List contents of provided S3 bucket, return bucket URI's
def list_s3(bucket):
    keys = []
    s3_client = boto3.client('s3')
    response = s3_client.list_objects_v2(
        Bucket = bucket,
        Prefix = "media"
    )
    if 'Contents' in response.keys():
        for k in response['Contents']:
            keys.append(f"https://{bucket}.s3-us-west-2.amazonaws.com/{k['Key']}")

    return keys

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
