"""
appid: 578080,
classid: "2225519338",
instanceid: "0",
currency: 0,
background_color: "",
icon_url: "8HAGSsiO9OXk0bu4o76O6xabNUY8RRLf00e56zWT3IZUH8Flab9goIFna_837oFuZVQtrmh23qr2ro4kS68RfPtexg",
icon_url_large: "8HAGSsiO9OXk0bu4o76O6xabNUY8RRLf00e56zWT3IZUH8Flab9goIFna_837oFuZVQtrmh23qr2ro4kS68RfPtexg",
tradable: 1,
name: "Bloody Shirt",
type: "",
market_name: "Bloody Shirt",
market_hash_name: "Bloody Shirt",
commodity: 1,
market_tradable_restriction: 7,
market_marketable_restriction: 7,
marketable: 1

prices
  'prices': {'avg': 0.61,
             'latest': 0.53,
             'max': 0.72,
             'mean': 0.6,
             'min': 0.51,
             'safe': 0.56,
             'safe_ts': {'last_24h': 0.57,
                         'last_30d': 0.28,
                         'last_7d': 0.56,
                         'last_90d': 0.35},
             'sold': {'avg_daily_volume': 3331,
                      'last_24h': 2504,
                      'last_30d': 108884,
                      'last_7d': 23323,
                      'last_90d': 225277},
             'unstable': False,
             'unstable_reason': False},
"""

class ItemPrices(object):
    def __init__(self, data):
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


class Item(object):
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

        self.prices = ItemPrices(data.get('prices'))

        self._raw = data

    def __str__(self):
        return "Item: {name}{amnt}::{cid}".format(
            name=self.market_hash_name,
            cid=self.classid,
            amnt="x"+self.amount if int(self.amount) > 1 else "",
        )

    def __repr__(self):
        return "<{}>".format(str(self))
