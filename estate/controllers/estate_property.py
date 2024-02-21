import json
import requests

from odoo import http
from ..utils.auth_utils import authenticate


class EstateProperty(http.Controller):
	@http.route('/healthcheck', auth='public', methods=['GET', 'POST'])
	def healthcheck(self, **kw):
		return "IT Works"

	@http.route('/xyz', auth='user')
	def xyz(self, **kw):
		return "This is accessible for authenticated user"

	@http.route('/entries', auth='public')
	@authenticate
	def entries(self, **kw):
		response = requests.get("https://api.publicapis.org/entries")
		return json.dumps(response.json())