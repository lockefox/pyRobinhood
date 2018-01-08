"""test_schemas.py: validate responses from live Robinhood.com endpoints"""
import pytest
import jsonschema

import helpers

@pytest.mark.auth
def test_accounts_schema():
    """validate /accounts endpoint"""
    token = helpers.xfail_can_auth()

    result = helpers.raw_request_get(
        'https://api.robinhood.com/accounts/',
        headers={'Authorization': 'Token ' + token},
    )

    schema = helpers.load_schema('accounts.schema')

    jsonschema.validate(result, schema)

@pytest.mark.auth
def test_applications_schema():
    """validate /applications endpoint"""
    token = helpers.xfail_can_auth()

    result = helpers.raw_request_get(
        'https://api.robinhood.com/applications/',
        headers={'Authorization': 'Token ' + token},
    )

    schema = helpers.load_schema('applications.schema')

    jsonschema.validate(result, schema)

@pytest.mark.auth
def test_dividends_schema():
    """validate /dividends endpoint"""
    token = helpers.xfail_can_auth()

    result = helpers.raw_request_get(
        'https://api.robinhood.com/dividends/',
        headers={'Authorization': 'Token ' + token},
    )

    schema = helpers.load_schema('dividends.schema')

    jsonschema.validate(result, schema)

@pytest.mark.auth
def test_documents_schema():
    """validate /documents endpoint"""
    token = helpers.xfail_can_auth()

    result = helpers.raw_request_get(
        'https://api.robinhood.com/documents/',
        headers={'Authorization': 'Token ' + token},
    )

    schema = helpers.load_schema('documents.schema')

    jsonschema.validate(result, schema)

def test_fundamentals_schema():
    """validate /fundamentals endpoint"""
    result = helpers.raw_request_get(
        'https://api.robinhood.com/fundamentals/',
        params={'symbols': helpers.CONFIG.get('tests', 'good_stock_list')},
    )

    schema = helpers.load_schema('fundamentals.schema')

    jsonschema.validate(result, schema)

def test_instruments_schema():
    """validate /instruments endpoint"""
    result = helpers.raw_request_get(
        'https://api.robinhood.com/instruments/' +
        helpers.CONFIG.get('tests', 'good_instrument')
    )

    schema = helpers.load_schema('instruments.schema')

    jsonschema.validate(result, schema)

def test_news_schema():
    """validate /midlands/news/ endpoint"""
    result = helpers.raw_request_get(
        'https://api.robinhood.com/midlands/news/',
        params={'symbol': helpers.CONFIG.get('tests', 'good_stock')}
    )

    schema = helpers.load_schema('news.schema')

    jsonschema.validate(result, schema)
