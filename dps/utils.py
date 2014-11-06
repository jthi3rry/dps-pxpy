# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from .vendors.inflection import underscore


def underscore_keys(dictionary):
    """
    Convert all keys in dictionary to their underscored form.

    Example:
      {'TestKeyA': 123, 'TestKeyB': 456} is transformed into {'test_key_a': 123, 'test_key_b': 456}
    """
    result = {}
    for k, v in dictionary.items():
        if isinstance(v, dict):
            result[underscore(k)] = underscore_keys(v)
        else:
            result[underscore(k)] = v
    return result


def underscore_keys_postproc(_, key, value):
    """
    Convert a key/value pair into a tuple with the key in underscored form.

    Note:
      If value is a dictionary, its keys will also be converted into underscored form.
    """
    if not isinstance(value, dict):
        return underscore(key), value
    else:
        return underscore(key), underscore_keys(value)
