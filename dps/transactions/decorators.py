# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import functools


def accept_txn(*types):
    """
    Checks first argument against a list of valid types. Use kwargs otherwise.

    """
    def decorator(f):
        @functools.wraps(f)
        def wrapper(self, transaction=None, **kwargs):
            if transaction:
                if isinstance(transaction, types):
                    transaction.validate()
                    return f(self, **dict(transaction))
                raise ValueError("Invalid transaction type. (got: {}, expects: {})".format(transaction.__class__.__name__, ", ".join((cls.__name__ for cls in types))))
            elif kwargs:
                if any(txn_class(**kwargs).is_valid() for txn_class in types):
                    return f(self, **kwargs)
                raise ValueError("Invalid kwargs for transaction types: {}".format(", ".join((cls.__name__ for cls in types))))
            raise ValueError("Expects either a transaction or kwargs")
        return wrapper
    return decorator
