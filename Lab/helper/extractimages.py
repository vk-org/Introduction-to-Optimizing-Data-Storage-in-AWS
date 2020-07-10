import pymysql
import base64

db =  pymysql.connect('localhost', 'selfies_admin', 'Strongpass1', 'johnselfie')
cursor = db.cursor()

get_files = "SELECT file_name, file_data FROM selfies"
cursor.execute(get_files)
files = cursor.fetchall()
db.close()

for file in files:
    with open(f"media/{file[0]}", 'wb') as file_object:
        file_object.write(base64.b64decode(file[1]))