======================
Crawling Robinhood API
======================

Hats off to the team at `Robinhood`_ their `REST API`_ is well formed.  pyRobinhood uses the REST API architecture online to crawl and gather data directly by route.

Just walk the API node-by-node.  Crawler is provided as a layer to access raw `Robinhood`_ data.  Filtering and subsetting will be done by **TODO**

.. code-block:: python

    import pyrobinhood.crawler as crawler

    root = crawler.Endpoint(username='MYACCOUNT', password='MYPASSWORD')

    # List all companies in Robinhood tracking
    company_fundamentals = []
    for page in root.fundamentals
        company_fundamentals.extend(page.results)


    # List all stocks I hold
    my_stocks = []
    for page in root.account.positions:
        my_stocks.extend(page.results)


.. _Robinhood: https://robinhood.com/
.. _REST API: https://github.com/sanko/Robinhood