"""test_schemas.py: validate responses from live Robinhood.com endpoints"""
import pytest
import jsonschema
import requests

import helpers

def test_api_root():
    """validate / has all expected routes"""
    endpoint_list = {
        'mfa': 'https://api.robinhood.com/mfa/',
        'margin_interest_charges': 'https://api.robinhood.com/cash_journal/margin_interest_charges/',
        'margin_upgrades': 'https://api.robinhood.com/margin/upgrades/',
        'instruments': 'https://api.robinhood.com/instruments/',
        'quotes': 'https://api.robinhood.com/quotes/',
        'accounts': 'https://api.robinhood.com/accounts/',
        'orders': 'https://api.robinhood.com/orders/',
        'subscription_fees': 'https://api.robinhood.com/subscription/subscription_fees/',
        'id_documents': 'https://api.robinhood.com/upload/photo_ids/',
        'portfolios': 'https://api.robinhood.com/portfolios/',
        'markets': 'https://api.robinhood.com/markets/',
        'wire_relationships': 'https://api.robinhood.com/wire/relationships/',
        'ach_queued_deposit': 'https://api.robinhood.com/ach/queued_deposit/',
        'subscriptions': 'https://api.robinhood.com/subscription/subscriptions/',
        'wire_transfers': 'https://api.robinhood.com/wire/transfers/',
        'dividends': 'https://api.robinhood.com/dividends/',
        'notification_settings': 'https://api.robinhood.com/settings/notifications/',
        'applications': 'https://api.robinhood.com/applications/',
        'user': 'https://api.robinhood.com/user/',
        'ach_relationships': 'https://api.robinhood.com/ach/relationships/',
        'ach_deposit_schedules': 'https://api.robinhood.com/ach/deposit_schedules/',
        'ach_iav_auth': 'https://api.robinhood.com/ach/iav/auth/',
        'notifications': 'https://api.robinhood.com/notifications/',
        'ach_transfers': 'https://api.robinhood.com/ach/transfers/',
        'positions': 'https://api.robinhood.com/positions/',
        'watchlists': 'https://api.robinhood.com/watchlists/',
        'document_requests': 'https://api.robinhood.com/upload/document_requests/',
        'edocuments': 'https://api.robinhood.com/documents/',
        'password_reset': 'https://api.robinhood.com/password_reset/request/',
        'password_change': 'https://api.robinhood.com/password_change/',
    }
    req = requests.get('https://api.robinhood.com/')
    req.raise_for_status()
    data = req.json()

    assert data == endpoint_list

@pytest.mark.auth
def test_accounts_schema():
    """validate /accounts endpoint"""
    token = helpers.xfail_can_auth()

    result = helpers.raw_request_get(
        endpoint='accounts',
        headers={'Authorization': 'Token ' + token},
    )

    schema = helpers.load_schema('accounts.schema')

    jsonschema.validate(result, schema)

@pytest.mark.auth
def test_applications_schema():
    """validate /applications endpoint"""
    token = helpers.xfail_can_auth()

    result = helpers.raw_request_get(
        endpoint='applications',
        headers={'Authorization': 'Token ' + token},
    )

    schema = helpers.load_schema('applications.schema')

    jsonschema.validate(result, schema)

@pytest.mark.auth
def test_dividends_schema():
    """validate /dividends endpoint"""
    token = helpers.xfail_can_auth()

    result = helpers.raw_request_get(
        endpoint='dividends',
        headers={'Authorization': 'Token ' + token},
    )

    schema = helpers.load_schema('dividends.schema')

    jsonschema.validate(result, schema)

@pytest.mark.auth
def test_documents_schema():
    """validate /documents endpoint"""
    token = helpers.xfail_can_auth()

    result = helpers.raw_request_get(
        endpoint='edocuments',
        headers={'Authorization': 'Token ' + token},
    )

    schema = helpers.load_schema('documents.schema')

    jsonschema.validate(result, schema)

def test_fundamentals_schema():
    """validate /fundamentals endpoint"""
    result = helpers.raw_request_get(
        endpoint_url='https://api.robinhood.com/fundamentals/',
        params={'symbols': helpers.CONFIG.get('tests', 'good_stock_list')},
    )

    schema = helpers.load_schema('fundamentals.schema')

    jsonschema.validate(result, schema)

def test_instruments_schema():
    """validate /instruments endpoint"""
    # TODO: instruments from API ROOT
    result = helpers.raw_request_get(
        endpoint='instruments'
    )

    schema = helpers.load_schema('instruments.schema')

    jsonschema.validate(result, schema)

def test_markets_schema():
    """validate /markets endpoint"""
    result = helpers.raw_request_get(
        endpoint='markets'
    )

    schema = helpers.load_schema('markets.schema')

    jsonschema.validate(result, schema)

@pytest.mark.auth
def test_mfa_schema():
    """validate /mfa endpoint"""
    token = helpers.xfail_can_auth()

    result = helpers.raw_request_get(
        endpoint='mfa',
        headers={'Authorization': 'Token ' + token},
    )

    schema = helpers.load_schema('mfa.schema')

    jsonschema.validate(result, schema)

def test_news_schema():
    """validate /midlands/news/ endpoint"""
    # TODO: not on API ROOT?
    result = helpers.raw_request_get(
        endpoint_url='https://api.robinhood.com/midlands/news/',
        params={'symbol': helpers.CONFIG.get('tests', 'good_stock')}
    )

    schema = helpers.load_schema('news.schema')

    jsonschema.validate(result, schema)

@pytest.mark.auth
def test_orders_schema():
    """validate /orders endpoint"""
    token = helpers.xfail_can_auth()

    result = helpers.raw_request_get(
        endpoint='orders',
        headers={'Authorization': 'Token ' + token},
    )

    schema = helpers.load_schema('orders.schema')

    jsonschema.validate(result, schema)

def test_quotes_schema():
    """validate /quotes endpoint"""
    # TODO: not on API ROOT?
    result = helpers.raw_request_get(
        endpoint='quotes',
        params={'symbols': helpers.CONFIG.get('tests', 'good_stock_list')}
    )

    schema = helpers.load_schema('quotes.schema')

    jsonschema.validate(result, schema)
