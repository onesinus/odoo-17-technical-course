# -*- coding: utf-8 -*-
# from odoo import http


# class LearnCustomization(http.Controller):
#     @http.route('/learn_customization/learn_customization', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/learn_customization/learn_customization/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('learn_customization.listing', {
#             'root': '/learn_customization/learn_customization',
#             'objects': http.request.env['learn_customization.learn_customization'].search([]),
#         })

#     @http.route('/learn_customization/learn_customization/objects/<model("learn_customization.learn_customization"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('learn_customization.object', {
#             'object': obj
#         })

