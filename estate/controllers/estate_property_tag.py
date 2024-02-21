import json

from odoo import http
from odoo.http import request, Response

from ..utils.auth_utils import authenticate

class EstatePropertyTagController(http.Controller):
	@http.route('/estate-property-tags', auth="public", methods=['GET'])
	@authenticate
	def get_property_tags(self, **kwargs):
		tags = request.env['estate.property.tag'].search([])

		property_tags = []
		for tag in tags:
			property_tags.append({
				'id': tag.id,
				'name': tag.name,
				'color': tag.color
			})

		return Response(json.dumps(property_tags), content_type="application/json")