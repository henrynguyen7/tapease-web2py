"""
To run this test: "python web2py.py -S tapease -M -R applications/tapease/tests/test.py"

More info: http://www.web2py.com/AlterEgo/default/show/260
"""

import json
import unittest
import time
import requests

from gluon.globals import Request

BASE_URL = 'http://127.0.0.1:8000/tapease/default'
ENDPOINT_USER = BASE_URL + '/user'
ENDPOINT_ORG = BASE_URL + '/org'
ENDPOINT_MEMBERSHIP = BASE_URL + '/membership'
ENDPOINT_TAP = BASE_URL + '/tap'

EMAIL = 'test@test.com'
PASSWORD = 'testtest'
ORG_NAME = 'tapease'

s = requests.Session()


class TestTapease(unittest.TestCase):
    USER_ID = None
    ORG_ID = None
    TAP_ID = None

    """
    User
    """
    def test_01_post_user(self):
        data = {'email': EMAIL, 'password': PASSWORD }
        resp = s.post(ENDPOINT_USER, data=data)
        self.assertEqual(resp.status_code, 200)
        self.__class__.USER_ID = resp.json()['id']

    def test_02_get_user(self):
        data = {'email': EMAIL, 'password': PASSWORD }
        resp = s.get(ENDPOINT_USER, params=data)
        self.assertEqual(resp.status_code, 200)

    def test_03_put_user(self):
        data = {
            'name': 'Test User',
            'image_url': 'www.tapease.com/image_user',
            'is_enabled': 'true',
        }
        resp = s.put(ENDPOINT_USER, data=data)
        self.assertEqual(resp.status_code, 200)

    """
    Org
    """
    def test_04_post_org(self):
        timestamp = int(time.time())
        data = { 'name': ORG_NAME + str(timestamp) }
        resp = s.post(ENDPOINT_ORG, data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.json()['id'])
        self.__class__.ORG_ID = resp.json()['id']

    def test_05_get_org(self):
        resp = s.get(ENDPOINT_ORG)
        self.assertEqual(resp.status_code, 200)

    def test_06_put_org(self):
        timestamp = int(time.time())
        data = {
            'name': 'Tapease' + str(timestamp),
            'url': 'www.tapease.com',
            'image_url': 'www.tapease.com/image_org',
        }
        resp = s.put(ENDPOINT_ORG, data=data)
        self.assertEqual(resp.status_code, 200)

    """
    Membership
    """
    def test_07_post_membership(self):
        data = { 'org_id': self.__class__.ORG_ID }
        resp = s.post(ENDPOINT_MEMBERSHIP, data=data)
        self.assertEqual(resp.status_code, 200)

    def test_08_get_membership(self):
        resp = s.get(ENDPOINT_ORG)
        self.assertEqual(resp.status_code, 200)

    """
    Tap
    """
    def test_09_post_tap(self):
        data = {
            'org_id': self.__class__.ORG_ID,
            'page_uid': 'test_page_uid',
            'page_token': 'test_page_token',
            'element_route': 'test_element_route',
            'element_node': 'test_element_node',
            'comment': 'test_comment',
        }
        resp = s.post(ENDPOINT_TAP, data=data)
        self.assertEqual(resp.status_code, 200)
        self.__class__.TAP_ID = resp.json()['id']

    def test_10_get_tap(self):
        resp = s.get(ENDPOINT_TAP)
        self.assertEqual(resp.status_code, 200)

    def test_11_put_tap(self):
        data = { 'id': self.__class__.TAP_ID, 'comment': 'test comment' }
        resp = s.put(ENDPOINT_TAP, data=data)
        self.assertEqual(resp.status_code, 200)

    """
        Delete
    """
    def test_12_delete_tap(self):
        data = { 'id': self.__class__.TAP_ID }
        resp = s.put(ENDPOINT_TAP, data=data)
        self.assertEqual(resp.status_code, 200)

    def test_13_delete_membership(self):
        timestamp = int(time.time())
        data = { 'user_id': self.__class__.USER_ID, 'org_id': self.__class__.ORG_ID }
        resp = s.delete(ENDPOINT_MEMBERSHIP, data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['success'], True)

    def test_14_delete_org(self):
        data = { 'id': self.__class__.ORG_ID }
        resp = s.delete(ENDPOINT_ORG, data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['success'], True)

    def test_15_delete_user(self):
        resp = s.delete(ENDPOINT_USER)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['success'], True)


suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestTapease))
unittest.TextTestRunner(verbosity=1).run(suite)