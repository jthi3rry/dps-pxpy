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
It provides clients for both `PxPost <https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxPost>`_
and `PxFusion <https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxFusion.aspx>`_.

Installation
------------
::

    pip install dps-pxpy


Usage
-----

PxPost
~~~~~~

`PxPost <https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxPost>`_ allows merchants to perform authorisations, payments and refunds.

Client
``````
First, instantiate a client with your PxPost username and password::


    from dps.pxpost import PxPostClient

    client = PxPostClient("username", "password")


The client provides either a low level ``post`` method taking keyword arguments, or higher level ``authorize``, ``purchase``, ``complete``, ``refund`` and ``status`` methods.

Authorize
`````````

To issue an authorisation on a credit or debit card::

    response = client.authorize(amount="10.01", input_currency="NZD", card_number="4111111111111111", card_holder_name="Holder Name", date_expiry="1114", cvc2="123")

This will issue an POST to the PxPost endpoint (dps-pxpy relies on the popular `requests <https://pypi.python.org/pypi/requests>`_).

You can also use a DPS billing token::

    response = client.authorize(amount="10.01", input_currency="NZD", dps_billing_id="billingtoken")

Or a custom billing token::

    response = client.authorize(amount="10.01", input_currency="NZD", billing_id="custombillingtoken")

Complete
````````

When you issue an authorisation and get a transaction reference from DPS, you can use this reference to complete the transaction and transfer the funds::

    response = client.complete(dps_txn_ref="reference")

Purchase
````````

``purchase`` is used in the same way as ``authorize``, but funds are transferred immediately::

    response = client.purchase(amount="10.01", input_currency="NZD", card_number="4111111111111111", card_holder_name="Holder Name", date_expiry="1114", cvc2="123")

Note that you can use a DPS or custom billing token as per the ``authorize`` examples.

Refund
``````

When a transaction was completed (either via ``complete`` or ``purchase``), you can perform a refund using the transaction reference::

    response = client.refund(dps_txn_ref="reference", amount="10.50", merchant_reference="reason for refund")

Status
``````

Finally, you can query the status of a transaction via a transaction ID (``authorize`` and ``purchase`` can take an optional ``txn_id`` used as a unique merchant reference)::

    response = client.status(txn_id="inv1234")

For a complete documentation of the PxPost API: https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxPost.aspx

PxFusion
~~~~~~~~

`PxFusion <https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxFusion.aspx>`_ is used when you do not want to have credit or debit card numbers transiting through your servers, but instead you want your customers to post their details to DPS directly and transparently while simply getting the outcome of the transaction.

Client
``````

First, instantiate a client with your PxFusion username and password::

    from dps.pxfusion import PxFusionClient

    client = PxFusionClient("username", "password")

Transaction
```````````

Before being able to post payment details to DPS, you need to initiate a transaction to retrieve a transaction ID (also called session ID)::

    response = client.purchase(amount="10.01", currency="NZD", return_url="https://example.org/callback", txn_ref="ref")

This will issue a SOAP call to ``GetTransactionId`` and initiate a ``Purchase`` transaction (dps-pxpy relies on `suds-jurko <https://pypi.python.org/pypi/suds-jurko/0.6>`_). You can also issue an ``Authorize`` transaction by using ``client.authorize`` instead of ``client.purchase``. Note that completing an authorisation can only be done via PxPost.

Note that, at this stage, you can request a billing token to be returned with the outcome of the transaction and use it with PxPost for recurrent billing or subsequent payments.

Status
``````

After posting the payment details along with the session ID to the PxFusion HTTP endpoint (https://sec.paymentexpress.com/pxmi3/pxfusionauth), DPS will redirect your customer to the ``return_url`` specified in the purchase or authorisation along with the session ID in the query string, this is when you need to check the outcome of the transaction::

    response = client.status(transaction_id='sessionid')

Cancellation
````````````

To prevent a transaction from taking place, it can be cancelled::

    response = client.cancel(transaction_id="sessionid")

For a complete documentation of the PxFusion API: https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxFusion.aspx


Running Tests
-------------
::

    tox


Contributions
-------------

All contributions and comments are welcome.

Change Log
----------

v0.1
~~~~
* Initial
