# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from suds.client import Client as SOAPClient

from ..vendors import suds_requests
from ..vendors.inflection import camelize
from ..utils import underscore_keys
from ..transactions import accept_txn

from .transactions import PxFusionGetTransaction, PxFusionStatusTransaction, PxFusionCancelTransaction


class PxFusionClient(object):
    """
    PxFusion Endpoint.

    This class performs calls to the DPS PxFusion service as documented at:
    http://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxFusion

    """

    WSDL = 'https://sec.paymentexpress.com/pxf/pxf.svc?wsdl'

    AUTH = 'Auth'
    PURCHASE = 'Purchase'

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.soap_client = SOAPClient(self.WSDL, transport=suds_requests.RequestsTransport())

    def create_transaction_details(self, **kwargs):
        """
        Hydrates a TransactionDetails SOAP object from kwargs

        """
        txn_details = self.soap_client.factory.create('TransactionDetails')
        for k, v in kwargs.items():
            txn_details[camelize(k, False)] = v
        return txn_details

    def get_transaction_id(self, **kwargs):
        """
        The merchant will make a server-side SOAP HTTP POST to the
        web service. The data submitted will not include sensitive
        card data such as card number, expiry date, CVC, card holder
        name and issue number. This data is not collected by, and is
        never available to, the merchant website.

        Required kwargs:
          txn_type (str)
          amount (str)
          currency (str)
          return_url (str)
          txn_ref (str)

        Optional kwargs:
          avs_action (int)
          avs_post_code (str)
          avs_street_address (str)
          billing_id (str)
          date_start (str)
          enable_add_bill_card (int)
          enable_avs_data (int)
          enable_pax_info (int)
          merchant_reference (str)
          pax_carrier (str)
          pax_carrier2 (str)
          pax_carrier3 (str)
          pax_carrier4 (str)
          pax_class1 (str)
          pax_class2 (str)
          pax_class3 (str)
          pax_class4 (str)
          pax_date2 (str)
          pax_date3 (str)
          pax_date4 (str)
          pax_date_depart (str)
          pax_fare_basis1 (str)
          pax_fare_basis2 (str)
          pax_fare_basis3 (str)
          pax_fare_basis4 (str)
          pax_flight_number1 (str)
          pax_flight_number2 (str)
          pax_flight_number3 (str)
          pax_flight_number4 (str)
          pax_leg1 (str)
          pax_leg2 (str)
          pax_leg3 (str)
          pax_leg4 (str)
          pax_name (str)
          pax_origin (str)
          pax_stop_over_code1 (str)
          pax_stop_over_code2 (str)
          pax_stop_over_code3 (str)
          pax_stop_over_code4 (str)
          pax_ticket_number (str)
          pax_time1 (str)
          pax_time2 (str)
          pax_time3 (str)
          pax_time4 (str)
          pax_travel_agent_info (str)
          txn_data1 (str)
          txn_data2 (str)
          txn_data3 (str)

        """
        trans_details = self.create_transaction_details(**kwargs)
        response = self.soap_client.service.GetTransactionId(self.username, self.password, trans_details)
        return underscore_keys(dict(response))

    def get_transaction(self, transaction_id):
        """
        Upon receiving a request for the returnUrl the merchant is
        in a position to be able to update their records in
        recognition of the transaction and/or present the result to
        the user. To do so the merchant must make a GetTransaction
        SOAP call. The merchant populates the tranasctionId parameter
        of the GetTransaction SOAP call with sessionId value contained
        within the query string.

        """
        response = self.soap_client.service.GetTransaction(self.username, self.password, transaction_id)
        return underscore_keys(dict(response))

    def cancel_transaction(self, transaction_id):
        """
        The merchant will make a server-side SOAP HTTP POST to the web
        service. The call will prevent a transaction taking place for
        a given sessionId.

        """
        return self.soap_client.service.CancelTransaction(self.username, self.password, transaction_id)

    @accept_txn(PxFusionGetTransaction)
    def authorize(self, **kwargs):
        """
        Authorise - Amount is authorised, no funds transferred.

        Facade to get_transaction_id that takes a transaction as argument

        """
        return self.get_transaction_id(txn_type=self.AUTH, **kwargs)

    @accept_txn(PxFusionGetTransaction)
    def purchase(self, **kwargs):
        """
        Purchase - Funds are transferred immediately.

        Facade to get_transaction_id that takes a transaction as argument

        """
        return self.get_transaction_id(txn_type=self.PURCHASE, **kwargs)

    @accept_txn(PxFusionStatusTransaction)
    def status(self, **kwargs):
        """
        Status - requests transaction status after user
        is redirect back from dps

        Facade to get_transaction that takes a transaction as argument

        """
        return self.get_transaction(**kwargs)

    @accept_txn(PxFusionCancelTransaction)
    def cancel(self, **kwargs):
        """
        Cancel - cancel transaction for given session

        Facade to cancel_transaction that takes a transaction as argument

        """
        return self.cancel_transaction(**kwargs)
