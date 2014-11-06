# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import unittest
import decimal

from dps import transactions as txn


class MockTransaction(txn.BaseTransaction):

    amount = txn.AmountField(required=True)
    currency = txn.StringField(max_length=4, choices=txn.CURRENCY_CHOICES, required=True)
    enable_avs_data = txn.BooleanField(default=False)


class MockSubTransaction(MockTransaction):
    class Meta:
        required = ["enable_avs_data"]


class FieldsTest(unittest.TestCase):

    def test_choices(self):

        class MockObject(object):
            field = txn.StringField(choices=['choice1', 'choice2'])

        o = MockObject()
        o.field = 'choice1'
        o.field = 'choice2'

        with self.assertRaises(ValueError):
            o.field = 'invalid choice'

        o.field = None

    def test_default(self):

        class MockObject(object):
            field = txn.StringField(default='initial')

        o = MockObject()
        self.assertEqual(o.field, 'initial')

        o.field = 'newvalue'
        self.assertEqual(o.field, 'newvalue')

        del o.field
        self.assertEqual(o.field, 'initial')

    def test_instance_owner_isolation(self):

        class MockObject(object):
            field = txn.IntegerField()

        a = MockObject()
        b = MockObject()

        a.field = 1
        self.assertEqual(a.field, 1)
        self.assertIsNone(b.field)

        b.field = 2
        self.assertEqual(a.field, 1)
        self.assertEqual(b.field, 2)

    def test_string_field(self):

        class MockObject(object):
            field = txn.StringField(max_length=5)
            exp = txn.StringField(pattern=r'(0[1-9]|1[0-2])\d{2}')

        o = MockObject()
        o.field = 'short'
        self.assertEqual(o.field, 'short')

        with self.assertRaises(ValueError):
            o.field = 1

        with self.assertRaises(ValueError):
            o.field = 'toolong'

        o.exp = '0122'
        self.assertEqual(o.exp, '0122')
        with self.assertRaises(ValueError):
            o.exp = '1322'

        with self.assertRaises(ValueError):
            o.exp = '0022'

    def test_boolean_field(self):

        class MockObject(object):
            field = txn.BooleanField()

        o = MockObject()
        o.field = True

        self.assertEqual(o.field, True)
        self.assertEqual(str(o.field), '1')

        o.field = False
        self.assertEqual(o.field, False)
        self.assertEqual(str(o.field), '0')

        o.field = None
        self.assertIsNone(o.field, None)

        with self.assertRaises(ValueError):
            o.field = 1

        with self.assertRaises(ValueError):
            o.field = 'nonbool'

    def test_integer_field(self):

        class MockObject(object):
            field = txn.IntegerField()

        o = MockObject()

        o.field = 12345
        self.assertEqual(o.field, 12345)

        o.field = None
        self.assertIsNone(o.field, None)

        with self.assertRaises(ValueError):
            o.field = 'nonint'

    def test_amount_field(self):
        import decimal

        class MockObject(object):
            field = txn.AmountField(decimal_context=decimal.Context(rounding=decimal.ROUND_DOWN))

        o = MockObject()
        o.field = decimal.Decimal('1.105')
        self.assertEqual(o.field, decimal.Decimal('1.10'))
        self.assertEqual(str(o.field), '1.10')

        o.field = 1.105
        self.assertEqual(o.field, decimal.Decimal('1.10'))
        self.assertEqual(str(o.field), '1.10')

        o.field = '1.105'
        self.assertEqual(o.field, decimal.Decimal('1.10'))
        self.assertEqual(str(o.field), '1.10')

        o.field = '1'
        self.assertEqual(o.field, decimal.Decimal('1.00'))
        self.assertEqual(str(o.field), '1.00')

        o.field = None
        self.assertIsNone(o.field, None)

        with self.assertRaises(ValueError):
            o.field = 'invalid'


class TransactionTest(unittest.TestCase):

    def test_init(self):

        txn = MockTransaction(amount='10.123', currency='NZD')
        self.assertEqual(txn.amount, decimal.Decimal('10.12'))
        self.assertEqual(txn.currency, 'NZD')
        self.assertEqual(txn.enable_avs_data, 0)

    def test_invalid_values(self):
        with self.assertRaises(ValueError):
            MockTransaction(amount='10.123', currency='NZD', enable_avs_data='invalid')

    def test_invalid_fields(self):
        with self.assertRaises(ValueError):
            MockTransaction(invalid="invalid")

    def test_validate(self):
        with self.assertRaises(ValueError):
            txn = MockTransaction(amount='10.123')
            txn.validate()

    def test_is_valid(self):
        txn = MockTransaction(amount='10.123')
        self.assertFalse(txn.is_valid())
        txn = MockTransaction(amount='10.123', currency='NZD')
        self.assertTrue(txn.is_valid())

    def test_iterable(self):
        txn = MockTransaction(amount='10.123', currency='NZD')
        self.assertDictEqual(dict(txn), {'amount': decimal.Decimal('10.12'), 'currency': 'NZD', 'enable_avs_data': False})

    def test_transactions_subclasses_inherit_fields(self):
        txn = MockSubTransaction(amount='10.123', currency='NZD', enable_avs_data=True)
        self.assertEqual(txn.amount, decimal.Decimal('10.12'))
        self.assertEqual(txn.currency, 'NZD')
        self.assertEqual(txn.enable_avs_data, True)

    def test_validate_with_meta_required(self):
        with self.assertRaises(ValueError):
            txn = MockSubTransaction(amount='10.123', currency='NZD', enable_avs_data=None)
            txn.validate()


class DecoratorsTest(unittest.TestCase):

    def setUp(self):
        class Client(object):
            @txn.accept_txn(MockTransaction)
            def test(self, **kwargs):
                return kwargs
        self.client = Client()

    def test_call_with_transaction(self):
        self.assertDictEqual({"amount": decimal.Decimal("10.01"), "currency": "NZD", "enable_avs_data": False},
                             self.client.test(MockTransaction(amount=decimal.Decimal("10.01"), currency="NZD")))

    def test_call_with_invalid_transaction(self):
        class InvalidTransaction(txn.BaseTransaction):
            pass

        with self.assertRaises(ValueError):
            self.client.test(InvalidTransaction())

    def test_call_with_kwargs_matching_transaction(self):
        self.assertDictEqual({"amount": decimal.Decimal("10.01"), "currency": "NZD", "enable_avs_data": False},
                             self.client.test(amount=decimal.Decimal("10.01"), currency="NZD", enable_avs_data=False))

    def test_call_with_kwargs_not_matching_transaction(self):
        with self.assertRaises(ValueError):
            self.client.test(amount=decimal.Decimal("10.01"))

    def test_call_with_invalid_args(self):
        with self.assertRaises(ValueError):
            self.client.test()

if __name__ == "__main__":
    unittest.main()
