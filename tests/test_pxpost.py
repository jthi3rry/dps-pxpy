# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import unittest
import decimal
from mock import Mock, patch, call
from dps.pxpost import PxPostClient, PxPostCardTransaction, PxPostBillingTransaction, PxPostDpsBillingTransaction, PxPostCompleteTransaction, PxPostStatusTransaction, PxPostRefundTransaction
from dps.pxpost.client import PxRequest, PxResponse


class PxPostTest(unittest.TestCase):

    def setUp(self):
        self.client = PxPostClient('username', 'password')

    def tearDown(self):
        pass

    def test_request(self):
        req = PxRequest('RootTag', test_key='value')
        expected = '<?xml version="1.0" ?><RootTag><TestKey>value</TestKey></RootTag>'
        self.assertEquals(req.to_xml(), expected)

    def test_response(self):
        res = PxResponse('<?xml version="1.0" ?><RootTag><TestKey>value</TestKey></RootTag>')
        expected = {'test_key': 'value'}
        self.assertEquals(res.to_dict(), expected)

    def test_credentials(self):
        self.assertEquals(self.client.username, 'username')
        self.assertEquals(self.client.password, 'password')

    @patch('dps.pxpost.client.requests')
    def test_post(self, mock_requests):
        mock_requests.post.return_value = mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = '<?xml version="1.0" ?><Txn><TestKey>value</TestKey></Txn>'
        self.assertEqual(self.client.post(txn_type='authorize', test_key='value'), {'test_key': 'value'})

    def test_authorize_with_card(self):
        self.client.post = Mock()
        self.client.authorize(PxPostCardTransaction(amount=decimal.Decimal('10.01'), input_currency='NZD', card_number='4111111111111111', card_holder_name='Holder Name', date_expiry='1114', cvc2='123'))
        self.assertTrue(self.client.post.called)
        self.assertEquals(self.client.post.call_args, call(txn_type='Auth', amount=decimal.Decimal('10.01'), input_currency='NZD', card_number='4111111111111111', card_holder_name='Holder Name', date_expiry='1114', cvc2='123'))
        self.assertEquals(self.client.post.call_count, 1)

    def test_authorize_with_dps_billing_token(self):
        self.client.post = Mock()
        self.client.authorize(PxPostDpsBillingTransaction(amount=decimal.Decimal('10.01'), input_currency='NZD', dps_billing_id='BILLINGID'))
        self.assertTrue(self.client.post.called)
        self.assertEquals(self.client.post.call_args, call(txn_type='Auth', amount=decimal.Decimal('10.01'), input_currency='NZD', dps_billing_id='BILLINGID'))
        self.assertEquals(self.client.post.call_count, 1)

    def test_authorize_with_custom_billing_token(self):
        self.client.post = Mock()
        self.client.authorize(PxPostBillingTransaction(amount=decimal.Decimal('10.01'), input_currency='NZD', billing_id='BILLINGID'))
        self.assertTrue(self.client.post.called)
        self.assertEquals(self.client.post.call_args, call(txn_type='Auth', amount=decimal.Decimal('10.01'), input_currency='NZD', billing_id='BILLINGID'))
        self.assertEquals(self.client.post.call_count, 1)

    def test_purchase_with_card(self):
        self.client.post = Mock()
        self.client.purchase(PxPostCardTransaction(amount=decimal.Decimal('10.01'), input_currency='NZD', card_number='4111111111111111', card_holder_name='Holder Name', date_expiry='1114', cvc2='123'))
        self.assertTrue(self.client.post.called)
        self.assertEquals(self.client.post.call_args, call(txn_type='Purchase', amount=decimal.Decimal('10.01'), input_currency='NZD', card_number='4111111111111111', card_holder_name='Holder Name', date_expiry='1114', cvc2='123'))
        self.assertEquals(self.client.post.call_count, 1)

    def test_purchase_with_dps_billing_token(self):
        self.client.post = Mock()
        self.client.purchase(PxPostDpsBillingTransaction(amount=decimal.Decimal('10.01'), input_currency='NZD', dps_billing_id='BILLINGID'))
        self.assertTrue(self.client.post.called)
        self.assertEquals(self.client.post.call_args, call(txn_type='Purchase', amount=decimal.Decimal('10.01'), input_currency='NZD', dps_billing_id='BILLINGID'))
        self.assertEquals(self.client.post.call_count, 1)

    def test_purchase_with_billing_token(self):
        self.client.post = Mock()
        self.client.purchase(PxPostBillingTransaction(amount=decimal.Decimal('10.01'), input_currency='NZD', billing_id='BILLINGID'))
        self.assertTrue(self.client.post.called)
        self.assertEquals(self.client.post.call_args, call(txn_type='Purchase', amount=decimal.Decimal('10.01'), input_currency='NZD', billing_id='BILLINGID'))
        self.assertEquals(self.client.post.call_count, 1)

    def test_complete(self):
        self.client.post = Mock()
        self.client.complete(PxPostCompleteTransaction(dps_txn_ref='REFERENCE', amount=decimal.Decimal('10.01')))
        self.assertTrue(self.client.post.called)
        self.assertEquals(self.client.post.call_args, call(txn_type='Complete', dps_txn_ref='REFERENCE', amount=decimal.Decimal('10.01')))
        self.assertEquals(self.client.post.call_count, 1)
