# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import unittest
import decimal
from mock import Mock, patch, call
from dps.pxfusion import PxFusionClient, PxFusionGetTransaction, PxFusionStatusTransaction, PxFusionCancelTransaction


class PxFusionTest(unittest.TestCase):

    @patch('dps.pxfusion.client.SOAPClient')
    def setUp(self, mock_soap):
        self.client = PxFusionClient('username', 'password')

    def tearDown(self):
        pass

    def test_credentials(self):
        self.assertEqual(self.client.username, 'username')
        self.assertEqual(self.client.password, 'password')

    def test_create_transaction_details(self):
        mock_create = self.client.soap_client.factory.create
        mock_create.return_value = dict()
        result = self.client.create_transaction_details(amount='10.01', merchant_reference='reference')
        expected = {'amount': '10.01', 'merchantReference': 'reference'}
        self.assertEqual(result, expected)
        self.assertTrue(mock_create.called)
        self.assertEqual(mock_create.call_count, 1)
        self.assertEqual(mock_create.call_args, call('TransactionDetails'))

    def test_get_transaction_id(self):
        expected = {'success': True, 'transaction_id': 'txnid', 'session_id': 'txnid'}
        mock_get_id = self.client.soap_client.service.GetTransactionId
        mock_get_id.return_value = expected
        self.client.soap_client.factory.create = mock_create = Mock()
        mock_create.return_value = dict()
        result = self.client.get_transaction_id(test_arg='test')
        self.assertEqual(result, expected)
        self.assertTrue(mock_get_id.called)
        self.assertEqual(mock_get_id.call_count, 1)
        self.assertEqual(mock_get_id.call_args, call('username', 'password', {'testArg': 'test'}))

    def test_get_transaction(self):
        expected = {'response_text': 'success', 'txn_id': 'txnid'}
        mock_get = self.client.soap_client.service.GetTransaction
        mock_get.return_value = expected
        result = self.client.get_transaction(transaction_id='txnid')
        self.assertEqual(result, expected)
        self.assertTrue(mock_get.called)
        self.assertEqual(mock_get.call_count, 1)
        self.assertEqual(mock_get.call_args, call('username', 'password', 'txnid'))

    def test_cancel_transaction(self):
        expected = {'response_text': 'success', 'txn_id': 'txnid'}
        mock_cancel = self.client.soap_client.service.CancelTransaction
        mock_cancel.return_value = expected
        result = self.client.cancel_transaction(transaction_id='txnid')
        self.assertEqual(result, expected)
        self.assertTrue(mock_cancel.called)
        self.assertEqual(mock_cancel.call_count, 1)
        self.assertEqual(mock_cancel.call_args, call('username', 'password', 'txnid'))

    def test_authorize(self):
        self.client.get_transaction_id = Mock()
        self.client.authorize(PxFusionGetTransaction(amount='10.01', currency='NZD', return_url='https://example.org', txn_ref='ref'))
        self.assertTrue(self.client.get_transaction_id.called)
        self.assertEqual(self.client.get_transaction_id.call_args, call(txn_type='Auth', currency='NZD', amount=decimal.Decimal('10.01'), txn_ref='ref', return_url='https://example.org'))
        self.assertEqual(self.client.get_transaction_id.call_count, 1)

    def test_purchase(self):
        self.client.get_transaction_id = Mock()
        self.client.purchase(amount=decimal.Decimal('10.01'), currency='NZD', return_url='https://example.org', txn_ref='ref')
        self.assertTrue(self.client.get_transaction_id.called)
        self.assertEqual(self.client.get_transaction_id.call_args, call(txn_type='Purchase', currency='NZD', amount=decimal.Decimal('10.01'), txn_ref='ref', return_url='https://example.org'))
        self.assertEqual(self.client.get_transaction_id.call_count, 1)

    def test_status(self):
        self.client.get_transaction = Mock()
        self.client.status(PxFusionStatusTransaction(transaction_id='ref'))
        self.assertTrue(self.client.get_transaction.called)
        self.assertEqual(self.client.get_transaction.call_args, call(transaction_id='ref'))
        self.assertEqual(self.client.get_transaction.call_count, 1)

    def test_cancel(self):
        self.client.cancel_transaction = Mock()
        self.client.cancel(PxFusionCancelTransaction(transaction_id='ref'))
        self.assertTrue(self.client.cancel_transaction.called)
        self.assertEqual(self.client.cancel_transaction.call_args, call(transaction_id='ref'))
        self.assertEqual(self.client.cancel_transaction.call_count, 1)

    def test_authorize_with_kwargs(self):
        self.client.get_transaction_id = Mock()
        self.client.authorize(amount=decimal.Decimal('10.01'), currency='NZD', return_url='https://example.org', txn_ref='ref')
        self.assertEqual(self.client.get_transaction_id.call_args, call(txn_type='Auth', currency='NZD', amount=decimal.Decimal('10.01'), txn_ref='ref', return_url='https://example.org'))

    def test_purchase_with_kwargs(self):
        self.client.get_transaction_id = Mock()
        self.client.purchase(amount=decimal.Decimal('10.01'), currency='NZD', return_url='https://example.org', txn_ref='ref')
        self.assertEqual(self.client.get_transaction_id.call_args, call(txn_type='Purchase', currency='NZD', amount=decimal.Decimal('10.01'), txn_ref='ref', return_url='https://example.org'))

    def test_status_with_kwargs(self):
        self.client.get_transaction = Mock()
        self.client.status(transaction_id='ref')
        self.assertEqual(self.client.get_transaction.call_args, call(transaction_id='ref'))

    def test_cancel_with_kwargs(self):
        self.client.cancel_transaction = Mock()
        self.client.cancel(transaction_id='ref')
        self.assertEqual(self.client.cancel_transaction.call_args, call(transaction_id='ref'))

if __name__ == "__main__":
    unittest.main()
