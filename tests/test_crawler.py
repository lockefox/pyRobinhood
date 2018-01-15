"""test_crawler.py: validate Robinhood crawler utilities"""

import pytest
import requests_mock
import jsonschema

import helpers
import pyrobinhood.crawler as crawler
import pyrobinhood.exceptions as exceptions

def test_prod_crawler_pub():
    """validate we can spawn a prod crawler"""
    endpoint = crawler.Endpoint()

    fundamentals = endpoint.instruments.results[0].fundamentals._data

    schema = helpers.load_schema('fundamentals.schema')

    jsonschema.validate(fundamentals, schema['properties']['results']['items'],)

@pytest.mark.auth
def test_prod_crawler_auth():
    """validate auth crawler on prod"""
    helpers.xfail_can_auth()

    endpoint = crawler.Endpoint(
        username=helpers.CONFIG.get('robinhood', 'username'),
        password=helpers.CONFIG.get('robinhood', 'password'),
    )

    positions = endpoint.accounts.results[0].positions._data

    schema = helpers.load_schema('positions.schema')

    jsonschema.validate(positions, schema)
