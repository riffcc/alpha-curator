#!/usr/bin/python3
# Grab data from the Riff.CC MySQL service and render it to the Curator's PostgreSQL database

# Credits:
#  - https://stackoverflow.com/questions/10195139/how-to-retrieve-sql-result-column-value-using-column-name-in-python
#  - https://github.com/PyMySQL/PyMySQL

# Import needed modules
from __future__ import with_statement
from grizzled.os import working_directory
from urllib.parse import urlparse
import os, sys, yaml, re
import importlib
import pymysql.cursors
import psycopg2

# Set our API key
from pathlib import Path
apiname = os.path.expanduser('~/.rcc-api')
apitoken = Path(apiname).read_text()

# Dynamically load in our magic config files
configname = os.path.expanduser('~/.rcc-tools.yml')
config = yaml.safe_load(open(configname))

# Check if the config is empty
if config is None:
    print("Failed to load configuration.")
    sys.exit(1338)

# Get our Riff.CC credentials and load them in
rccuser = config["rccuser"]
rccpass = config["rccpass"]
sqlpassword = config["password"]
curator_user = config["curator_user"]
curator_pass = config["curator_pass"]
curator_host = config["curator_host"]

# Connect to the Unit3D database
connection = pymysql.connect(host='localhost',
                             user='unit3d',
                             password=sqlpassword,
                             database='unit3d',
                             cursorclass=pymysql.cursors.DictCursor)

# Connect to the Curator database
connpg = psycopg2.connect(host=curator_host,
                          database="collection",
                          user=curator_user,
                          password=curator_pass)

# create a cursor
cursorpg = connpg.cursor()

# execute a statement
print('PostgreSQL database version:')
cursorpg.execute('')
cursorpg.execute('SELECT * FROM releases')

with connection:
    with connection.cursor() as cursor:
        # Read everything from Unit3D (traditional site)
        sql = "SELECT * FROM `torrents` WHERE id=1"
        cursor.execute(sql)
        result_set = cursor.fetchall()
        for row in result_set:
            print("hello")
            id = row["id"]
            name = row["name"]
            slug = row["slug"]
            description = row["description"]
            mediainfo = row["mediainfo"]
            category_id = row["category_id"]
            user_id = row["user_id"]
            featured = row["featured"]
            created_at = row["created_at"]
            updated_at = row["updated_at"]
            type_id = row["type_id"]
            ipfs_hash = row["stream_id"]
            print("Processing id "+ str(id))
            print("Name:" + name + " user_id: " + str(user_id))
        # Dump it into The Curator (new prototype)
