import json

import requests
from odoo.tests import HttpCase


class TestEstatePropertyTagAPI(HttpCase):
	def setUp(self):
		super(TestEstatePropertyTagAPI, self).setUp()
		self.base_url = "http://localhost:8069"
		self.auth_token = "444eb4bd-7f2d-44d0-a88a-8e727bfd973a"
		self.session_id = self.authenticate()

	def authenticate(self):
		url = f'{self.base_url}/web/session/authenticate'
		headers = {'Content-Type': 'application/json'}
		data = {
			"jsonrpc": "2.0",
			"method": "call",
			"id": 1,
			"method": "login",			
			"params": {
				"db": "learn-odoo-technical",
				"login": "admin",
				"password": "admin"
			},
		}

		response = requests.post(url, headers=headers, data=json.dumps(data))

	def test_get_tags(self):
		url = f'{self.base_url}/estate-property-tags'
		headers = {
			'Authorization': self.auth_token,
			'Cookie': f'session_id={self.session_id}'
		}
		response = requests.get(url, headers=headers)
		self.assertEqual(response.status_code, 200)

	def test_get_tag_by_id(self):
		tag_id = 1
		url = f'{self.base_url}/estate-property-tag/{tag_id}'
		headers = {
			'Authorization': self.auth_token,
			'Cookie': f'session_id={self.session_id}'
		}

		response = requests.get(url, headers=headers)
		self.assertEqual(response.status_code, 200)

		expected_response = {
		    "id": 1,
		    "name": "Red",
		    "color": 1
		}
		self.assertEqual(response.json(), expected_response)