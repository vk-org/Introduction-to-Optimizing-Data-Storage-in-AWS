import json
import urllib3
from flask import Flask, request, redirect, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS
from fileutil import save_local, upload_s3, list_local, list_s3, allowed_file

upload_folder = 'media'

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = upload_folder

http = urllib3.PoolManager()
ip = http.request('GET', '169.254.169.254/latest/meta-data/public-ipv4').data.decode()

@app.route('/')
def root():
    return send_from_directory('web', 'index.html')

@app.route('/<filename>')
def webfiles(filename):
    return send_from_directory("web", filename)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method ==  'POST':
        if 'file' not in request.files:
            return 'No file part'

        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
# MAKE CHANGES HERE!
            #save_local(file)
            upload_s3(file, "john-selfie")
# ------------------
            return f'Received {filename}'
    return

@app.route('/listmedia')
def list_media():
# MAKE CHANGES HERE!
    #media_files = list_local()
    media_files = list_s3('john-selfie')
# ------------------
    return json.dumps(media_files)

@app.route('/media/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
