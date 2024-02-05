from odoo import http


class EstateProperty(http.Controller):
	@http.route('/healthcheck', auth='public', methods=['GET', 'POST'])
	def healthcheck(self, **kw):
		return "IT Works"

	@http.route('/xyz', auth='user')
	def xyz(self, **kw):
		return "This is accessible for authenticated user"