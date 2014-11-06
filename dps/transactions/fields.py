# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import re
import six
import decimal
from weakref import WeakKeyDictionary


__all__ = ["StringField", "BooleanField", "IntegerField", "AmountField"]


class BaseField(object):
    """
    Base class for all fields.

    """
    def __init__(self, default=None, choices=None, required=False):
        self.data = WeakKeyDictionary()
        self.choices = choices
        self.required = required
        if default is not None:
            self.validate(default)
        self.default = default

    def validate(self, value):
        """
        Default field validator.

        Checks whether the field's value is valid for the field type

        """
        if isinstance(self.choices, (list, tuple)) and value not in self.choices and value is not None:
            raise ValueError("{} not a choice in {}".format(value, self.choices))

    def __get__(self, instance, owner):
        """
        Field descriptor __get__ method.

        """
        return self.data.get(instance, self.default)

    def __set__(self, instance, value):
        """
        Field descriptor __set__ method.

        """
        self.validate(value)
        self.data[instance] = value

    def __delete__(self, instance):
        """
        Field descriptor __delete__ method.

        """
        del self.data[instance]


class StringField(BaseField):
    """
    Field that handles string values.

    """

    def __init__(self, max_length=None, pattern=None, **kwargs):
        """
        Creates a String field with optional max_length

        """
        self.max_length = max_length
        self.pattern = pattern
        super(StringField, self).__init__(**kwargs)

    def validate(self, value):
        """
        String field validator.

        """
        super(StringField, self).validate(value)

        if value is None:
            return

        if not isinstance(value, six.string_types):
            raise ValueError('{} is not a string'.format(repr(value)))

        if self.max_length and len(value) > self.max_length:
            raise ValueError("{} is too long (max length is {})".format(value, self.max_length))

        if self.pattern and not re.match(self.pattern, value):
            raise ValueError("{} does not match pattern {}".format(value, self.pattern))


class BooleanField(BaseField):
    """
    Field that handles boolean values.

    """

    def validate(self, value):
        """
        Boolean field validator.

        """
        super(BooleanField, self).validate(value)

        if value is None:
            return

        if not isinstance(value, bool):
            raise ValueError('{} is not a boolean'.format(repr(value)))

    def __get__(self, instance, owner):
        """
        __get__ returns 0 or 1

        """

        try:
            return int(super(BooleanField, self).__get__(instance, owner))
        except:
            return None


class IntegerField(BaseField):
    """
    Field that handles integer values.

    """

    def validate(self, value):
        """
        Integer field validator.

        """
        super(IntegerField, self).validate(value)

        if value is None:
            return

        if not isinstance(value, int):
            raise ValueError('{} is not an integer'.format(repr(value)))


class AmountField(BaseField):
    """
    Field that handles amount values.

    """

    # Quantize mask (0.01)
    TWOPLACES = decimal.Decimal(10) ** -2

    def __init__(self, decimal_context=None, **kwargs):
        """
        Creates an Amount field with optional decimal_context

        """
        self.decimal_context = decimal_context or decimal.Context()
        super(AmountField, self).__init__(**kwargs)

    def validate(self, value):
        """
        Amount field validator.

        """
        super(AmountField, self).validate(value)

        if value is None:
            return

        if not isinstance(value, decimal.Decimal):
            raise ValueError('{} is not a decimal'.format(repr(value)))

    def __get__(self, instance, owner):
        """
        __get__ returns a Decimal quantized to 2 decimal places
        """
        try:
            return super(AmountField, self).__get__(instance, owner).quantize(self.TWOPLACES, context=self.decimal_context)
        except:
            return None

    def __set__(self, instance, value):
        """
        __set__ ensures that the internal value is stored as a Decimal

        """
        try:
            value = decimal.Decimal(str(value))  # Convert to str first to accommodate py26
        except:
            pass
        super(AmountField, self).__set__(instance, value)
