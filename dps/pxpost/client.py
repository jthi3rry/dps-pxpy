# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import requests
from xml.dom.minidom import Document

from ..vendors import xmltodict
from ..vendors.inflection import camelize
from ..utils import underscore_keys_postproc
from ..transactions import accept_txn

from .transactions import PxPostCardTransaction, PxPostDpsBillingTransaction, PxPostBillingTransaction, \
                          PxPostCompleteTransaction, PxPostRefundTransaction, PxPostStatusTransaction


__all__ = ["PxPostClient"]


class PxRequest(object):
    """
    PxPost/PxFusion XML Transaction helper class.

    This class transforms keyword arguments into an XML-formatted request as required by DPS SOAP endpoints.
    """

    def __init__(self, root_tag, **kwargs):
        """
        Create a new PxRequest instance.

        Args:
          root_tag (str): XML tag that will contain parameters sent to DPS.

        Keyword Args:
          Accepts an arbitrary list of keyword arguments to be transformed into XML camelized elements inside the root
          tag.
        """
        self.dict = kwargs
        self.root_tag = root_tag

    def to_xml(self):
        """Returns request as an XML document fragment."""
        doc = Document()
        root = doc.createElement(self.root_tag)
        for key, value in self.dict.items():
            element = doc.createElement(camelize(key))
            element.appendChild(doc.createTextNode(str(value)))
            root.appendChild(element)
        doc.appendChild(root)
        return doc.toxml()


class PxResponse(object):
    """
    PxPost/PxFusion XML Response helper class.
    """

    def __init__(self, xml):
        """
        Create a new PxResponse.

        Args:
          xml (str): XML document fragment received from DPS.
        """
        self.xml = xml

    def to_dict(self):
        """Returns response as a Python dictionary."""
        dictionary = dict(xmltodict.parse(self.xml, postprocessor=underscore_keys_postproc))
        return list(dictionary.values()).pop()


class PxPostClient(object):
    """
    PxPost Endpoint.

    This class performs calls to the DPS PxPost service as documented at:
    http://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxPost

    """

    URI = 'https://sec.paymentexpress.com/pxpost.aspx'

    AUTHORIZE = 'Auth'
    PURCHASE = 'Purchase'
    COMPLETE = 'Complete'
    REFUND = 'Refund'
    VALIDATE = 'Validate'
    STATUS = 'Status'

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def post(self, **kwargs):
        """
        Performs a call to the pxpost endpoint.

        Required kwargs:
          txn_type (str)
          amount (str)
          input_currency (str)

        Required kwargs for dps billing token transactions:
          dps_billing_id (str)

        Required kwargs for custom billing token transactions:
          billing_id (str)

        Required kwargs for payment card transactions:
          card_holder_name (str)
          card_number (str)
          cvc2 (str)
          date_expiry (str)

        Required kwargs for complete transactions:
          dps_txn_ref (str)

        Optional kwargs:
          avs_action (int)
          avs_post_code (str)
          avs_street_address (str)
          cvc2_presence (int)
          date_start (str)
          enable_add_bill_card (int)
          enable_avs_data (int)
          issue_number (int)
          merchant_reference (str)
          session_id (str)
          track2 (str)
          txn_data1 (str)
          txn_data2 (str)
          txn_data3 (str)
          txn_id (str)
          txn_ref (str)

        """
        kwargs.update({'post_username': self.username, 'post_password': self.password})
        response = requests.post(self.URI, data=PxRequest('Txn', **kwargs).to_xml())
        response.raise_for_status()
        return PxResponse(response.content).to_dict()

    @accept_txn(PxPostCardTransaction, PxPostDpsBillingTransaction, PxPostBillingTransaction)
    def authorize(self, **kwargs):
        """
        Authorizes a transaction. Must be completed within 7 days
        using the "Complete" TxnType.

        """
        return self.post(txn_type=self.AUTHORIZE, **kwargs)

    @accept_txn(PxPostCompleteTransaction)
    def complete(self, **kwargs):
        """
        Completes (settles) a pre-approved Auth Transaction. The
        DpsTxnRef value returned by the original approved Auth
        transaction must be supplied, as well as an amount.

        """
        return self.post(txn_type=self.COMPLETE, **kwargs)

    @accept_txn(PxPostCardTransaction, PxPostDpsBillingTransaction, PxPostBillingTransaction)
    def purchase(self, **kwargs):
        """
        Performs a transaction where funds are transferred immediately.

        """
        return self.post(txn_type=self.PURCHASE, **kwargs)

    @accept_txn(PxPostRefundTransaction)
    def refund(self, **kwargs):
        """
        Performs a refund where funds are transferred immediately.

        """
        return self.post(txn_type=self.REFUND, **kwargs)

    @accept_txn(PxPostCardTransaction)
    def validate(self, **kwargs):

        """
        Validation Transaction. Issues a $1.00 Auth to validate card
        details including expiry date. Often utilised with the
        EnableAddBillCard property set to 1 to automatically add to
        Billing Database if the transaction is approved.

        """
        return self.post(txn_type=self.VALIDATE, **kwargs)

    @accept_txn(PxPostStatusTransaction)
    def status(self, **kwargs):
        """
        If you didn't receive a response to your Post, or if StatusRequired
        was set to 1 in the response, then you must send another Post to
        request the status of the transaction. For this function to work you
        will need to send up a TxnId with your original transaction. TxnId
        must be a unique value for each transaction. It can be up to 16
        characters long.

        """
        return self.post(txn_type=self.STATUS, **kwargs)
