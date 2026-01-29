# -*- coding: utf-8 -*-
# import io
import os
import random
import sdk_test
from edge2client.constants import OFF

CURPATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


class TestRule(sdk_test.TestSdk):
    def test_cache(self):
        condition = [{'var': 'client-country', 'op': 'eq', 'val': 'CN'}]
        cache_key = ['uri', 'query-string', 'client-city']
        cache_rule = {'cache_key': cache_key}
        rule_id = self.client.new_rule(condition=condition, cache=cache_rule)
        self.assertIs(type(rule_id), int)
        self.assertGreater(rule_id, 0)

        condition[0]['val'] = 'JP'
        cache_key = [
            {'name': "uri", },
            {'name': "client-city"},
            {'name': "client-continent", 'args': 'first-x-forwarded-addr'},
            {'name': "query-string"}
        ]
        default_ttls= [{
            'ttl_unit': "min", 'status': 200, 'ttl': 2
        }, {
            'ttl_unit': "min", 'status': 301, 'ttl': 1
        }]
        cache_rule = {
            'cache_key': cache_key,
            'default_ttls': default_ttls,
            'browser_ttl': 2,
            'browser_ttl_unit': 'min',
            'disable_convert_head': True,
            'enforce_cache': True,
            'cluster_hash': True,
            'enable_global': True,
        }
        ok = self.client.put_rule(rule_id=rule_id, condition=condition,
                                  cache=cache_rule)
        self.assertTrue(ok)

        data = self.client.get_rule(rule_id)
        self.assertEqual(data['cache']['cache_key'][0]['name'], 'uri')
        self.assertEqual(data['cache']['cache_key'][1]['name'], 'client-city')
        self.assertEqual(data['cache']['cache_key'][2]['args'], 'first-x-forwarded-addr')
        self.assertEqual(len(data['cache']['cache_key']), 4)
        self.assertEqual(data['cache']['cluster_hash'], True)
        self.assertEqual(data['cache']['disable_convert_head'], True)
        self.assertEqual(data['cache']['enforce_cache'], True)
        self.assertEqual(data['cache']['enable_global'], True)
        self.assertEqual(data['cache']['browser_ttl'], 2)
        self.assertEqual(data['cache']['browser_ttl_unit'], 'min')
        self.assertEqual(type(data['cache']['default_ttls']), type(list()))
        self.assertEqual(data['conditions'][0]['values'][0]['val'], 'JP')

        # disable default cache
        cache_rule = {
            'cache_key': cache_key,
            'default_ttls': OFF,
            'browser_ttl': OFF,
            'browser_ttl_unit': 'min',
            'disable_convert_head': False,
            'enforce_cache': False,
            'cluster_hash': False,
            'enable_global': False,
        }
        ok = self.client.put_rule(rule_id=rule_id, condition=condition,
                                  cache=cache_rule)
        self.assertTrue(ok)

        data = self.client.get_rule(rule_id)
        self.assertEqual(data['cache'].get('default_ttls',None), None)
        self.assertEqual(data['cache']['cluster_hash'], False)
        self.assertEqual(data['cache']['enforce_cache'], False)
        self.assertEqual(data['cache'].get('browser_ttl',None), None)
        self.assertEqual(data['cache'].get('browser_ttl_unit',None), None)
        self.assertEqual(data['cache']['disable_convert_head'], False)
        self.assertEqual(data['cache']['enable_global'], False)

        ok = self.client.del_rule(rule_id)
        self.assertTrue(ok)

        data = self.client.get_rule(rule_id)
        self.assertEqual(data, {})
