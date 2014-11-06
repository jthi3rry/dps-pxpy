# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import unittest
from dps import utils


class UtilsTest(unittest.TestCase):

    def test_underscore_keys(self):

        initial = {'TestKeyA': True, 'TestKey1': True, 'TestDictKey': {'TestInnerKey': True}}
        expected = {'test_key_a': True, 'test_key1': True, 'test_dict_key': {'test_inner_key': True}}
        self.assertEquals(utils.underscore_keys(initial), expected)

    def test_underscore_key_post_proc(self):

        self.assertEquals(utils.underscore_keys_postproc(None, 'TestKey', 'value'), ('test_key', 'value'))
        self.assertEquals(utils.underscore_keys_postproc(None, 'TestKey', {'TestInnerKey': True}), ('test_key', {'test_inner_key': True}))

if __name__ == "__main__":
    unittest.main()
