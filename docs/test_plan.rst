===================
Testing pyRobinhood
===================

We take testing and coverage seriously.  You depend on Robinhood to execute orders on a valuable account, and you should trust your API/interface just as much.

Schema Tests
============

pyRobinhood is designed to let the REST lead, and return the results as directly as possible.  To monitor what is actually returned, ``test_schema.py`` exercizes Robinhood's REST endpoints directly. 

There are two key problems our schema tests cover:

1. API endpoints remain consistent
2. Give a doc/seed for mock tests

`New to JsonSchema?`_

Skipped Endpoints
-----------------

- ``/subscription/subscription_fees/``
- ``/subscription/subscriptions/``
- ``/cash_journal/margin_interest_charges/``
- ``/margin/upgrades/``
- ``/password_reset/request/``
- ``/password_change/``
- ``/wire/relationships/``
- ``/ach/queued_deposit/``
- ``/wire/transfers/``
- ``/settings/notifications/``

Authorization
=============

Though live Robinhood tests would be best, Robinhood account credentials are extremely valuable.  

We do not test authorized feeds in `CI`_, and opt for mocks as much as possible to exercize code.  Any live-tests that require authorization should be marked with ``@pytest.mark.auth``.

To test authorized feeds:

.. code-block:: bash

    cp tests/test_options.cfg tests/test_options_local.cfg
    # fill out #SECRETS
    python setup.py test

.. _New to JsonSchema?: https://spacetelescope.github.io/understanding-json-schema/
.. _CI: https://travis-ci.org/lockefox/pyRobinhood