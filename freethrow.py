#!ipython3

import json
import requests

with open("private_config.json") as f:
    PRIVATE_CONFIG = json.load(f)
with open("public_config.json") as f:
    PUBLIC_CONFIG = json.load(f)
