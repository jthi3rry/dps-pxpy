# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from .. import transactions as txn

__all__ = ["PxPostCardTransaction", "PxPostDpsBillingTransaction", "PxPostBillingTransaction",
           "PxPostCompleteTransaction", "PxPostRefundTransaction", "PxPostStatusTransaction",]


class PxPostBaseTransaction(txn.BaseTransaction):
    """
    Contains data required by PxPost transactions

    See https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxPost#XMLTxnInput

    """

    # https://www.paymentexpress.com/technical_resources/ecommerce_nonhosted/pxpost.html#Amount
    amount = txn.AmountField(required=True)

    # https://www.paymentexpress.com/technical_resources/ecommerce_nonhosted/pxpost.html#InputCurrency
    input_currency = txn.StringField(choices=txn.CURRENCY_CHOICES, required=True)

    # https://www.paymentexpress.com/technical_resources/ecommerce_nonhosted/pxpost.html#DpsTxnRef
    dps_txn_ref = txn.StringField(max_length=16)

    # https://www.paymentexpress.com/technical_resources/ecommerce_nonhosted/pxpost.html#cardholderName
    card_holder_name = txn.StringField(max_length=64)

    # https://www.paymentexpress.com/technical_resources/ecommerce_nonhosted/pxpost.html#cardnumber
    card_number = txn.StringField(max_length=20)

    # https://www.paymentexpress.com/technical_resources/ecommerce_nonhosted/pxpost.html#dateexpiry
    date_expiry = txn.StringField(pattern=r'(0[1-9]|1[0-2])\d{2}')

    # https://www.paymentexpress.com/technical_resources/ecommerce_nonhosted/pxpost.html#Cvc2
    cvc2 = txn.StringField(max_length=4)

    # https://www.paymentexpress.com/technical_resources/ecommerce_nonhosted/pxpost.html#DpsBillingId
    dps_billing_id = txn.StringField(max_length=16)

    # https://www.paymentexpress.com/technical_resources/ecommerce_nonhosted/pxpost.html#BillingId
    billing_id = txn.StringField(max_length=32)

    # https://www.paymentexpress.com/technical_resources/ecommerce_nonhosted/pxpost.html#Cvc2Presence
    cvc2_presence = txn.IntegerField(choices=txn.CVC2_CHOICES)

    # https://www.paymentexpress.com/technical_resources/ecommerce_nonhosted/pxpost.html#EnableAddBillCard
    enable_add_bill_card = txn.BooleanField()

    # https://www.paymentexpress.com/technical_resources/ecommerce_nonhosted/pxpost.html#MerchantReference
    merchant_reference = txn.StringField(max_length=64)

    # https://www.paymentexpress.com/technical_resources/ecommerce_nonhosted/pxpost.html#txndata
    txn_data1 = txn.StringField(max_length=255)
    txn_data2 = txn.StringField(max_length=255)
    txn_data3 = txn.StringField(max_length=255)

    # https://www.paymentexpress.com/technical_resources/ecommerce_nonhosted/pxpost.html#TxnId
    txn_id = txn.StringField(max_length=16)

    # https://www.paymentexpress.com/technical_resources/ecommerce_nonhosted/pxpost.html#enableAvsData
    enable_avs_data = txn.BooleanField()

    # https://www.paymentexpress.com/technical_resources/ecommerce_nonhosted/pxpost.html#avsAction
    avs_action = txn.IntegerField(choices=txn.AVS_CHOICES)

    # https://www.paymentexpress.com/technical_resources/ecommerce_nonhosted/pxpost.html#avsPostCode
    avs_post_code = txn.StringField(max_length=20)

    # https://www.paymentexpress.com/technical_resources/ecommerce_nonhosted/pxpost.html#avsStreetAddress
    avs_street_address = txn.StringField(max_length=60)

    # https://www.paymentexpress.com/technical_resources/ecommerce_nonhosted/pxpost.html#issueNumber
    issue_number = txn.IntegerField()

    # https://www.paymentexpress.com/technical_resources/ecommerce_nonhosted/pxpost.html#dateStart
    date_start = txn.StringField(pattern=r'(0[1-9]|1[0-2])\d{2}')

    # https://www.paymentexpress.com/technical_resources/ecommerce_nonhosted/pxpost.html#track2
    track2 = txn.StringField(max_length=37)


