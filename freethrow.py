#!ipython3

import json
import requests

with open("private_config.json") as f:
    PRIVATE_CONFIG = json.load(f)
    STEAMAPIS_APIKEY = KEY = PRIVATE_CONFIG['steamapis_apikey']
    STEAMID_64 = PRIVATE_CONFIG['steamid_64']
with open("public_config.json") as f:
    PUBLIC_CONFIG = json.load(f)
    PUBG_ID = PUBLIC_CONFIG['app_ids']['pubg']

BASE_URL = "https://api.steamapis.com/"
DEFAULT_CONTEXT = 2

def _do_request(url):
    response = requests.get(BASE_URL+url, params={"api_key": STEAMAPIS_APIKEY})
    response.raise_for_status()
    return response

def get_your_game_inventory(app_id):
    print('getting your inventory for app id {}...'.format(app_id), end='')
    url = "steam/inventory/{sid64}/{app_id}/{ctxt}/".format(
            sid64=STEAMID_64,
            app_id=PUBG_ID,
            ctxt=DEFAULT_CONTEXT)
    response = _do_request(url)
    print('done;')
    return response

def get_game_inventory(app_id):
    print('getting static inventory for app id {}...'.format(app_id), end='')
    url = "market/items/{app_id}/".format(
        app_id=PUBG_ID,
    )
    print('done')
    response = _do_request(url)
    return response


response = get_your_game_inventory(PUBG_ID)
response = get_game_inventory(PUBG_ID)
