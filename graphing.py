#!ipython3

import json
import dateutil
from operator import itemgetter
import requests

import matplotlib.pyplot as plt
import numpy as np

from pprint import pprint as pp

import models


def trendline(median_data, days=15):
    if not isinstance(median_data, models.MedianAvgPrices15):
        raise Exception("must be MedianAvgPrices15")

    data = median_data.data[-days:]

    x = np.arange(0, len(data))
    y = np.array(list(map(itemgetter(1), data)))

    order = 1
    coeffs = np.polyfit(x, y, order)
    slope = coeffs[-2]

    result = round(float(slope), 3)
    return result

