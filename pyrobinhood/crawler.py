"""crawler.py: Use Robinhood's REST architecture to crawl relevant endpoints"""
import abc

import requests
import validators

from . import exceptions

API_ROOT = 'https://api.robinhood.com/'
HEADERS = {'User-Agent': 'github.com/lockefox/pyRobinhood'}

class Crawler():
    """TODO"""

    def __init__(self, address=API_ROOT, username='', password=''):
        self.endpoint = Endpoint(address=address)
        self.username = username
        self.password = password

    def __getattr__(self, name):
        value = self.endpoint[name]
        if validators.url(value):
            return Endpoint(address=value)

        return value

class Endpoint():
    """TODO"""

    def __init__(
            self,
            address=API_ROOT,
            # TODO: headers
            # TODO: auth
    ):
        self._address = address
        req = requests.get(self._address,)
        req.raise_for_status()
        self._contents = req.json()

        # append tree into object
        self.__dict__.update(self._contents)

    def __getitem__(self, route):
        return self.__dict__[route]
