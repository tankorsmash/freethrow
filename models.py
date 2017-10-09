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
"""


class Item(object):
    def __init__(self, data):
        self.name = data.get('name')
        self.market_hash_name = data.get('market_hash_name')
        self.amount = int(data.get('amount'))

        self.appid = int(data.get('appid'))
        self.classid = int(data.get('classid'))

        self.icon_url = data.get('icon_url')
        self.icon_url_large = data.get('icon_url_large')

        self.prices = data.get('prices')

        self._raw = data

    def __str__(self):
        return "Item: {name}{amnt}::{cid}".format(
            name=self.market_hash_name,
            cid=self.classid,
            amnt="x"+self.amount if int(self.amount) > 1 else "",
        )

    def __repr__(self):
        return "<{}>".format(str(self))
