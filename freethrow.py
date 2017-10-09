#!ipython3

import json
import requests

from pprint import pprint as pp

from models import Item

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

def match_asset_to_description(assets, descriptions, cid):
    asset = list(filter(lambda a: a['classid']==cid, assets))[0]
    description = list(filter(lambda a: a['classid']==cid, descriptions))[0]

    result = {}
    result.update(**asset)
    result.update(**description)
    return result

def request_your_game_inventory(app_id):
    print('requesting your inventory for app id {}...'.format(app_id), end='')
    url = "steam/inventory/{sid64}/{app_id}/{ctxt}/".format(
            sid64=STEAMID_64,
            app_id=PUBG_ID,
            ctxt=DEFAULT_CONTEXT)
    response = _do_request(url)
    print('done;')
    return response

def get_your_game_inventory(app_id, market_data=None):
    response = request_your_game_inventory(app_id)

    assets = response.json()['assets']
    descriptions = response.json()['descriptions']

    items = []
    for asset_data in assets:
        data = match_asset_to_description(assets, descriptions, asset_data['classid'])
        if market_data is not None:
            data['prices'] = list(filter(lambda md: md['nameID'] == data['classid'], market_data))
        item = Item(data)
        items.append(item)

    return items

def request_game_market_data(app_id):
    print('requesting static inventory for app id {}...'.format(app_id), end='')
    url = "market/items/{app_id}/".format(
        app_id=PUBG_ID,
    )
    print('done')
    response = _do_request(url)
    return response

def get_game_market_data(app_id):
    response = request_game_market_data(app_id)
    return response.json()['data']


pubg_market_data = get_game_market_data(PUBG_ID)
items = get_your_game_inventory(PUBG_ID, market_data=pubg_market_data)
print ("found {} items".format(len(items)))
# response = request_game_inventory(PUBG_ID)
