from odoo.http import request, Response
from odoo.exceptions import AccessError


def authenticate(func):
	def wrapper(*args, **kwargs):
		try:
			token = request.httprequest.headers.get('Authorization')
			user = authenticate_user(token)

			request.env = request.env(user=user)

			kwargs['user'] = user

			return func(*args, **kwargs)
		except AccessError as ae:
			return Response(f"Un-authorized: {(str(ae))}", status=401)
		except Exception as e:
			return Response(f"Bad Request: {str(e)}", status=400)

	return wrapper

def authenticate_user(token):
	user = request.env['res.users'].sudo().search([('auth_token', '=', token)])
	if not user:
		raise AccessError("Invalid authentication token")

	return user