#
    def test_refund(self):
        self.client.post = Mock()
        self.client.refund(PxPostRefundTransaction(dps_txn_ref='REFERENCE', amount=decimal.Decimal('10.01')))
        self.assertTrue(self.client.post.called)
        self.assertEquals(self.client.post.call_args, call(txn_type='Refund', dps_txn_ref='REFERENCE', amount=decimal.Decimal('10.01')))

    def test_validate(self):
        self.client.post = Mock()
        self.client.validate(PxPostCardTransaction(amount=decimal.Decimal('10.01'), input_currency='NZD', card_number='4111111111111111', card_holder_name='Holder Name', date_expiry='1114', cvc2='123'))
        self.assertTrue(self.client.post.called)
        self.assertEquals(self.client.post.call_args, call(txn_type='Validate', amount=decimal.Decimal('10.01'), input_currency='NZD', card_number='4111111111111111', card_holder_name='Holder Name', date_expiry='1114', cvc2='123'))
        self.assertEquals(self.client.post.call_count, 1)

    def test_status(self):
        self.client.post = Mock()
        self.client.status(PxPostStatusTransaction(txn_id='TXNID'))
        self.assertTrue(self.client.post.called)
        self.assertEquals(self.client.post.call_args, call(txn_type='Status', txn_id='TXNID'))
        self.assertEquals(self.client.post.call_count, 1)

    def test_authorize_with_kwargs(self):
        self.client.post = Mock()
        self.client.authorize(amount=decimal.Decimal('10.01'), input_currency='NZD', dps_billing_id='BILLINGID')
        self.assertEquals(self.client.post.call_args, call(txn_type='Auth', input_currency='NZD', amount=decimal.Decimal('10.01'), dps_billing_id='BILLINGID'))

    def test_complete_with_kwargs(self):
        self.client.post = Mock()
        self.client.complete(amount=decimal.Decimal('10.01'), input_currency='NZD', dps_txn_ref='TXNREF')
        self.assertEquals(self.client.post.call_args, call(txn_type='Complete', input_currency='NZD', amount=decimal.Decimal('10.01'), dps_txn_ref='TXNREF'))

    def test_purchase_with_kwargs(self):
        self.client.post = Mock()
        self.client.purchase(amount=decimal.Decimal('10.01'), input_currency='NZD', dps_billing_id='BILLINGID')
        self.assertEquals(self.client.post.call_args, call(txn_type='Purchase', input_currency='NZD', amount=decimal.Decimal('10.01'), dps_billing_id='BILLINGID'))

    def test_refund_with_kwargs(self):
        self.client.post = Mock()
        self.client.refund(amount=decimal.Decimal('10.01'), dps_txn_ref='TXNREF')
        self.assertEquals(self.client.post.call_args, call(txn_type='Refund', amount=decimal.Decimal('10.01'), dps_txn_ref='TXNREF'))

    def test_validate_with_kwargs(self):
        self.client.post = Mock()
        self.client.validate(amount=decimal.Decimal('10.01'), input_currency='NZD', card_number='4111111111111111', card_holder_name='Holder Name', date_expiry='1214', cvc2='123')
        self.assertEquals(self.client.post.call_args, call(txn_type='Validate', cvc2='123', date_expiry='1214', input_currency='NZD', amount=decimal.Decimal('10.01'), card_number='4111111111111111', card_holder_name='Holder Name'))

    def test_status_with_kwargs(self):
        self.client.post = Mock()
        self.client.status(txn_id='TXNID')
        self.assertEquals(self.client.post.call_args, call(txn_type='Status', txn_id='TXNID'))


if __name__ == "__main__":
    unittest.main()
