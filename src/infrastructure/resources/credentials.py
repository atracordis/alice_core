import json
from .paths import *
import os

# read credentials (hashed)
with open(path_creds) as json_file:
    credentials = json.load(json_file)

if "SECRET" not in os.environ.keys():
    # read secret (for hashing)
    with open(path_secret, 'r') as file:
        SECRET_KEY = file.read()
else:
    SECRET_KEY=str(os.environ["SECRET"])