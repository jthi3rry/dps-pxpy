# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import six
from .fields import BaseField

__all__ = ["BaseTransaction"]


class MetaTransaction(type):

    def __new__(cls, name, bases, attrs):

        class Meta(object):
            _fields = {}
            _required = set()

        # merge fields from bases
        for fields in (base._meta._fields for base in bases if hasattr(base, '_meta')):
            Meta._fields.update(fields)
        # merge fields from attrs
        Meta._fields.update({k: v for k, v in attrs.items() if isinstance(v, BaseField)})

        # merge required fields from bases
        for required in (base._meta._required for base in bases if hasattr(base, '_meta')):
            Meta._required.update(required)
        # merge required fields from fields with the required property
        Meta._required.update(k for k, v in Meta._fields.items() if isinstance(v, BaseField) and v.required)
        # merge required fields from list defined in class' Meta.required
        Meta._required.update(attrs["Meta"].required if 'Meta' in attrs and hasattr(attrs['Meta'], 'required') else [])

        attrs['_meta'] = Meta

        return type.__new__(cls, name, bases, attrs)


class BaseTransaction(six.with_metaclass(MetaTransaction)):
    """
    Base class for DPS Transactions.

    This class allows for easier handling of transaction data sent to DPS while performing field validation.

    """
    def __init__(self, **kwargs):
        """
        Creates a new Transaction object.

        Optionally accepts keyword arguments to populate the transaction's fields.

        """
        for key, val in kwargs.items():
            if key not in self._meta._fields:
                raise ValueError("{0} field does not exist".format(key))
            setattr(self, key, val)

    def validate(self):
        """
        Checks that all required fields are present

        """
        if not all(getattr(self, name) is not None for name in self._meta._required):
            missing = filter(lambda name: getattr(self, name) is None, self._meta._required)
            raise ValueError("Transaction is missing required fields: {}".format(", ".join(missing)))

    def is_valid(self):
        """
        Checks that a transaction is valid

        """
        try:
            self.validate()
            return True
        except ValueError:
            return False

    def __iter__(self):
        """
        Iterator over fields that are not None

        """
        return ((key, getattr(self, key)) for key in self._meta._fields.keys() if getattr(self, key) is not None)