class PxPostCardTransaction(PxPostBaseTransaction):
    """
    Contains data required by PxPost transactions using a payment card

    """

    # https://www.paymentexpress.com/technical_resources/ecommerce_nonhosted/pxpost.html#cardholderName
    card_holder_name = txn.StringField(max_length=64, required=True)

    # https://www.paymentexpress.com/technical_resources/ecommerce_nonhosted/pxpost.html#cardnumber
    card_number = txn.StringField(max_length=20, required=True)

    # https://www.paymentexpress.com/technical_resources/ecommerce_nonhosted/pxpost.html#dateexpiry
    date_expiry = txn.StringField(pattern=r'(0[1-9]|1[0-2])\d{2}', required=True)

    # https://www.paymentexpress.com/technical_resources/ecommerce_nonhosted/pxpost.html#Cvc2
    cvc2 = txn.StringField(max_length=4, required=True)

    # https://www.paymentexpress.com/technical_resources/ecommerce_nonhosted/pxpost.html#BillingId
    billing_id = txn.StringField(max_length=32)


class PxPostDpsBillingTransaction(PxPostBaseTransaction):
    """
    Contains data required by PxPost transactions using a dps billing token

    """

    # https://www.paymentexpress.com/technical_resources/ecommerce_nonhosted/pxpost.html#DpsBillingId
    dps_billing_id = txn.StringField(max_length=16, required=True)


class PxPostBillingTransaction(PxPostBaseTransaction):
    """
    Contains data required by PxPost transactions using a custom billing token

    """

    # https://www.paymentexpress.com/technical_resources/ecommerce_nonhosted/pxpost.html#BillingId
    billing_id = txn.StringField(max_length=32, required=True)


class PxPostCompleteTransaction(txn.BaseTransaction):
    """
    Contains data required by PxPost transactions using a custom billing token

    """

    # https://www.paymentexpress.com/technical_resources/ecommerce_nonhosted/pxpost.html#DpsTxnRef
    dps_txn_ref = txn.StringField(max_length=16, required=True)

    # https://www.paymentexpress.com/technical_resources/ecommerce_nonhosted/pxpost.html#Amount
    amount = txn.AmountField()

    # https://www.paymentexpress.com/technical_resources/ecommerce_nonhosted/pxpost.html#InputCurrency
    input_currency = txn.StringField(choices=txn.CURRENCY_CHOICES)


class PxPostRefundTransaction(txn.BaseTransaction):
    """
    Contains data required by PxPost refund transactions

    See https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxPost#Refunds

    """

    # https://www.paymentexpress.com/technical_resources/ecommerce_nonhosted/pxpost.html#Amount
    amount = txn.AmountField(required=True)

    # https://www.paymentexpress.com/technical_resources/ecommerce_nonhosted/pxpost.html#DpsTxnRef
    dps_txn_ref = txn.StringField(max_length=16, required=True)

    # https://www.paymentexpress.com/technical_resources/ecommerce_nonhosted/pxpost.html#MerchantReference
    merchant_reference = txn.StringField(max_length=64)


class PxPostStatusTransaction(txn.BaseTransaction):
    """
    Contains data required by PxPost status transactions

    See https://www.paymentexpress.com/technical_resources/ecommerce_nonhosted/pxpost.html#ExceptionHandling

    """

    # https://www.paymentexpress.com/technical_resources/ecommerce_nonhosted/pxpost.html#TxnId
    txn_id = txn.StringField(max_length=16, required=True)
