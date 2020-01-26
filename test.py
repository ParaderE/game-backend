import unittest
import json

from api import app


class LoginTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
    
    def test_server_is_up_and_running(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_create_account_and_check_for_free(self):
        res = self.app.post('/register/', json={"account": "test test"})
        json_res = res.json
        self.assertTrue(json_res['is_free'])
        json_res = self.app.post('/register/', json={'account': "test test"}).json
        self.assertFalse(json_res['is_free'])
    
    def test_enter(self):
        self.app.post('/register/', json={"account": "test test"})
        res = self.app.post('/enter/', json={"account": "test test"}).json['location']
        self.assertEqual(res['num'], 4)
        self.assertEqual(res['coords'], [200, 200])
        self.app.post('/register/', json={"account": "test test1"})
        res = self.app.post('/enter/', json={"account": "test test1"}).json['location']
        self.assertEqual(res['num'], 4)
        self.assertEqual(res['coords'], [200, 200])
    
    def test_exit(self):
        payload = {
            'account': 'test test',
            'location': {
                'num': 1,
                'coords': [100, 100]
            }
        }
        self.app.post('/exit/', json=payload)
        res = self.app.post('/enter/', json={"account": "test test"}).json['location']
        self.assertEqual(res['num'], 1)
        self.assertEqual(res['coords'], [100, 100])



if __name__ == "__main__":
    unittest.main()