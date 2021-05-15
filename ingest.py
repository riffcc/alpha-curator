#!/usr/bin/python3
# Grab data from the Riff.CC MySQL service and render it to the Curator's PostgreSQL database

# Credits:
#  - https://stackoverflow.com/questions/10195139/how-to-retrieve-sql-result-column-value-using-column-name-in-python
#  - https://github.com/PyMySQL/PyMySQL
#  - https://stackoverflow.com/questions/37926717/psycopg2-unable-to-insert-into-specific-columns

# Import needed modules
from __future__ import with_statement
import os
import sys
import yaml
import pymysql.cursors
import psycopg2

# Dynamically load in our magic config files
configname = os.path.expanduser('~/.rcc-tools.yml')
config = yaml.safe_load(open(configname))

# Check if the config is empty
if config is None:
    print("Failed to load configuration.")
    sys.exit(1338)

# Get our Riff.CC credentials and load them in
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

with connection:
    with connection.cursor() as cursor:
        # Read everything from Unit3D (traditional site), filtering for only valid torrents
        sql = "SELECT * FROM `torrents` WHERE status=1"
        cursor.execute(sql)
        result_set = cursor.fetchall()
        for row in result_set:
            # For every existing release, gather relevant metadata and massage it into Curator.
            release_id = row["id"]
            name = row["name"]
            slug = row["slug"]
            description = row["description"]
            mediainfo = row["mediainfo"]
            category_id = row["category_id"]
            uploader_id = row["user_id"]
            featured = bool(row["featured"])
            created_at = row["created_at"]
            updated_at = row["updated_at"]
            type_id = row["type_id"]
            ipfs_hash = "none"
            if row["stream_id"] is not None:
                ipfs_hash = row["stream_id"]
            resolution_id = row["resolution_id"]
            print("Processing release id: " + str(release_id) + " (name: " + str(name) + ")")
            # do this the right way - https://www.psycopg.org/docs/usage.html?highlight=escape#the-problem-with-the-query-parameters
            SQL = '''INSERT INTO releases
                  (id, name, category_id, type_id, resolution_id, uploader_id, featured, created_at, updated_at, description, mediainfo, slug, ipfs_hash)
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                  ON CONFLICT (id) DO UPDATE SET
                  (id, name, category_id, type_id, resolution_id, uploader_id, featured, created_at, updated_at, description, mediainfo, slug, ipfs_hash)
                  = (EXCLUDED.id, EXCLUDED.name, EXCLUDED.category_id, EXCLUDED.type_id, EXCLUDED.resolution_id, EXCLUDED.uploader_id, EXCLUDED.featured, EXCLUDED.created_at, EXCLUDED.updated_at, EXCLUDED.description, EXCLUDED.mediainfo, EXCLUDED.slug, EXCLUDED.ipfs_hash);'''
            data = (release_id, name, category_id, type_id, resolution_id, uploader_id, featured, created_at, updated_at, description, mediainfo, slug, ipfs_hash)
            cursorpg.execute(SQL, data)
            # We could move this outside the loop and simply commit everything in one go.
            # Write the data to the Curator.
            connpg.commit()
