#!ipython3

import json
import dateutil
from operator import itemgetter
import requests

import matplotlib.pyplot as plt
import numpy as np

from pprint import pprint as pp

import models
from graphing import trendline

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
    try:
        response.raise_for_status()
    except Exception as e:
        print(e)
        import ipdb; ipdb.set_trace(); #TODO
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
    if market_data is None:
        print("no market data passed in, item.prices will be empty")
        market_data = []

    items = []
    for asset_data in assets:
        data = match_asset_to_description(assets, descriptions, asset_data['classid'])
        if market_data is not None:
            prices = list(filter(
                lambda md: md['market_hash_name'] == data['market_hash_name'],
                market_data.data
            ))
            if prices:
                data['prices'] = prices[0]
            else:
                data['prices'] = {}
        # print(market_data)
        # print(data['prices'])
        item = models.Item(data)
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
    data = response.json()
    market_data = models.GameMarketData(data)
    return market_data

def request_market_data_for_app_and_name(app_id, market_hash_name):
    print('market data for app id {} and item {}...'.format(app_id, market_hash_name), end='')
    url = "market/item/{app_id}/{market_hash_name}".format(
        app_id=PUBG_ID,
        market_hash_name=market_hash_name,
    )
    print('done')
    response = _do_request(url)
    return response

def get_market_data_for_app_and_name(app_id, market_hash_name):
    response = request_market_data_for_app_and_name(app_id, market_hash_name)
    data = response.json()
    return data

def get_market_data_for_item(item):
    if not item.marketable:
        data = {}
    else:
        data = get_market_data_for_app_and_name(item.appid, item.market_hash_name)
    item.fill_market_data(data)
    return data

def old_test():
    pubg_market_data = get_game_market_data(PUBG_ID)
    items = get_your_game_inventory(PUBG_ID, market_data=pubg_market_data)
    print ("found {} items".format(len(items)))
    trendlines = []
    for item in items:
        get_market_data_for_item(item)
        prices = item.prices
        histogram = item.market_data.histogram
        median_data = item.market_data.median_avg_prices_15days
        if item.marketable:
            trendlines.append((item.market_hash_name, median_data.trendlines()))

    trendlines.sort(key=lambda tl: itemgetter(3)(tl[1]))
    pp(trendlines[0])
    pp(trendlines[-1])
    # pp(median_data.data)
    # x = list(map(dateutil.parser.parse, map(itemgetter(0), median_data)))
    # y = list(map(itemgetter(2), median_data))
    # plt.plot(x, y)
    # plt.title("ASDASDA")
    # plt.plot_date(median_data)
    # response = request_game_inventory(PUBG_ID)

def testing():
    pubg_market_data = get_game_market_data(PUBG_ID)
    raw_items = []
    for item_market_data in pubg_market_data.data:
        data = get_market_data_for_app_and_name(PUBG_ID, item_market_data['market_hash_name'])
        raw_items.append(data)

    import ipdb; ipdb.set_trace(); #TODO


if __name__ == "__main__":
    old_test()
    # testing()
