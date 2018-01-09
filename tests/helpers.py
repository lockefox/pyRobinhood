'''helpers.py: pytest helpers/config parsers'''
import atexit
from os import path
import json
import configparser
import inspect

import pytest
import requests

HERE = path.abspath(path.dirname(__file__))
AUTH_KEY = ''
ENDPOINTS = {}

def fetch_endpoints(endpoint_name, api_root='https://api.robinhood.com/', _recur=False):
    """get routes from REST root

    Args:
        endpoint_name (str): name of endpoint
        api_root (str): URL for ROOT
        recur (bool): has recursed?  avoid infini-loop

    Returns:
        str: address for desired endpoint

    Raises:
        requests.exceptions: HTTP/connection errors
        KeyError: endpoint_name not found

    """
    global ENDPOINTS
    if endpoint_name in ENDPOINTS:
        return ENDPOINTS[endpoint_name]

    if _recur:
        raise Exception('Infinite Loop')

    req = requests.get(api_root)
    req.raise_for_status()

    ENDPOINTS = req.json()
    return fetch_endpoints(endpoint_name, _recur=True)

def load_config(config_path=path.join(HERE, 'test_options.cfg')):
    """load test configuration from file

    Notes:
        Prefers *_local.cfg, untracked by git

    Args:
        config_path (str): path to config file

    Returns:
        configparser.ConfigParser: config parser object

    Raises:
        FileNotFoundError: unable to find valid filepath

    """
    local_cfg_path = config_path.replace('.cfg', '_local.cfg')
    if path.isfile(local_cfg_path):
        config_path = local_cfg_path

    config = configparser.ConfigParser(
        interpolation=configparser.ExtendedInterpolation(),
        allow_no_value=True,
        delimiters=('='),
        inline_comment_prefixes=('#')
    )

    with open(config_path, 'r') as cfg_fh:
        config.read_file(cfg_fh)

    return config

CONFIG = load_config()

def raw_request_get(
        endpoint='',
        endpoint_url='',
        params=None,
        headers=None,
):
    """fetch raw data from endpoint

    Args:
        endpoint (str): name
        endpoint_url (str): direct-connect url
        params (:obj:`dict`): params for request
        headers (:obj:`dict`): HTTP headers

    Returns:
        dict: JSON parsed data

    Raises:
        requests.exceptions: HTTP/connection errors

    """
    if not endpoint_url:
        endpoint_url = fetch_endpoints(endpoint)
    req = requests.get(endpoint_url, params=params, headers=headers)
    req.raise_for_status()
    return req.json()


def xfail_can_auth(config=CONFIG):
    """help make sure test can run

    Args:
        config (:obj:`configparser.ConfigParser`): configuration object

    Returns:
        str: auth token

    Raises:
        pytest.xfail: xFail test if can't auth:

    """
    if not config.get('robinhood', 'username') and not config.get('robinhood', 'password'):
        pytest.xfail('Unable to auth -- {}()'.format(
            inspect.getouterframes(inspect.currentframe(), 2)[1][3]
        ))

    global AUTH_KEY
    if not AUTH_KEY:
        try:
            req = requests.post('https://api.robinhood.com/api-token-auth/', data={
                'username':config.get('robinhood', 'username'),
                'password':config.get('robinhood', 'password'),
            })
            req.raise_for_status()
            AUTH_KEY = req.json()['token']
        except Exception as err:
            pytest.xfail('Unable to connect to auth {!r}'.format(err))

        atexit.register(end_logout, AUTH_KEY)

    return AUTH_KEY

def end_logout(auth_key):
    """atexit handler for logging out token

    Args:
        auth_key (str): token to log out

    Raises:
        requests.exceptions: HTTP/connection errors

    """
    print('logging out!')
    req = requests.post(
        'https://api.robinhood.com/api-token-logout/',
        headers={'Authorization':'Token ' + auth_key},
    )
    req.raise_for_status()


def load_schema(
        schema_name,
        schema_path=path.join(HERE, 'schemas')
):
    """load JSONschema from file

    Args:
        schema_name (str): name of schema file
        schema_path (str): path to schema collection

    Returns:
        dict: JSON-parsed schema file

    Raises:
        FileNotFoundError: unable to locate desired schema

    """
    with open(path.join(schema_path, schema_name)) as schema_fh:
        schema = json.load(schema_fh)

    return schema
