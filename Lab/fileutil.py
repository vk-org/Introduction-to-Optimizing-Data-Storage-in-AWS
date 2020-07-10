import json
from flask import jsonify
import boto3
import base64
import os
import urllib3
import pymysql
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


# Database functions
def get_files():
    files = []
    db = pymysql.connect('localhost', 'selfies_admin', 'Strongpass1', 'johnselfie')
    cursor = db.cursor()
    sql = 'SELECT file_name, file_data FROM selfies'
    
    try:
        cursor.execute(sql)

        selfies = cursor.fetchall()
        for selfie in selfies:
            file_data = selfie[1].decode('ascii')
            files.append({'file_name': selfie[0], 'file_data': file_data})
        result = json.dumps(files)
    
    except Exception as e:
        result = "Exception"
        print(f'Encounter Exception: {e}')
    
    db.close
    return result

def add_file(file):
    bucket = open('bucket', 'r').read()
    db =  pymysql.connect('localhost', 'selfies_admin', 'Strongpass1', 'johnselfie')
    cursor = db.cursor()

    cursor.execute('SELECT file_name FROM selfies')
    existing_files = cursor.fetchall()

    cursor.execute('show columns from selfies like "file_data"')
    file_data_info = cursor.fetchone()
    column_type = file_data_info[1]

    if column_type == 'mediumblob':
        file_to_add = {'file_name': file.filename, 'file_data': base64.b64encode(file.read())}
    else:
        file_to_add = {'file_name': file.filename, 'file_data': f"https://{bucket}.s3-us-west-2.amazonaws.com/media/{file.filename}"}

    if file_to_add['file_name'] not in existing_files:
        sql = 'INSERT INTO selfies(file_name, file_data) VALUES (%s, %s)'
        sql_data = (file_to_add["file_name"], file_to_add["file_data"])

        try:
            cursor.execute(sql, sql_data)
            db.commit()
        
        except Exception as e:
            db.rollback()
            print(f'Encounter Exception: {e}')
            return "Exception"
    else:
        return "File already exists"
    
    db.close()
    return