from odoo import models, fields

class EstatePropertyTagInherit(models.Model):
    _inherit = "estate.property.tag"

    priority = fields.Integer(string="Tag Priority", default=0)
    color = fields.Integer(string="Color Index Overide field", required=True)

    # def create(self):
    # 	# put your codes here
    #     return super().create()

class SalesOrderInherit(models.Model):
    _inherit = "sale.order"

    client_document_number = fields.Char(string="SO Client Number")
