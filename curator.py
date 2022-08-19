#!/usr/bin/python3
# when push it comes to shove we do not fall out of love
# we double down, we do not fade.
# - metric
import sys,yaml
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

# For each release directory...
for directory in directory_list:
    # Get list of formats
    format_list = natsorted([f.name for f in scandir(directory) if f.is_dir], alg=ns.PATH | ns.IGNORECASE)
    # # For each format:
    # for format in format_list:
    #     print(format)
