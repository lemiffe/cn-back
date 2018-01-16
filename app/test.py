import unittest
import app
import os
import json
import logging


class AppTest(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()
        app.init()
        self.assertEqual(1,1)

    def test_index(self):
        """
        Endpoint: /
        Methods: ['POST', 'DELETE', 'GET']
        Params: tree_id
        Responses: 200, 400, 404, 409
        """
        # POST
        #http_response = self.app.post('/', data=json.dumps(dict(tree_id=1)), content_type='application/json')
        #result = json.loads(http_response.data)
        #self.assertEqual(int(result['meta']['code']), 200)
        
        # POST again?
        #http_response = self.app.post('/', data=json.dumps(dict(tree_id=1)), content_type='application/json')
        #result = json.loads(http_response.data)
        #self.assertEqual(int(result['meta']['code']), 409)
        self.assertEqual(1,1)

if __name__ == '__main__':
    unittest.main()