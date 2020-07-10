import pymysql
import urllib3
import boto3

bucket = open('../bucket', 'r').read()
http = urllib3.PoolManager()
region = http.request('GET', '169.254.169.254/latest/meta-data/placement//availability-zone').data.decode()[:-1]

db =  pymysql.connect('localhost', 'selfies_admin', 'Strongpass1', 'johnselfie')
cursor = db.cursor()

drop_column = "ALTER TABLE selfies DROP file_data"
add_column = "ALTER TABLE selfies ADD COLUMN file_data VARCHAR(500) NOT NULL"
get_files = "SELECT id, file_name FROM selfies"

print(f"Removing current file_data column with\n{drop_column}...")
cursor.execute(drop_column)
db.commit()
print("...done")
print(f"\nAdding file_data column with\n{drop_column}...")
cursor.execute(add_column)
db.commit()
print("...done")

print(f"Adding records to table for S3 URI's for bucket {bucket}...")
cursor.execute(get_files)
files = cursor.fetchall()

for file in files:
    update = f"UPDATE selfies SET file_data = 'https://{bucket}.s3-{region}.amazonaws.com/media/{file[1]}' WHERE id = {file[0]}"
    print(f"Updating id: {file[0]} file: {file[1]} with  {update}...")
    cursor.execute(update)
    print("...done")

db.commit()
db.close()