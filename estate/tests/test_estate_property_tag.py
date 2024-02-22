from odoo.tests import TransactionCase


class TestEstatePropertyTag(TransactionCase):

	def setUp(self):
		super(TestEstatePropertyTag, self).setUp()
		self.estate_property_tag_model = self.env['estate.property.tag']

	def test_create_tag(self):
		tag_data = {
			'name': 'TAG 001',
			'color': 99
		}
		tag = self.estate_property_tag_model.create(tag_data)
		self.assertEqual(tag.name, 'TAG 001')
		self.assertEqual(tag.color, 99)