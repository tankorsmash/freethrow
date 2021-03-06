import os
import json
import time
import pathlib

import models

MINUTES_1 = 60
MINUTES_5 = MINUTES_1 * 5
MINUTES_15 = MINUTES_1 * 15
MINUTES_30 = MINUTES_1 * 30

HOURS_1 = MINUTES_1 * 60
HOURS_6 = HOURS_1 * 6
HOURS_12 = HOURS_1 * 12

DAYS_1 = HOURS_1 * 24
DAYS_2 = DAYS_1 * 2
DAYS_3 = DAYS_1 * 3
DAYS_7 = DAYS_1 * 7
DAYS_14 = DAYS_1 * 14
DAYS_30 = DAYS_1 * 30

CACHE_DIR = "_cache_dir"

GAME_MARKET_DATA_PATH_FORMAT = "./{root}/{{appid}}/game_market_data.json".format(
    root=CACHE_DIR,
)

ITEM_MARKET_DATA_PATH_FORMAT = "./{root}/{{appid}}/item_market_data.json".format(
    root=CACHE_DIR,
)

def get_game_market_data_from_cache(app_id):
    pathname = GAME_MARKET_DATA_PATH_FORMAT.format(
        appid=app_id,
    )
    path = pathlib.Path(pathname)
    if not path.exists():
        return None

    created_at = path.stat().st_mtime
    now = time.time()
    if (now - created_at) > HOURS_1:
        print("cache expired")
        return None

    try:
        with path.open() as f:
            data = json.load(f)
    except Exception as e:
        print("open json cache failed", e)
        import ipdb; ipdb.set_trace(); #TODO

    return models.GameMarketData(data)

def write_game_market_data_to_cache(game_market_data):
    pathname = GAME_MARKET_DATA_PATH_FORMAT.format(
        appid=game_market_data.appid,
    )
    path = pathlib.Path(pathname)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w") as f:
        to_dump = game_market_data._raw
        json.dump(to_dump, f)

def get_item_market_data_from_cache(app_id):
    pathname = ITEM_MARKET_DATA_PATH_FORMAT.format(
        appid=app_id,
    )
    path = pathlib.Path(pathname)
    if not path.exists():
        return None

    created_at = path.stat().st_mtime
    now = time.time()
    if (now - created_at) > MINUTES_5:
        print("item market data cache expired")
        return None

    try:
        with path.open() as f:
            data = json.load(f)
    except Exception as e:
        print("open json cache failed", e)
        import ipdb; ipdb.set_trace(); #TODO

    return list(map(models.ItemMarketData, data))


def write_item_market_data_to_cache(game_market_data):
    if not game_market_data._raw_item_market_data:
        print("no item market data on GameMarketData, aborting cache")
        return

    pathname = ITEM_MARKET_DATA_PATH_FORMAT.format(
        appid=game_market_data.appid,
    )
    path = pathlib.Path(pathname)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w") as f:
        to_dump = game_market_data._raw_item_market_data
        json.dump(to_dump, f)
