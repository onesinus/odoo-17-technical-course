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

	@http.route('/estate-property-tag/<int:tag_id>', auth="public", methods=['GET'])
	@authenticate
	def get_property_tag_by_id(self, tag_id, **kwargs):
		try:
			tag = request.env['estate.property.tag'].browse(tag_id)

			response_data = {
				'id': tag.id,
				'name': tag.name,
				'color': tag.color
			}

			return Response(json.dumps(response_data), content_type="application/json")
		except Exception as e:
			return Response(json.dumps({'error': 'something went wrong', 'error_detail': str(e)}), status=500)

	@http.route('/estate-property-tag', auth="public", methods=['POST'], csrf=False)
	@authenticate
	def create_tag(self, **kwargs):
		try:
			request_data = json.loads(request.httprequest.data.decode("utf-8"))

			name = request_data.get('name')
			color = int(request_data.get('color'))

			if not all([name, color]):
				return Response("Bad Request: name and color are required", status=400)

			check_tag_exist = request.env['estate.property.tag'].search([('name', '=', name)])
			if check_tag_exist:
				return Response(f"Tag with this name ({name}) is already exist!", status=400)

			tag = request.env['estate.property.tag'].create({
				'name': name,
				'color': color
			})

			response = json.dumps({'id': tag.id, 'name': name, 'color': color})
			return Response(response, content_type="application/json", status=201)

		except Exception as e:
			return Response(f"There is error occured: {str(e)}", status=500)

	@http.route('/estate-property-tag/<int:tag_id>', auth="public", methods=['PUT'], csrf=False)
	@authenticate
	def update_tag(self, tag_id, **kwargs):
		try:
			tag = request.env['estate.property.tag'].browse(tag_id)

			updated_data = json.loads(request.httprequest.data.decode("utf-8"))
			
			name = updated_data.get('name')
			color = int(updated_data.get('color'))

			tag.write({
				'name': name,
				'color': color
			})

			response = json.dumps({'id': tag.id, 'name': name, 'color': color})
			return Response(response, content_type="application/json")
		except Exception as e:
			return Response(f"There is error occured: {str(e)}", status=500)

	@http.route('/estate-property-tag/<int:tag_id>', auth="public", methods=['DELETE'], csrf=False)
	@authenticate
	def delete_tag(self, tag_id, **kwargs):
		tag = request.env['estate.property.tag'].browse(tag_id)
		tag.unlink()

		response_data = {
			'id': tag_id,
			'message': f"Tag with id #{tag_id} has been deleted."
		}
		return Response(json.dumps(response_data), content_type="application/json")