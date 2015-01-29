========
dps-pxpy
========

.. image:: https://pypip.in/version/dps-pxpy/badge.svg
    :target: https://pypi.python.org/pypi/dps-pxpy/

.. image:: https://pypip.in/format/dps-pxpy/badge.svg
    :target: https://pypi.python.org/pypi/dps-pxpy/

.. image:: https://travis-ci.org/OohlaLabs/dps-pxpy.svg?branch=master
    :target: https://travis-ci.org/OohlaLabs/dps-pxpy

.. image:: https://coveralls.io/repos/OohlaLabs/dps-pxpy/badge.png?branch=master
    :target: https://coveralls.io/r/OohlaLabs/dps-pxpy

.. image:: https://pypip.in/py_versions/dps-pxpy/badge.svg
    :target: https://pypi.python.org/pypi/dps-pxpy/

.. image:: https://pypip.in/license/dps-pxpy/badge.svg
    :target: https://pypi.python.org/pypi/dps-pxpy/

This package provides a Python low-level client for the `DPS Payment Express <https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted>`_ API's.
Clients for both `PxPost <https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxPost>`_
and `PxFusion <https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxFusion.aspx>`_ are available.

Installation
------------
::

    pip install dps-pxpy


Usage
-----

PxPost
~~~~~~

PxPost allows merchants to handle the entire lifecycle of payment transactions using HTTPS POST requests.

For a complete documentation of the PxPost API: https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxPost.aspx

Client
``````
Instantiate a client with your PxPost username and password::


    from dps.pxpost import PxPostClient

    client = PxPostClient("username", "password")


PxPostClient relies on the popular `requests <https://pypi.python.org/pypi/requests>`_.

Authorize
`````````

To issue an authorization on a credit or debit card::

    response = client.authorize(amount="10.01",
                                input_currency="NZD",
                                card_number="4111111111111111",
                                card_holder_name="Holder Name",
                                date_expiry="1114",
                                cvc2="123")

You can also use a DPS billing token::

    response = client.authorize(amount="10.01",
                                input_currency="NZD",
                                dps_billing_id="billingtoken")

Or, a custom billing token::

    response = client.authorize(amount="10.01",
                                input_currency="NZD",
                                billing_id="custombillingtoken")

Complete
````````

To complete an authorization and transfer funds::

    response = client.complete(dps_txn_ref="reference")

Purchase
````````

``purchase`` is similar to ``authorize``, but funds are transferred immediately::

    response = client.purchase(amount="10.01",
                               input_currency="NZD",
                               card_number="4111111111111111",
                               card_holder_name="Holder Name",
                               date_expiry="1114",
                               cvc2="123")

You can also use a DPS or custom billing token.

Refund
``````

To perform a complete or partial refund, use the dps transaction id returned by ``purchase`` or ``complete``::

    response = client.refund(dps_txn_ref="reference",
                             amount="5.01",
                             merchant_reference="reason for refund")

Status
``````

To query the status of a transaction, use your merchant transaction id (``authorize`` and ``purchase`` can take an optional ``txn_id`` used as a unique merchant reference)::

    response = client.status(txn_id="inv1234")


PxFusion
~~~~~~~~

PxFusion allows merchants to accept credit card details within a form on their own web page. The form posts sensitive data directly to DPS, which processes the transaction and redirects the user's browser to the merchant's website in a way that is totally transparent to the cardholder.

For a complete documentation of the PxFusion API: https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxFusion.aspx

Client
``````

Instantiate a client with your PxFusion username and password::

    from dps.pxfusion import PxFusionClient

    client = PxFusionClient("username", "password")

PxFusionClient relies on `suds-jurko <https://pypi.python.org/pypi/suds-jurko/0.6>`_ for SOAP requests and ships with `suds_requests <https://pypi.python.org/pypi/suds_requests>`_ to take advantage of requests.

Transaction
```````````

To retrieve a session ID where funds are transferred immediately::

    response = client.purchase(amount="10.01",
                               currency="NZD",
                               return_url="https://yourdomain.com/pxfusion-callback",
                               txn_ref="ref")


You can also issue authorizations::

    response = client.authorize(amount="10.01",
                                currency="NZD",
                                return_url="https://yourdomain.com/pxfusion-callback",
                                txn_ref="ref")

Note that completing an authorization transaction must be done via PxPost's ``complete``.

After posting the payment details and session ID to the PxFusion endpoint (https://sec.paymentexpress.com/pxmi3/pxfusionauth), DPS redirects your customer to ``return_url`` with the session ID in the query string.

Status
``````

To check the outcome of a transaction::

    response = client.status(transaction_id="sessionid")

Cancellation
````````````

To prevent a transaction from taking place::

    response = client.cancel(transaction_id="sessionid")


Running Tests
-------------

Get a copy of the repository::

    git clone git@github.com:OohlaLabs/dps-pxpy.git .

Install `tox <https://pypi.python.org/pypi/tox>`_::

    pip install tox

Run the tests::

    tox

Contributions
-------------

All contributions and comments are welcome.

Change Log
----------

v0.2.1
~~~~~~
* Switch to Semantic Versioning
* Fix issue with parse_requirements for newer versions of pip (>=6.0.0)

v0.2
~~~~
* Fix setup.py for distribution

v0.1
~~~~
* Initial
