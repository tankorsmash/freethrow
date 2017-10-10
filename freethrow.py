#!ipython3

import json
import dateutil
from operator import itemgetter
import grequests, requests
import concurrent.futures

import matplotlib.pyplot as plt
import numpy as np

from pprint import pprint as pp

import models
import cache
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
    response = requests.get(url, params={"api_key": STEAMAPIS_APIKEY})
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

def _request_your_game_inventory(app_id):
    print('requesting your inventory for app id {}...'.format(app_id), end='')
    url = BASE_URL+"steam/inventory/{sid64}/{app_id}/{ctxt}/".format(
            sid64=STEAMID_64,
            app_id=PUBG_ID,
            ctxt=DEFAULT_CONTEXT)
    response = _do_request(url)
    print('done;')
    return response

def bind_my_items_to_market_data(items, market_data):
    for item in items:
        prices = list(filter(
            lambda md: md['market_hash_name'] == item.market_hash_name,
            market_data.data
        ))
        if prices:
            prices = prices[0]
        else:
            prices = {}

        item.fill_prices_data(prices)



def get_your_game_inventory(app_id):
    response = _request_your_game_inventory(app_id)

    assets = response.json()['assets']
    descriptions = response.json()['descriptions']

    items = []
    for asset_data in assets:
        data = match_asset_to_description(assets, descriptions, asset_data['classid'])
        item = models.ItemOwned(data)
        items.append(item)

    return items

def build_game_market_data_url(app_id):
    return BASE_URL+"market/items/{app_id}/".format(
        app_id=PUBG_ID,
    )

def _request_game_market_data(app_id):
    print('requesting static inventory for app id {}...'.format(app_id), end='')
    url = build_game_market_data_url(app_id)
    response = _do_request(url)
    print('done')
    return response

def get_game_market_data(app_id):
    """
    app details and list of all items with their prices within
    """
    response = _request_game_market_data(app_id)
    data = response.json()
    market_data = models.GameMarketData(data)
    return market_data

def build_market_data_url_for_item(app_id, market_hash_name):
    return BASE_URL+"market/item/{app_id}/{market_hash_name}".format(
        app_id=PUBG_ID,
        market_hash_name=market_hash_name,
    )

def _request_market_data_for_app_and_name(app_id, market_hash_name):
    print('market data for app id {} and item {}...'.format(app_id, market_hash_name), end='')
    url = build_market_data_url_for_item(app_id, market_hash_name)
    response = _do_request(url)
    print('done')
    return response

def get_market_data_for_app_and_name(app_id, market_hash_name):
    response = _request_market_data_for_app_and_name(app_id, market_hash_name)
    data = response.json()
    return data

def get_and_fill_market_data_for_item(item):
    if not item.marketable:
        data = {}
    else:
        data = get_market_data_for_app_and_name(item.appid, item.market_hash_name)
    item.fill_market_data(data)
    return data

def exception_handler(request, exception):
    print(exception)
    import ipdb; ipdb.set_trace(); #TODO

def old_test():
    print("starting old_test")
    pubg_market_data = get_game_market_data(PUBG_ID)
    items = get_your_game_inventory(PUBG_ID)
    bind_my_items_to_market_data(items, pubg_market_data)
    print ("found {} items".format(len(items)))

    pooled_reqs = []
    for item in items:
        if item.marketable:
            url = build_market_data_url_for_item(item.appid, item.market_hash_name)
            pooled_reqs.append(grequests.get(url, params={"api_key": STEAMAPIS_APIKEY}))

    print("start pooling {} requests...".format(len(pooled_reqs)), end=" ")
    market_data = grequests.map(pooled_reqs, exception_handler=exception_handler)
    market_data = [md.json() for md in market_data]
    print("done")

    trendlines = []
    for item in items:
        if item.marketable:
            data = list(filter(lambda d: d['market_hash_name'] == item.market_hash_name, market_data))
            if data:
                item.fill_market_data(data[0])

            median_data = item.market_data.median_avg_prices_15days
            trendlines.append((item.market_hash_name, median_data.trendlines()))

    trendlines.sort(key=lambda tl: itemgetter(3)(tl[1]))

def async_get_all_market_data_in_app(market_data):
    """
    get histogram and 15 day history for the items within an app's item list
    """
    urls = []
    for imd in market_data.data:
        url = build_market_data_url_for_item(market_data.appid, imd['market_hash_name'])
        urls.append(url)

    print("start pooling {} requests...".format(len(urls)), end=" ")
    response_data = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        future_to_url = {executor.submit(lambda u: requests.get(u, params={"api_key": STEAMAPIS_APIKEY}), url) : url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            resp = future.result()
            response_data.append(resp)

    response_data = [md.json() for md in response_data]
    print("done")

    item_mds = []
    for imd in market_data.data:
        try:
            data = list(filter(
                lambda d: d['market_hash_name'] == imd['market_hash_name'],
                response_data
            ))
        except Exception as e:
            print(e)
            import ipdb; ipdb.set_trace(); #TODO

        if data:
            data = data[0]
            item_market_data = models.ItemMarketData(data)
            item_mds.append(item_market_data)

    return item_mds

def testing():
    pubg_market_data = cache.get_game_market_data_from_cache(PUBG_ID)
    if pubg_market_data is None:
        print("expired or invalid market data, getting new")
        pubg_market_data = get_game_market_data(PUBG_ID)
    #
    # item_mds = async_get_all_market_data_in_app(pubg_market_data)
    # pubg_market_data.take_item_market_data(item_mds)
    #
    cache.write_game_market_data_to_cache(pubg_market_data)
    # cache.write_item_market_data_to_cache(pubg_market_data)

    # import ipdb; ipdb.set_trace(); #TODO
    print("ALL DONE")



if __name__ == "__main__":
    # old_test()
    testing()
