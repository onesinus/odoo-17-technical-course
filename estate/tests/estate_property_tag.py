from odoo.tests import TransactionCase


class EstatePropertyTagTest(TransactionCase):

	def setUp(self):
		super(EstatePropertyTagTest).setUp()
		self.estate_property_tag_model = self.env['estate.property.tag']