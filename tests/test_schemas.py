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
        headers={'Authorization':'Token ' + token}
    )

    schema = helpers.load_schema('accounts.schema')

    jsonschema.validate(result, schema)
