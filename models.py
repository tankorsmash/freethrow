import dateutil

import graphing


def convert_median_data(row):
    return [dateutil.parser.parse(row[0]), round(row[1], 3), row[2]]

class MedianAvgPrices15(object):
    def __init__(self, market_hash_name, data):
        self.market_hash_name = market_hash_name

        self.data = list(map(convert_median_data, data))

        self._raw = data

    def __str__(self):
        return "ItemMarketData for {}".format(self.market_hash_name)

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

        self.prices = None
        self.market_data = None

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
        self.appid = data.get('appid')
        self.createdAt = data.get('createdAt')

        self.data = data.get('data')

        self._raw = data

    def __str__(self):
        return "GameMarketData for {}".format(self.appid)

    def __repr__(self):
        return "<{}>".format(str(self))
