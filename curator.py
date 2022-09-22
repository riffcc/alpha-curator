#!/usr/bin/python3
# when push it comes to shove we do not fall out of love
# we double down, we do not fade.
# - metric
from platform import release
import sys,yaml,re
import urllib.parse
import requests
import subprocess
from os import scandir,getcwd,chdir,path
from pathlib import Path
from natsort import natsorted, ns

# Set our API key
api_name = path.expanduser('~/.rcc-api')
api_token = Path(api_name).read_text()

# Dynamically load in our magic config files
config_name = path.expanduser('~/.rcc-tools.yml')
config = yaml.safe_load(open(config_name))

# Check if the config is empty
if config is None:
    print("Failed to load configuration.")
    sys.exit(1338)

# Load Director config vars
director_host = config["director_host"]
radio_folder = config["radio_folder"]
releases_per_page = config["releases_per_page"]
force_new_publication = config["force_new_publication"]

# Change to main releases directory
chdir(radio_folder + "/radio/releases")

# Get a list of all directories, sorted naturally
directory_list = natsorted([f.name for f in scandir(getcwd()) if f.is_dir], alg=ns.PATH | ns.IGNORECASE)
# Get a list of all files, sorted naturally
files_list = natsorted([f.name for f in scandir(getcwd()) if f.is_file], alg=ns.PATH | ns.IGNORECASE)

number_of_releases = len(directory_list)
release_num = 1

# For each release directory...
for release_name in directory_list:
    print("Processing release " + str(release_num) + "/" + str(number_of_releases) + ": " + release_name)
    # Get the format by checking the end of the string for []
    pattern = re.compile(r"\[(.*?)\]$", re.IGNORECASE)
    try:
        release_format = pattern.search(release_name).group(1)
        print(release_format)
    except:
        print("Couldn't find release_format for " + release_name)
        release_format = "UNKNOWN"
    # Search the site for that release
    # Get the URL-encoded version of the release name
    release_urlname = urllib.parse.quote(release_name)
    # Try to search the site for that release name
    r = requests.get(director_host + "api/torrents/filter?name=" + release_urlname + "&api_token=" + api_token)
    release = r.json()
    # Check the results we got back
    if release["meta"]["total"] == 0:
        print("NO RELEASE FOUND")
    elif release["meta"]["total"] == 1:
        print("RELEASE FOUND")
    else:
        print("SOMETHING WEIRD HAPPENED")
    # If the release does not exist, let's upload it
    # We need to generate a torrent first.
    if (release_name + ".torrent") in files_list:
        print("TRUE")
    #subprocess.run('mktorrent')
    # If the release exists, check if its hash matches and then ask if you want to replace the download if it doesn't.

    # Increment release_num
    release_num += 1
