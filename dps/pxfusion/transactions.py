# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from .. import transactions as txn

__all__ = ["PxFusionGetTransaction", "PxFusionCancelTransaction", "PxFusionStatusTransaction"]


class PxFusionGetTransaction(txn.BaseTransaction):
    """
    Contains data required by PxFusion GetTransactionId

    See https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxFusion#GetTransactionId

    """

    # https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxFusion#amount
    amount = txn.AmountField(required=True)

    # https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxFusion#Currency
    currency = txn.StringField(choices=txn.CURRENCY_CHOICES, required=True)

    # https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxFusion#ReturnUrl
    return_url = txn.StringField(max_length=255, required=True)

    # https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxFusion#txnref
    txn_ref = txn.StringField(max_length=16, required=True)

    # https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxFusion#enableaddbillcard
    enable_add_bill_card = txn.BooleanField()

    # https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxFusion#avsAction
    avs_action = txn.IntegerField(choices=txn.AVS_CHOICES)

    # https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxFusion#avsPostCode
    avs_post_code = txn.StringField(max_length=20)

    # https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxFusion#avsStreetAddress
    avs_street_address = txn.StringField(max_length=60)

    # https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxFusion#billingid
    billing_id = txn.StringField(max_length=32)

    # https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxFusion#dateStart
    date_start = txn.StringField(pattern=r'(0[1-9]|1[0-2])\d{2}')

    # https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxFusion#enableAvsData
    enable_avs_data = txn.BooleanField()

    # https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxFusion#EnablePaxInfo
    enable_pax_info = txn.BooleanField()

    # https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxFusion#merchantreference
    merchant_reference = txn.StringField(max_length=64)

    # https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxFusion#PaxCarrier
    pax_carrier = txn.StringField(max_length=2)
    pax_carrier_2 = txn.StringField(max_length=2)
    pax_carrier_3 = txn.StringField(max_length=2)
    pax_carrier_4 = txn.StringField(max_length=2)

    # https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxFusion#PaxClass
    pax_class_1 = txn.StringField(max_length=1)
    pax_class_2 = txn.StringField(max_length=1)
    pax_class_3 = txn.StringField(max_length=1)
    pax_class_4 = txn.StringField(max_length=1)

    # https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxFusion#PaxDate
    pax_date2 = txn.StringField(max_length=20)
    pax_date3 = txn.StringField(max_length=20)
    pax_date4 = txn.StringField(max_length=20)

    # https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxFusion#PaxDateDepart
    pax_date_depart = txn.StringField(pattern=r'\d{4}(0[1-9]|1[1-2])([0-2][1-9]|3[01])')

    # https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxFusion#PaxFareBasis
    pax_fare_basis1 = txn.StringField(max_length=6)
    pax_fare_basis2 = txn.StringField(max_length=6)
    pax_fare_basis3 = txn.StringField(max_length=6)
    pax_fare_basis4 = txn.StringField(max_length=6)

    # https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxFusion#PaxFlightNumber
    pax_flight_number1 = txn.StringField(max_length=6)
    pax_flight_number2 = txn.StringField(max_length=6)
    pax_flight_number3 = txn.StringField(max_length=6)
    pax_flight_number4 = txn.StringField(max_length=6)

    # https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxFusion#PaxLeg
    pax_leg1 = txn.StringField(max_length=3)
    pax_leg2 = txn.StringField(max_length=3)
    pax_leg3 = txn.StringField(max_length=3)
    pax_leg4 = txn.StringField(max_length=3)

    # https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxFusion#PaxName
    pax_name = txn.StringField(max_length=20)

    # https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxFusion#PaxOrigin
    pax_origin = txn.StringField(max_length=3)

    # https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxFusion#PaxStopOverCode
    pax_stop_over_code1 = txn.StringField(max_length=1)
    pax_stop_over_code2 = txn.StringField(max_length=1)
    pax_stop_over_code3 = txn.StringField(max_length=1)
    pax_stop_over_code4 = txn.StringField(max_length=1)

    # https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxFusion#PaxTicketNumber
    pax_ticket_number = txn.StringField(max_length=10)

    # https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxFusion#PaxTime
    pax_time1 = txn.StringField(max_length=4)
    pax_time2 = txn.StringField(max_length=4)
    pax_time3 = txn.StringField(max_length=4)
    pax_time4 = txn.StringField(max_length=4)

    # https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxFusion#PaxTravelAgentInfo
    pax_travel_agent_info = txn.StringField(max_length=25)

    # https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxFusion#txndata
    txn_data1 = txn.StringField(max_length=255)
    txn_data2 = txn.StringField(max_length=255)
    txn_data3 = txn.StringField(max_length=255)


class PxFusionCancelTransaction(txn.BaseTransaction):
    """
    Contains data required by PxFusion CancelTransaction

    See https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxFusion#CancelTransaction

    """

    # https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxFusion#transactionId
    transaction_id = txn.StringField(max_length=32, required=True)


class PxFusionStatusTransaction(txn.BaseTransaction):
    """
    Contains data required by PxFusion GetTransaction

    See https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxFusion#GetTransaction

    """

    # https://www.paymentexpress.com/Technical_Resources/Ecommerce_NonHosted/PxFusion#transactionId
    transaction_id = txn.StringField(max_length=32, required=True)
