"""crawler.py: Use Robinhood's REST architecture to crawl relevant endpoints"""
import logging
import atexit

import requests
import validators

from . import exceptions

API_ROOT = 'https://api.robinhood.com/'
HEADERS = {'User-Agent': 'github.com/lockefox/pyRobinhood'}

def get_auth_token(
        username,
        password,
        route='https://api.robinhood.com/api-token-auth/'
):
    """get an auth token for authenticated feeds

    Args;
        username (str): Robinhood Username
        password (str): Robinhood Password
        route (str): URL for token auth

    Notes:
        create atexit handle to close tokens responsibly

    Returns:
        str: auth token

    Raises:
        requests.exception: HTTP/connection errors

    """
    logging.debug('Fetching AUTH token')
    req = requests.post(
        url=route,
        json={
            'username': username,
            'password': password
        }
    )
    req.raise_for_status()
    token = req.json()['token']

    #TODO: create atexit handle for token

    return token

class Endpoint:
    """Robinhood endpoint crawler

    Args:
        address (str): source address
        username (str): username for auth
        password (str): password for auth
        token (str): token for auth
        params (dict): params for request
        _raw_data (dict): raw data (no request)

    """
    def __init__(
            self,
            address=API_ROOT,
            username='',
            password='',
            token='',
            params={},
            _raw_data={},
    ):
        self.__address = address
        self.__username = username
        self.__password = password
        self._data = {}
        self._is_iter = False
        self._token = token

        headers = {}
        if self._token:
            headers = {'Authorization': 'Token ' + self._token}

        if _raw_data:
            self._data = _raw_data
        else:
            self._data = self.fetch_endpoint(params=params, headers=headers)

    def fetch_endpoint(
            self,
            params={},
            headers={},
            _recur=False,
    ):
        """fetch data from Robinhood

        Args:
            params (dict): request params
            headers (dict): request headers
            _recur (bool): recursion check

        Returns:
            dict: raw JSON data for endpoint

        Raises:
            requests.exceptions: HTTP/connection errors

        """
        logging.debug('Fetching: %s', self.__address)
        try:
            req = requests.get(
                url=self.__address,
                params=params,
                headers=headers,
            )
            req.raise_for_status()
            data = req.json()
        except Exception:
            if _recur:
                raise

            self._token = get_auth_token(self.__username, self.__password)
            headers.update({'Authorization': 'Token ' + self._token})
            data = self.fetch_endpoint(
                params=params, headers=headers, _recur=True
            )

        #TODO test/setup __iter__ handles, yield only `results` if paginated

        return data

    def __getattr__(self, item):
        if item in self.__dict__:  # TODO: this seems wrong
            return self.__dict__[item]

        value = self._data[item]

        if isinstance(value, list):
            return [
                Endpoint(
                    address=self.__address,
                    username=self.__username,
                    password=self.__password,
                    token=self._token,
                    _raw_data=row,)
                for row in value
            ]
        if isinstance(value, dict):
            return Endpoint(
                address=self.__address,
                username=self.__username,
                password=self.__password,
                token=self._token,
                _raw_data=value,
            )
        if validators.url(value):
            return Endpoint(
                address=value,
                username=self.__username,
                password=self.__password,
                token=self._token,
            )

        return value

    def __repr__(self):
        return str(self._data)
