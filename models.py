import dateutil
from operator import itemgetter, attrgetter

import graphing


def convert_median_data(row):
    return [dateutil.parser.parse(row[0]), round(row[1], 3), row[2]]

class MedianAvgPrices15(object):
    def __init__(self, market_hash_name, data):
        self.market_hash_name = market_hash_name

        self.data = list(map(convert_median_data, data))

        self._raw = data

    def __str__(self):
        return "MedianAvgPrices15 for {}".format(self.market_hash_name)

    def __repr__(self):
        return "<{}>".format(str(self))

    def trendline(self, days=15):
        return graphing.trendline(self, days)

    def trendlines(self):
        return {
            3: self.trendline(3),
            5: self.trendline(5),
            10: self.trendline(10),
            15: self.trendline(15),
        }



class ItemMarketData(object):
    def __init__(self, data):
        self.market_hash_name = data.get('market_hash_name')

        self.median_avg_prices_15days = MedianAvgPrices15(
            self.market_hash_name,
            data.get('median_avg_prices_15days', [])
        )
        self.histogram = data.get('histogram')

        self._raw = data

    def __str__(self):
        return "ItemMarketData for {}".format(self.market_hash_name)

    def __repr__(self):
        return "<{}>".format(str(self))


class ItemPricesData(object):
    def __init__(self, data):
        self.market_hash_name = data.get('market_hash_name')

        self.avg = data.get('avg')
        self.latest = data.get('latest')
        self.max = data.get('max')
        self.mean = data.get('mean')
        self.min = data.get('min')

        self.safe = data.get('safe')
        self.safe_ts = data.get('safe_ts')

        self.sold = data.get('sold')

        self.unstable = data.get('unstable')
        self.unstable_reason = data.get('unstable_reason')

        self._raw = data

    def __str__(self):
        return "ItemPrice for {}".format(self.market_hash_name)

    def __repr__(self):
        return "<{}>".format(str(self))

class ItemOwned(object):
    def __init__(self, data):
        self.name = data.get('name')
        self.market_hash_name = data.get('market_hash_name')
        self.amount = int(data.get('amount'))

        self.appid = int(data.get('appid'))
        self.classid = int(data.get('classid'))

        self.icon_url = data.get('icon_url')
        self.icon_url_large = data.get('icon_url_large')

        self.market_tradable_restriction = data.get('market_tradable_restriction')
        self.market_marketable_restriction = data.get('market_marketable_restriction')
        self.marketable = data.get('marketable')

        self.prices = None #fill with an entry from a game's market list
        self.market_data = None #fill with results from a specific item's api

        self._raw = data

    def fill_prices_data(self, data):
        self.prices = ItemPricesData(data)

    def fill_market_data(self, data):
        self.market_data = ItemMarketData(data)

    def __str__(self):
        return "ItemOwned: {name}{amnt}::{cid}".format(
            name=self.market_hash_name,
            cid=self.classid,
            amnt="x"+self.amount if int(self.amount) > 1 else "",
        )

    def __repr__(self):
        return "<{}>".format(str(self))


class GameMarketData(object):
    def __init__(self, data):
        self.appid = data.get('appID')
        self.createdAt = data.get('createdAt')

        self.item_prices = self.build_item_prices(data['data'])

        self.item_market_data = [] #fill from api elsewhere
        self._raw_item_market_data = [] #fill from api elsewhere

        self.data = data.get('data')
        self._raw = data

    def __str__(self):
        return "GameMarketData for {}".format(self.appid)

    def __repr__(self):
        return "<{}>".format(str(self))

    def build_item_prices(self, data):
        item_prices = []
        for d in data:
            prices = ItemPricesData(d)
            item_prices.append(prices)

        return item_prices

    def take_item_market_data(self, item_mds):
        hash_names = list(map(attrgetter("market_hash_name"), self.item_prices))
        matching_mds = list(filter(
            lambda md: md.market_hash_name in hash_names,
            item_mds
        ))
        print('from {} input mds, I found {}'.format(len(item_mds), len(matching_mds)))

        existing_hash_names = list(map(attrgetter("market_hash_name"), self.item_market_data))
        unique_mds = list(filter(
            lambda md: md.market_hash_name not in existing_hash_names,
            matching_mds
        ))
        print('of those {} new mds, I found {} new ones'.format(len(matching_mds), len(unique_mds)))
        for md in unique_mds:
            self.item_market_data.append(md)

        #update raw_item_market_data
        raw_item_market_data = []
        for item_md in self.item_market_data:
            raw_item_market_data.append(item_md._raw)
        self._raw_item_market_data = raw_item_market_data

